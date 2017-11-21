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
        i = image.Image()
        i.api = Api("url", username="username", password="password", headers=None,
                    disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        i.login = "login"
        i.password = "password"
        self.create_image(6000, mock_api_getall)
        new_pimages = uforge.publishImages()
        new_pimages.publishImages = pyxb.BIND()
        mock_api_pimg_getall.return_value = new_pimages
        # when
        i.do_list("")

        # then
        self.assertEquals(mock_table_add_row.call_count, 1)
        mock_table_add_row.assert_called_with([ANY, ANY, ANY, ANY, ANY, ANY, size(6000), ANY, ANY])




    def create_image(self, size, mock_api_getall):
        new_images = uforge.images()
        new_images.images = pyxb.BIND()

        newImage = uforge.image()
        newImage.dbId = 1
        newImage.fileSize = size
        newImage.size = 0
        newImage.name = "test"
        newImage.status = "complete"
        newImage.targetFormat = uforge.targetFormat()
        newImage.targetFormat.name = "test"
        newImage.created = datetime.datetime.now()
        newImage.compress = True

        new_images.images.append(newImage)

        mock_api_getall.return_value = new_images
