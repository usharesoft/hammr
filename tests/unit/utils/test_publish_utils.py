# Copyright (c) 2007-2018 UShareSoft, All rights reserved
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
from tests.unit.utils.file_utils import findRelativePathFor

class TestPublishUtils(TestCase):
    def test_is_image_ready_to_publish_should_return_true_when_memory_and_swap_size_are_defined(self):
        # given
        image = self.build_image_to_publish("complete", True)
        file = findRelativePathFor("tests/integration/data/publish_builder.yml")
        builder = self.build_builder(file)

        # when
        image_ready = is_image_ready_to_publish(image, builder)

        # then
        self.assertEqual(image_ready, True)

    def test_is_image_ready_to_publish_should_return_false_when_status_is_cancelled(self):
        # given
        image = self.build_image_to_publish("cancelled", False)
        file = findRelativePathFor("tests/integration/data/publish_builder.yml")
        builder = self.build_builder(file)

        # when
        image_ready = is_image_ready_to_publish(image, builder)

        # then
        self.assertEqual(image_ready, False)

    def build_builder(self, file):
        builder = retrieve_template_from_file(file)
        return builder

    def build_image_to_publish(self, status, status_complete):
        image = Image()
        image.dbId = 1234
        image.imageUri = 'users/guest/scannedinstances/5/scans/12/images/1234'
        image.status = status
        image.status.complete = status_complete

        install_profile = InstallProfile()
        install_profile.memorySize = 1024
        install_profile.swapSize = 1024

        image.installProfile = install_profile
        return image