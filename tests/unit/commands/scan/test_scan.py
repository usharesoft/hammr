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
from mock import patch
from uforge.application import Api
from uforge.objects.uforge import *

from hammr.commands.scan import scan
from hammr.commands.scan.scan import Scan
from hammr.utils import constants


class TestScan(TestCase):

    @patch("hammr.utils.hammr_utils.download_binary_in_local_temp_dir")
    @patch.object(Scan, "upload_and_launch_scan_binary")
    @patch('uforge.application.Api._Users._Scannedinstances.Getall')
    @patch("ussclicore.utils.printer.out")
    def test_do_run_return_error_when_regular_scan_and_overlay_option(self, mock_out, mock_api_getall, mock_upload_and_launch_scan_binary, mock_download_binary):
        # given
        name = "RegularScan"
        s, args = self.prepare_scan_run_command(name, "--overlay")

        self.create_scanned_instances(name, False, mock_api_getall)

        # when
        s.do_run(args)

        # then
        self.assertEqual(s.check_overlay_option_is_allowed(name, True), False)
        mock_out.assert_called_with("Performing scan with overlay into the scanned instance [RegularScan] is not allowed. Please retry with another one.", "ERROR")
        self.assertEquals(mock_download_binary.call_count, 0)
        self.assertEquals(mock_upload_and_launch_scan_binary.call_count, 0)

    @patch("hammr.utils.hammr_utils.download_binary_in_local_temp_dir")
    @patch.object(Scan, "upload_and_launch_scan_binary")
    @patch('uforge.application.Api._Users._Scannedinstances.Getall')
    @patch("ussclicore.utils.printer.out")
    def test_do_run_return_error_when_scan_with_overlay_and_no_overlay_option(self, mock_out, mock_api_getall, mock_upload_and_launch_scan_binary, mock_download_binary):
        # given
        name = "ScanWithOverlay"
        s, args = self.prepare_scan_run_command(name, "")

        self.create_scanned_instances(name, True, mock_api_getall)

        # when
        s.do_run(args)

        # then
        self.assertEqual(s.check_overlay_option_is_allowed(name, False), False)
        mock_out.assert_called_with(
            "Performing regular scan into the scanned instance [ScanWithOverlay] is not allowed. Please retry with another one.",
            "ERROR")
        self.assertEquals(mock_download_binary.call_count, 0)
        self.assertEquals(mock_upload_and_launch_scan_binary.call_count, 0)

    @patch("hammr.utils.hammr_utils.download_binary_in_local_temp_dir")
    @patch.object(Scan, "upload_and_launch_scan_binary")
    @patch('uforge.application.Api._Users._Scannedinstances.Getall')
    def test_do_run_succeed_when_scan_with_overlay_and_overlay_option(self, mock_api_getall, mock_upload_and_launch_scan_binary, mock_download_binary):
        #given
        name = "ScanWithOverlay"
        s, args = self.prepare_scan_run_command(name, "--overlay")

        self.create_scanned_instances(name, True, mock_api_getall)
        mock_upload_and_launch_scan_binary.return_value(0)

        # when
        s.do_run(args)

        # then
        self.assertEqual(s.check_overlay_option_is_allowed(name,True), True)
        self.assertEquals(mock_download_binary.call_count, 1)
        self.assertEquals(mock_upload_and_launch_scan_binary.call_count, 1)

    @patch("hammr.utils.hammr_utils.download_binary_in_local_temp_dir")
    @patch.object(Scan, "upload_and_launch_scan_binary")
    @patch('uforge.application.Api._Users._Scannedinstances.Getall')
    def test_do_run_succeed_when_regular_scan_and_no_overlay_option(self, mock_api_getall, mock_upload_and_launch_scan_binary, mock_download_binary):
        # given
        name = "RegularScan"
        s, args = self.prepare_scan_run_command(name, "")

        self.create_scanned_instances(name, False, mock_api_getall)
        mock_download_binary.return_value = ''
        mock_upload_and_launch_scan_binary.return_value(0)

        # when
        s.do_run(args)

        # then
        self.assertEqual(s.check_overlay_option_is_allowed(name, False), True)
        self.assertEquals(mock_download_binary.call_count, 1)
        self.assertEquals(mock_upload_and_launch_scan_binary.call_count, 1)

    def create_scanned_instances(self, name, overlay, mock_api_getall):
        scanned_instances = scannedInstances()
        scanned_instances.scannedInstances = pyxb.BIND()

        newScannedInstance = scannedInstance()
        newScannedInstance.name = name
        newScannedInstance.overlayIncluded = overlay
        scanned_instances.scannedInstances.append(newScannedInstance)

        mock_api_getall.return_value = scanned_instances

    def prepare_scan_run_command(self, name, overlay_option):
        s = scan.Scan()
        s.api = Api("url", username="username", password="password", headers=None,
                    disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        s.login = "login"
        s.password = "password"

        args = "--ip 10.0.0.1 --scan-login login --scan-password password %s --name '%s'" % (overlay_option, name)
        return s, args

    def test_get_uforge_auth_return_password(self):
        # given
        password = "my_password"
        s = scan.Scan()

        # when
        auth = s.get_uforge_auth(None, password)

        # then
        self.assertEqual(" -p " + password, auth)

    def test_get_uforge_auth_return_api_keys(self):
        # given
        publicKey = "my_pub"
        secretKey = "my_secret"
        s = scan.Scan()

        # when
        auth = s.get_uforge_auth({"publickey": publicKey, "secretkey": secretKey}, None)

        # then
        self.assertEqual(" -a " + publicKey + " -s " + secretKey, auth)

