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

import pyxb
from hammr.commands.template import template
from uforge.application import Api
from uforge.objects.uforge import *
from mock import MagicMock
from mock import patch
from mock import ANY
from hammr.utils import constants
import datetime

from tests.unit.utils.file_utils import find_relative_path_for


class TestTemplate(TestCase):
    def test_do_clone_should_split_parameters_even_with_spaces(self):
        # given
        template = self.create_template("url", "username", "password", "login", "password")
        name = "my new name wit spaces"
        args = "--id 42 --name '%s' --version 1.0" % name
        template.clone_appliance = MagicMock(return_value=appliance())

        # when
        template.do_clone(args)

        # then
        self.assertEqual(template.clone_appliance.call_count, 1)
        self.assertEqual(template.clone_appliance.call_args[0][1].name, name)

    @patch('uforge.application.Api._Users._Appliances.Getall')
    @patch('uforge.application.Api._Users._Images.Getall')
    @patch('texttable.Texttable.add_row')
    def test_do_list_succeed_when_appliance_list_with_UTC_Timezone(self, mock_table_add_row, mock_api_images_getall,mock_api_appliance_getall):
        # given
        template = self.create_template("url", "username", "password", "login", "password")

        timeZone = "UTC"
        self.create_appliance_list(timeZone, mock_api_appliance_getall)
        new_images = Images()
        new_images.Images = pyxb.BIND()
        mock_api_images_getall.return_value = new_images

        # when
        template.do_list("")

        # then
        self.assertEquals(mock_table_add_row.call_count, 1)
        mock_table_add_row.assert_called_with([1, "ApplianceWithInstallProfileUTCTimezone", "1.0", "Ubuntu 14.x x86_64", ANY, ANY, 0, None, ANY, ANY])

    def test_do_build_should_return_2_when_no_id_given_and_no_stack_section(self):
        # given
        yaml_path = find_relative_path_for("tests/integration/data/publish_builder.yml")
        args = "--file '%s'" % yaml_path

        template = self.create_template("url", "username", "password", "login", "password")

        # when
        return_value = template.do_build(args)

        # then
        self.assertEqual(2, return_value)

    @patch('uforge.application.Api._Users._Imports._Uploads.Upload')
    @patch('uforge.application.Api._Users._Imports.Import')
    def test_do_create_should_return_2_when_image_already_exist(self, mock_api_imports_getall, mock_api_upload):
        # given
        yaml_path = find_relative_path_for("tests/integration/data/test-parsing.yml")
        args = "--file " + yaml_path
        template = self.create_template("url", "username", "password", "login", "password")

        status = OpStatus()
        status.error = True
        status.message = "error"
        status.errorMessage = "error"
        mock_api_upload.return_value = status

        # when
        return_value = template.do_create(args)

        # then
        self.assertEqual(2, return_value)

    @patch('uforge.application.Api._Users._Appliances._Images.Generate')
    @patch('uforge.application.Api._Users._Targetformats.Getall')
    @patch('uforge.application.Api._Users._Appliances._Installprofile.Getdeprecated')
    @patch('uforge.application.Api._Users._Appliances.Getall')
    def test_do_build_should_return_0_when_id_given_and_no_stack_section(self, mock_api_appliance_getall,
                                                                         mock_api_appliance_getinstallprofile, mock_api_targetformat_getall, mock_api_generate):
        # given
        yaml_path = find_relative_path_for("tests/integration/data/publish_builder.yml")
        args = "--file '%s' --id 1" % yaml_path

        template = self.create_template("url", "username", "password", "login", "password")
        timeZone = "UTC"

        self.create_appliance_list(timeZone, mock_api_appliance_getall)
        self.create_installprofile(timeZone, mock_api_appliance_getinstallprofile)
        self.create_targetformat_list(mock_api_targetformat_getall)
        self.create_targetformat_list(mock_api_targetformat_getall)
        self.prepare_mock_generate(mock_api_generate)

        # when
        return_value = template.do_build(args)

        # then
        self.assertEqual(0, return_value)

    def create_template(self, url, username, password, template_login, template_password):
        templ = template.Template()
        templ.api = Api(url, username=username, password=password, headers=None, disable_ssl_certificate_validation = False, timeout = constants.HTTP_TIMEOUT)
        templ.login = template_login
        templ.password = template_password
        return templ

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

    def create_installprofile(self, timeZone, mock_api_appliance_getinstallprofile):
            install_profile = InstallProfile()
            install_profile.timezone = timeZone

            mock_api_appliance_getinstallprofile.return_value = install_profile

    def create_targetformat_list(self, mock_api_targetformat_getall):
            new_targetformats = TargetFormats()
            new_targetformats.targetFormats = pyxb.BIND()

            format1 = ImageFormat()
            format1.name = "openstackqcow2"

            targetformat1 = TargetFormat()
            targetformat1.format = format1
            targetformat1.name = "OpenStack QCOW2"
            new_targetformats.targetFormats.append(targetformat1)

            mock_api_targetformat_getall.return_value = new_targetformats


    def prepare_mock_generate(self, mock_api_generate):
        image = Image()
        status = OpStatus()
        status.complete = True
        status.message  = "complete"
        image.status = status
        image.uri = "/myimages/2"
        mock_api_generate.return_value = image