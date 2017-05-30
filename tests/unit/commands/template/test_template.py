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
from hammr.commands.template import template
from uforge.application import Api
from uforge.objects.uforge import *
from mock import MagicMock
from mock import patch
from mock import ANY
from hammr.utils import constants
import datetime


class TestTemplate(TestCase):
    def test_do_clone_should_split_parameters_even_with_spaces(self):
        # given
        t = template.Template()
        name = "my new name wit spaces"
        args = "--id 42 --name '%s' --version 1.0" % name
        t.clone_appliance = MagicMock(return_value=appliance())

        # when
        t.do_clone(args)

        # then
        self.assertEqual(t.clone_appliance.call_count, 1)
        self.assertEqual(t.clone_appliance.call_args[0][1].name, name)

    @patch('uforge.application.Api._Users._Appliances.Getall')
    @patch('uforge.application.Api._Users._Images.Getall')
    @patch('texttable.Texttable.add_row')
    def test_do_list_succeed_when_appliance_list_with_UTC_Timezone(self, mock_table_add_row, mock_api_images_getall,mock_api_appliance_getall):
        # given
        t = template.Template()
        t.api = Api("url", username="username", password="password", headers=None, disable_ssl_certificate_validation = False, timeout = constants.HTTP_TIMEOUT)
        t.login = "login"
        t.password = "password"
        timeZone = "UTC"
        self.create_appliance_list(timeZone, mock_api_appliance_getall)
        new_images = Images()
        new_images.Images = pyxb.BIND()
        mock_api_images_getall.return_value = new_images

        # when
        t.do_list("")

        # then
        self.assertEquals(mock_table_add_row.call_count, 1)
        mock_table_add_row.assert_called_with([1, "ApplianceWithInstallProfileUTCTimezone", "1.0", "Ubuntu 14.x x86_64", ANY, ANY, 0, None, ANY, ANY])


    def create_appliance_list(self, timeZone, mock_api_appliance_getall):
            new_appliances = Appliances()
            new_appliances.appliances = pyxb.BIND()

            prof = InstallProfile()
            prof.timezone = timeZone

            newAppliance = Appliance()
            newAppliance.dbId = 1
            newAppliance.created = datetime.datetime.now()
            newAppliance.lastModified = datetime.datetime.now()
            newAppliance.name = "ApplianceWithInstallProfileUTCTimezone"
            newAppliance.version = "1.0"
            newAppliance.archName = "x86_64"
            newAppliance.distributionName = "Ubuntu 14.x"
            newAppliance.installProfile = prof

            new_appliances.appliances.append(newAppliance)

            mock_api_appliance_getall.return_value = new_appliances