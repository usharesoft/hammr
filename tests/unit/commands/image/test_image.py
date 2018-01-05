# -*- coding: utf-8 -*-
# Copyright 2007-2016 UShareSoft SAS, All rights reserved
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

import pyxb
from mock import patch
from mock import ANY
from uforge.application import Api
from uforge.objects import uforge
from uforge.objects.uforge import *

from hammr.commands.image import image

from hurry.filesize import size
from hammr.utils import constants
import datetime

class TestImage(TestCase):

    @patch('uforge.application.Api._Users._Images.Getall')
    @patch('uforge.application.Api._Users._Pimages.Getall')
    @patch('texttable.Texttable.add_row')
    def test_do_list_check_size(self, mock_table_add_row, mock_api_pimg_getall, mock_api_getall):
        # given
        i = self.create_image()
        mock_api_getall.return_value = self.create_images(6000, "users/myuser/whatever/12/testing/18")
        new_pimages = uforge.publishImages()
        new_pimages.publishImages = pyxb.BIND()
        mock_api_pimg_getall.return_value = new_pimages
        # when
        i.do_list("")

        # then
        self.assertEquals(mock_table_add_row.call_count, 1)
        mock_table_add_row.assert_called_with([ANY, ANY, ANY, ANY, ANY, ANY, size(6000), ANY, ANY])

    @patch('__builtin__.raw_input', return_value='yes')
    @patch('uforge.application.Api._Users._Images.Getall')
    def test_do_delete_return_2_for_wrong_image_uri(self, mock_api_getall, _raw_input):
        # Given
        i = self.create_image()
        mock_api_getall.return_value = self.create_images(6000, "users/myuser/whatever/12/testing/18")

        # When
        return_value = i.do_delete("--id 1")

        # Then
        self.assertEqual(2, return_value)

    @patch('__builtin__.raw_input', return_value='yes')
    @patch('uforge.application.Api._Users._Images.Getall')
    def test_do_delete_return_2_for_wrong_arguments(self, mock_api_getall, _raw_input):
        # Given
        i = self.create_image()
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
        i = self.create_image()
        mock_api_getall.return_value = self.create_images(6000, "users/14/appliances/102/images/1")

        # When
        return_value = i.do_delete("--id 1")

        # Then
        self.assertEqual(0, return_value)

    @patch('__builtin__.raw_input', return_value='yes')
    @patch('uforge.application.Api._Users._Images.Getall')
    def test_do_cancel_return_2_for_non_existing_image(self, mock_api_getall, _raw_input):
        # Given
        i = self.create_image()
        mock_api_getall.return_value = self.create_images(6000, "users/myuser/whatever/12/testing/18")

        # When
        return_value = i.do_cancel("--id 14")

        # Then
        self.assertEqual(2, return_value)

    def create_image(self):
        i = image.Image()
        i.api = Api("url", username="username", password="password", headers=None,
                    disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        i.login = "login"
        i.password = "password"

        return i


    def create_images(self, size, uri):
        new_images = Images()
        new_images.images = pyxb.BIND()

        new_image = Image()
        new_image.dbId = 1
        new_image.fileSize = size
        new_image.size = 0
        new_image.name = "test"
        new_image.status = "complete"
        new_image.targetFormat = uforge.targetFormat()
        new_image.targetFormat.name = "test"
        new_image.created = datetime.datetime.now()
        new_image.compress = True
        new_image.uri = uri

        new_images.images.append(new_image)

        return new_images
