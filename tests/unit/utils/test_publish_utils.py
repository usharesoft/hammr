# Copyright (c) 2007-2019 UShareSoft, All rights reserved
#
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from unittest import TestCase

from hammr.utils.publish_utils import *
from hammr.utils.hammr_utils import *
from uforge.application import Api
from uforge.objects.uforge import *
from uforge.objects import uforge
from tests.unit.utils.file_utils import find_relative_path_for
from mock import patch, call

from hammr.commands.image import image

class TestPublishUtils(TestCase):
    app_uri = 'users/guest/appliances/5/images/1234/'
    scan_uri = 'users/guest/scannedinstances/5/scans/12/images/1234'
    published_app_uri = 'users/guest/appliances/5/images/1234/pimages/5678'
    published_scan_uri = 'users/guest/scannedinstances/5/scans/12/images/1234/pimages/5678'

    def test_is_image_ready_to_publish_returns_true_when_memory_and_swap_size_are_defined(self):
        # given
        image = self.build_image_to_publish("complete", True, self.app_uri)
        file = find_relative_path_for("tests/integration/data/publish_builder.yml")
        builder = self.build_builder(file)

        # when
        image_ready = is_image_ready_to_publish(image, builder)

        # then
        self.assertEqual(image_ready, True)

    def test_is_image_ready_to_publish_returns_false_when_status_is_cancelled(self):
        # given
        image = self.build_image_to_publish("cancelled", False, self.app_uri)
        file = find_relative_path_for("tests/integration/data/publish_builder.yml")
        builder = self.build_builder(file)

        # when
        image_ready = is_image_ready_to_publish(image, builder)

        # then
        self.assertEqual(image_ready, False)

    @patch('uforge.application.Api._Users._Scannedinstances._Scans._Images._Pimages.Publish')
    def test_call_publish_webservice_returns_published_image_for_a_scan_image(self, mock_scan_publish):
        # given
        mock_scan_publish.return_value = self.build_published_image(self.published_scan_uri)
        image = self.build_image_to_publish("complete", True, self.scan_uri)
        image_object = self.build_image_object()
        source = self.build_source_scan()

        # when
        published_image = call_publish_webservice(image_object, image, source, None)

        # then
        self.assertEqual(type(published_image), type(PublishImageAws()))

    @patch('uforge.application.Api._Users._Appliances._Images._Pimages.Publish')
    def test_call_publish_webservice_returns_published_image_for_a_template_image(self, mock_template_publish):
        # given
        mock_template_publish.return_value = self.build_published_image(self.published_app_uri)
        image = self.build_image_to_publish("complete", True, self.app_uri)
        image_object = self.build_image_object()
        source = self.build_source_template()

        # when
        published_image = call_publish_webservice(image_object, image, source, None)

        # then
        self.assertEqual(type(published_image), type(PublishImageAws()))

    @patch("ussclicore.utils.printer.out")
    @patch('progressbar.ProgressBar.finish')
    @patch('progressbar.ProgressBar.start')
    @patch('hammr.commands.image.image.Image.get_publish_image_from_publish_id')
    def test_print_publish_status_prints_ids_when_build_successful(self, mock_get_publish_image, mock_progressbar_start, mock_progressbar_finish, printer):
        #given
        image_object = self.build_image_object()
        published_image = self.build_image_to_publish("complete", True, self.app_uri)
        account_name = "my_account"
        mock_get_publish_image.return_value = published_image
        mock_progressbar_start.return_value = ProgressBar(None, None)
        mock_progressbar_finish.return_value = None

        #when
        print_publish_status(image_object, None, None, published_image, None, account_name)

        #then
        calls = []
        calls.append(call('Publication to ' + account_name + ' is ok', 'OK'))
        calls.append(call('Publish ID : ' + str(published_image.dbId)))
        calls.append(call('Cloud ID : ' + published_image.cloudId))
        printer.assert_has_calls(calls)

    def test_call_publish_webservice_raises_exception_for_wrong_image_uri(self):
        # given
        image = self.build_image_to_publish("complete", True, 'wrong/uri/')
        image_object = self.build_image_object()
        source = self.build_source_template()

        # when
        try:
            call_publish_webservice(image_object, image, source, None)

            # then
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def build_builder(self, file):
        builder = retrieve_template_from_file(file)
        return builder

    def build_image_to_publish(self, status, status_complete, uri):
        image = Image()
        image.dbId = 1234
        image.cloudId = "abcd-5678"
        image.uri = uri
        image.status = status
        image.status.complete = status_complete

        install_profile = InstallProfile()
        install_profile.memorySize = 1024
        install_profile.swapSize = 1024

        image.installProfile = install_profile
        return image

    def build_source_scan(self):
        source = Scan()
        source.uri = self.scan_uri
        return source

    def build_source_template(self):
        source = Appliance()
        source.uri = self.app_uri
        return source

    def build_published_image(self, uri):
        image = PublishImageAws()
        image.dbId = 5678
        image.imageUri = uri
        return image

    def build_image_object(self):
        image_object = image.Image()
        api = Api(None, username="user", password="pass", headers=None,
                  disable_ssl_certificate_validation=True, timeout=constants.HTTP_TIMEOUT)
        image_object.api = api
        image_object.login = "guest"
        return image_object

