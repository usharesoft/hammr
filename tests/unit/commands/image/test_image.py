# -*- coding: utf-8 -*-
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

import datetime
import pyxb
from mock import patch, ANY, call
from texttable import Texttable
from hurry.filesize import size

from uforge.application import Api
from uforge.objects import uforge
from hammr.commands.image import image
from hammr.utils import constants
import tests.unit.commands.image.info_test_utils as info_utils

class TestImage(TestCase):

    @patch('uforge.application.Api._Users._Images.Getall')
    @patch('uforge.application.Api._Users._Pimages.Getall')
    @patch('texttable.Texttable.add_row')
    def test_do_list_check_size(self, mock_table_add_row, mock_api_pimg_getall, mock_api_getall):
        # given
        i = self.prepare_image()
        mock_api_getall.return_value = self.create_images(6000, "users/myuser/whatever/12/testing/18")
        new_pimages = uforge.publishImages()
        new_pimages.publishImages = pyxb.BIND()
        mock_api_pimg_getall.return_value = new_pimages
        # when
        i.do_list("")

        # then
        self.assertEquals(mock_table_add_row.call_count, 1)
        mock_table_add_row.assert_called_with([ANY, ANY, ANY, ANY, ANY, ANY, size(6000), ANY, ANY])

    @patch('uforge.application.Api._Users._Images.Getall')
    @patch('hammr.commands.image.image.Image.do_info_draw_publication')
    @patch('hammr.commands.image.image.Image.do_info_draw_general')
    def test_do_info_should_call_draw_methods(self, mock_draw_general, mock_draw_publication, mock_api_getall):
        # given
        i = self.prepare_image()
        info_image = info_utils.create_image()

        mock_api_getall.return_value = info_utils.create_images(info_image)

        # when
        i.do_info("--id 1")

        # then
        mock_draw_general.assert_called_once_with(info_image)
        mock_draw_publication.assert_called_once_with(info_image)

    @patch('hammr.commands.image.image.Image.do_info_draw_generation')
    @patch('hammr.commands.image.image.Image.do_info_draw_source')
    @patch('texttable.Texttable.add_row')
    @patch('texttable.Texttable.draw')
    def test_do_info_draw_general(self, mock_table_draw, mock_table_add_row, mock_draw_source, mock_draw_generation):
        # given
        i = self.prepare_image()
        info_image = info_utils.create_image()

        # when
        i.do_info_draw_general(info_image)

        # then
        calls = []
        calls.append(call(["Name", info_image.name]))
        calls.append(call(["Format", info_image.targetFormat.name]))
        calls.append(call(["Id", info_image.dbId]))
        calls.append(call(["Version", info_image.version]))
        calls.append(call(["Revision", info_image.revision]))
        calls.append(call(["Uri", info_image.uri]))
        calls.append(call(["Created", info_image.created.strftime("%Y-%m-%d %H:%M:%S")]))
        calls.append(call(["Size", size(info_image.fileSize)]))
        calls.append(call(["Compressed", "Yes" if info_image.compress else "No"]))

        mock_table_draw.assert_called_once()
        mock_draw_source.assert_called_once()
        mock_draw_generation.assert_called_once()
        assert mock_table_add_row.call_count == 9
        mock_table_add_row.assert_has_calls(calls)

    @patch('hammr.commands.image.image.Image.do_info_draw_generation')
    @patch('hammr.commands.image.image.Image.do_info_draw_source')
    @patch('texttable.Texttable.add_row')
    @patch('texttable.Texttable.draw')
    def test_do_info_draw_general_docker_image(self, mock_table_draw, mock_table_add_row,
                                               mock_draw_source, mock_draw_generation):
        # given
        i = self.prepare_image()
        info_image = info_utils.create_image_format_docker()

        # when
        i.do_info_draw_general(info_image)

        # then
        calls = []
        calls.append(call(["Name", info_image.name]))
        calls.append(call(["Format", info_image.targetFormat.name]))
        calls.append(call(["Id", info_image.dbId]))
        calls.append(call(["Version", info_image.version]))
        calls.append(call(["Revision", info_image.revision]))
        calls.append(call(["Uri", info_image.uri]))
        calls.append(call(["Created", info_image.created.strftime("%Y-%m-%d %H:%M:%S")]))
        calls.append(call(["Size", size(info_image.fileSize)]))
        calls.append(call(["Compressed", "Yes" if info_image.compress else "No"]))
        calls.append(call(["RegisteringName", info_image.registeringName]))
        calls.append(call(["Entrypoint", info_image.entrypoint]))

        mock_table_draw.assert_called_once()
        mock_draw_source.assert_called_once()
        mock_draw_generation.assert_called_once()
        assert mock_table_add_row.call_count == 11
        mock_table_add_row.assert_has_calls(calls)

    @patch('uforge.application.Api._Users._Appliances.Get')
    @patch('texttable.Texttable.add_row')
    def test_do_info_draw_source_appliance(self, mock_table_add_row, mock_api_appliances_get):
        # given
        i = self.prepare_image()
        appliance = info_utils.create_appliance()
        mock_api_appliances_get.return_value = appliance

        # when
        i.do_info_draw_source(appliance.uri, Texttable(0))

        # then
        calls = []
        calls.append(call(["OS", appliance.distributionName + " " + appliance.archName]))
        calls.append(call(["Template Id", appliance.dbId]))
        calls.append(call(["Description", appliance.description]))

        assert mock_table_add_row.call_count == 3
        mock_table_add_row.assert_has_calls(calls)

    @patch('uforge.application.Api._Users._Scannedinstances.Get')
    @patch('texttable.Texttable.add_row')
    def test_do_info_draw_source_scan(self, mock_table_add_row, mock_api_scannedinstances_get):
        # given
        i = self.prepare_image()
        scanned_instance = info_utils.create_scanned_instance()
        mock_api_scannedinstances_get.return_value = scanned_instance

        # when
        i.do_info_draw_source(scanned_instance.uri, Texttable(0))

        # then
        calls = []
        distro = scanned_instance.distribution
        calls.append(call(["OS", distro.name + " " + distro.version + " " + distro.arch]))
        calls.append(call(["Scan Id", scanned_instance.dbId]))

        assert mock_table_add_row.call_count == 2
        mock_table_add_row.assert_has_calls(calls)

    @patch('uforge.application.Api._Users._Mysoftware._Templates.Get')
    @patch('uforge.application.Api._Users._Mysoftware.Get')
    @patch('texttable.Texttable.add_row')
    def test_do_info_draw_source_my_software(self, mock_table_add_row, mock_api_mysoftware_get, mock_api_templates_get):
        # given
        i = self.prepare_image()
        my_software = info_utils.create_my_software()
        container_template = info_utils.create_container_template()
        mock_api_mysoftware_get.return_value = my_software
        mock_api_templates_get.return_value = container_template

        # when
        i.do_info_draw_source(container_template.uri, Texttable(0))

        # then
        calls = []
        distro = container_template.distribution
        calls.append(call(["OS", distro.name + " " + distro.version + " " + distro.arch]))
        calls.append(call(["MySoftware Id", my_software.dbId]))
        calls.append(call(["Description", my_software.description]))

        assert mock_table_add_row.call_count == 3
        mock_table_add_row.assert_has_calls(calls)

    @patch('hammr.utils.image_utils.get_message_from_status')
    @patch('texttable.Texttable.add_row')
    def test_do_info_draw_generation_without_error(self, mock_table_add_row, mock_msg_from_status):
        # given
        i = self.prepare_image()
        info_image = info_utils.create_image()
        mock_msg_from_status.return_value = "Done"

        # when
        i.do_info_draw_generation(info_image, Texttable(0))

        # then
        calls = []
        calls.append(call(["Generation Status", "Done"]))
        calls.append(call(["Generation Message", info_image.status.message]))

        assert mock_table_add_row.call_count == 2
        mock_table_add_row.assert_has_calls(calls)
        mock_msg_from_status.assert_called_once_with(info_image.status)

    @patch('hammr.utils.image_utils.get_message_from_status')
    @patch('texttable.Texttable.add_row')
    def test_do_info_draw_generation_with_error(self, mock_table_add_row, mock_msg_from_status):
        # given
        i = self.prepare_image()
        info_image = info_utils.create_image_status_error()
        mock_msg_from_status.return_value = "Error"

        # when
        i.do_info_draw_generation(info_image, Texttable(0))

        # then
        calls = []
        calls.append(call(["Generation Status", "Error"]))
        calls.append(call(["Generation Message", info_image.status.message]))
        calls.append(call(["Detailed Error Message", info_image.status.errorMessage]))

        assert mock_table_add_row.call_count == 3
        mock_table_add_row.assert_has_calls(calls)
        mock_msg_from_status.assert_called_once_with(info_image.status)

    @patch('hammr.utils.image_utils.get_message_from_status')
    @patch('uforge.application.Api._Users._Pimages.Getall')
    @patch('texttable.Texttable.add_row')
    @patch('texttable.Texttable.draw')
    def test_do_info_draw_publication(self, mock_table_draw, mock_table_add_row,
                                      mock_api_pimg_getall, mock_msg_from_status):
        # given
        i = self.prepare_image()
        info_image = info_utils.create_image()
        pimage = info_utils.create_pimage()
        mock_api_pimg_getall.return_value = info_utils.create_pimages(pimage)
        mock_msg_from_status.return_value = "Done"

        # when
        i.do_info_draw_publication(info_image)

        # then
        mock_msg_from_status.assert_called_once_with(pimage.status)
        mock_table_draw.assert_called_once()
        mock_table_add_row.assert_called_once_with(["Done", pimage.cloudId])

    @patch('__builtin__.raw_input', return_value='yes')
    @patch('uforge.application.Api._Users._Images.Getall')
    def test_do_delete_return_2_for_wrong_image_uri(self, mock_api_getall, _raw_input):
        # Given
        i = self.prepare_image()
        mock_api_getall.return_value = self.create_images(6000, "users/myuser/whatever/12/testing/18")

        # When
        return_value = i.do_delete("--id 1")

        # Then
        self.assertEqual(2, return_value)

    @patch('__builtin__.raw_input', return_value='yes')
    @patch('uforge.application.Api._Users._Images.Getall')
    def test_do_delete_return_2_for_wrong_arguments(self, mock_api_getall, _raw_input):
        # Given
        i = self.prepare_image()
        mock_api_getall.return_value = self.create_images(6000, "users/myuser/whatever/12/testing/18")

        # When
        return_value = i.do_delete("--id 1 --test 18")

        # Then
        self.assertEqual(2, return_value)

    @patch('uforge.application.Api._Users._Appliances._Images.Delete')
    @patch('__builtin__.raw_input', return_value='yes')
    @patch('uforge.application.Api._Users._Images.Getall')
    def test_do_delete_return_0_when_ok(self, mock_api_getall, _raw_input, mock_api_delete):
        # Given
        i = self.prepare_image()
        mock_api_getall.return_value = self.create_images(6000, "users/14/appliances/102/images/1")

        # When
        return_value = i.do_delete("--id 1")

        # Then
        self.assertEqual(0, return_value)

    @patch('__builtin__.raw_input', return_value='yes')
    @patch('uforge.application.Api._Users._Images.Getall')
    def test_do_cancel_return_2_for_non_existing_image(self, mock_api_getall, _raw_input):
        # Given
        i = self.prepare_image()
        mock_api_getall.return_value = self.create_images(6000, "users/myuser/whatever/12/testing/18")

        # When
        return_value = i.do_cancel("--id 14")

        # Then
        self.assertEqual(2, return_value)

    @patch("hammr.utils.publish_builders.publish_vcenter")
    def test_build_publish_image_return_the_publish_image_created(self, mock_publish_vcenter):
        # given
        i = self.prepare_image()

        builder = {
            "displayName": "vcenter-vm-name",
            "esxHost": "esxhost_vcenter",
            "datastore": "datastore_vcenter",
            "network": "network_vcenter"
        }

        cred_account = uforge.CredAccountVSphere()

        publish_image = uforge.PublishImageVSphere()
        publish_image.displayName = builder["displayName"]
        publish_image.esxHost = builder["esxHost"]
        publish_image.datastore = builder["datastore"]
        publish_image.network = builder["network"]

        mock_publish_vcenter.return_value = publish_image

        # when
        publish_image_retrieved = i.build_publish_image(self.create_image("vcenter"), builder, cred_account)

        # then
        mock_publish_vcenter.assert_called_with(builder, cred_account)
        self.assertEqual(publish_image_retrieved.displayName, builder["displayName"])
        self.assertEqual(publish_image_retrieved.esxHost, builder["esxHost"])
        self.assertEqual(publish_image_retrieved.datastore, builder["datastore"])
        self.assertEqual(publish_image_retrieved.network, builder["network"])

    @patch("ussclicore.utils.printer.out")
    @patch("hammr.commands.image.image.Image.get_all_images")
    def test_do_download_should_display_command_when_docker_format(self, get_all_images, printer):
        # given
        i = self.prepare_image()
        image = info_utils.create_image_format_docker()
        get_all_images.return_value = [image]

        # when
        i.do_download("--id " + str(image.dbId))

        # then
        printer.assert_called_with("docker pull " + image.registeringName)

    def prepare_image(self):
        i = image.Image()
        i.api = Api("url", username="username", password="password", headers=None,
                    disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        i.login = "login"
        i.password = "password"

        return i

    def create_image(self, target_format_name):
        image_format = uforge.ImageFormat()
        image_format.name = target_format_name

        target_format = uforge.TargetFormat()
        target_format.name = target_format_name
        target_format.format = image_format

        image = uforge.Image()
        image.targetFormat = target_format
        return image

    def create_images(self, size, uri):
        new_images = uforge.Images()
        new_images.images = pyxb.BIND()

        new_image = self.create_image("vcenter")
        new_image.dbId = 1
        new_image.fileSize = size
        new_image.size = 0
        new_image.name = "test"
        new_image.status = "complete"
        new_image.created = datetime.datetime.now()
        new_image.compress = True
        new_image.uri = uri

        new_images.images.append(new_image)

        return new_images
