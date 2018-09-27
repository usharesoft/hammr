__author__ = 'UshareSoft'

import unittest
import json
import yaml
import paramiko

from mock import patch
from tests.unit.utils.file_utils import find_relative_path_for

from hammr.utils import constants
from hammr.utils import hammr_utils
from uforge.application import Api


class TestFiles(unittest.TestCase):
    def test_pythonObjectFromYamlParsingShouldBeTheSameAsJsonParsing(self):
        # Given
        json_path = find_relative_path_for("tests/integration/data/test-parsing.json")
        yaml_path = find_relative_path_for("tests/integration/data/test-parsing.yml")
        # When
        json_data = json.load(open(json_path))
        yaml_data = yaml.load(open(yaml_path))
        # Then
        self.assertEqual(json_data, yaml_data,
                         'Error : python object made from json parsing is different from yaml parsing')

    @patch("hammr.utils.hammr_utils.validate_configurations_file")
    @patch("hammr.utils.hammr_utils.check_extension_is_json")
    def test_validate_if_check_extension_is_json_return_true(self, mock_check_extension_is_json,
                                                             mock_validate_configurations_file):
        # Given
        json_path = "test.json"
        mock_check_extension_is_json.return_value = True

        # When
        hammr_utils.validate(json_path)

        # Then
        mock_validate_configurations_file.assert_called_with(json_path, isJson=True)

    @patch("hammr.utils.hammr_utils.validate_configurations_file")
    @patch("hammr.utils.hammr_utils.check_extension_is_json")
    def test_validate_if_check_extension_is_json_return_false(self, mock_check_extension_is_json,
                                                              mock_validate_configurations_file):
        # Given
        json_path = "test.json"
        mock_check_extension_is_json.return_value = False

        # When
        hammr_utils.validate(json_path)

        # Then
        mock_validate_configurations_file.assert_called_with(json_path, isJson=False)

    def test_check_extension_is_json_return_true_if_extension_is_json(self):
        # Given
        json_path = "test.json"

        # When
        is_json = hammr_utils.check_extension_is_json(json_path)

        # Then
        self.assertTrue(is_json)

    def test_check_extension_is_json_return_false_if_extension_is_yaml(self):
        # Given
        yaml_path = "test.yaml"

        # When
        is_json = hammr_utils.check_extension_is_json(yaml_path)

        # Then
        self.assertFalse(is_json)

    def test_check_extension_is_json_return_false_if_extension_is_yml(self):
        # Given
        yml_path = "test.yml"

        # When
        is_json = hammr_utils.check_extension_is_json(yml_path)

        # Then
        self.assertFalse(is_json)

    def test_check_extension_raise_exception_if_extension_is_not_supported(self):
        # Given
        unsupported_extension_path = "test.uss"

        # When
        # Then
        self.assertRaises(Exception, hammr_utils.check_extension_is_json, unsupported_extension_path)

    def test_extract_appliance_id_return_correct_id_for_correct_uri(self):
        # Given
        tested_uri = "users/14/appliances/12/whatever/8/testing"

        # When
        appliance_id = hammr_utils.extract_appliance_id(tested_uri)

        # Then
        self.assertEqual(12, appliance_id)

    def test_extract_appliance_id_return_none_for_non_appliance_uri(self):
        # Given
        tested_uri = "users/myuser/scannedinstances/18/scans/15/testing"

        # When
        appliance_id = hammr_utils.extract_appliance_id(tested_uri)

        # Then
        self.assertIsNone(appliance_id)

    def test_extract_scan_id_return_correct_id_for_correct_uri(self):
        # Given
        tested_uri = "users/14/scannedinstances/12/scans/108/whatever/18/testing"

        # When
        scan_id = hammr_utils.extract_scan_id(tested_uri)

        # Then
        self.assertEqual(108, scan_id)

    def test_extract_scan_id_return_none_for_non_scan_uri(self):
        # Given
        tested_uri = "users/14/appliances/12/whatever/8/testing"

        # When
        scan_id = hammr_utils.extract_scan_id(tested_uri)

        # Then
        self.assertIsNone(scan_id)

    def test_extract_scannedinstance_id_return_correct_id_for_correct_uri(self):
        # Given
        tested_uri = "users/14/scannedinstances/120/scans/108/whatever/18/testing"

        # When
        scannedinstance_id = hammr_utils.extract_scannedinstance_id(tested_uri)

        # Then
        self.assertEqual(120, scannedinstance_id)

    def test_extract_scannedinstance_id_return_non_for_nonscan_uri(self):
        # Given
        tested_uri = "users/14/appliances/12/whatever/8/testing"

        # When
        scannedinstance_id = hammr_utils.extract_scannedinstance_id(tested_uri)

        # Then
        self.assertIsNone(scannedinstance_id)

    def test_is_uri_based_on_scan_return_true_for_scan_uri(self):
        # Given
        tested_uri = "users/myuser/scannedinstances/120/scans/108/images/12"

        # When
        is_scan_uri = hammr_utils.is_uri_based_on_scan(tested_uri)

        # Then
        self.assertTrue(is_scan_uri)

    def test_is_uri_based_on_scan_return_false_for_appliance_uri(self):
        # Given
        tested_uri = "users/14/appliances/102/images/8"

        # When
        is_scan_uri = hammr_utils.is_uri_based_on_scan(tested_uri)

        # Then
        self.assertFalse(is_scan_uri)

    def test_is_uri_based_on_appliance_return_true_for_app_uri(self):
        # Given
        tested_uri = "users/14/appliances/102/images/8"

        # When
        is_appliance_uri = hammr_utils.is_uri_based_on_appliance(tested_uri)

        # Then
        self.assertTrue(is_appliance_uri)

    def test_is_uri_based_on_appliance_return_false_for_scan_uri(self):
        # Given
        tested_uri = "users/myuser/scannedinstances/120/scans/108/images/12"

        # When
        is_appliance_uri = hammr_utils.is_uri_based_on_appliance(tested_uri)

        # Then
        self.assertFalse(is_appliance_uri)

    @patch("ussclicore.utils.download_utils.Download")
    @patch("ussclicore.utils.generics_utils.get_uforge_url_from_ws_url")
    @patch("os.mkdir")
    def test_download_binary_in_local_temp_dir_download_with_good_url_and_directory(self, mock_mkdir, mock_get_uforge_url, mock_download):
        # Given
        api = Api("url", username="username", password="password", headers=None,
                  disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        mock_get_uforge_url.return_value = "/url"
        # When
        local_binary_path = hammr_utils.download_binary_in_local_temp_dir(api, "/tmp/local/temp/dir", "/uri/binary", "binaryName")

        # Then
        mock_download.assert_called_with("/url/uri/binary", "/tmp/local/temp/dir/binaryName", not api.getDisableSslCertificateValidation())
        self.assertEqual(local_binary_path, "/tmp/local/temp/dir/binaryName")

    @patch("paramiko.SFTPClient.from_transport")
    @patch("paramiko.SFTPClient")
    @patch("paramiko.Transport")
    @patch("paramiko.SSHClient.connect")
    def test_upload_binary_to_client_use_put_from_paramiko_SFTPClient(self, mock_connect, mock_transport, mock_sftp_client, mock_paramiko_from_transport):
        # Given
        mock_paramiko_from_transport.return_value = mock_sftp_client

        # When
        hammr_utils.upload_binary_to_client("hostname", 22, "username", "password",
                                            "/tmp/local/temp/dir/binaryName", "/tmp/uri/binary", None)

        # Then
        mock_transport.assert_called_with(("hostname", 22))
        mock_sftp_client.put.assert_called_with("/tmp/local/temp/dir/binaryName", "/tmp/uri/binary")
        mock_connect.assert_called_with("hostname", 22, "username", "password", None)

    @patch("paramiko.SSHClient.exec_command")
    def test_launch_binary_call_exec_command_with_given_command(self, mock_exec_command):
        # Given
        mock_exec_command.return_value = "stdin", "stdout", "stderr"

        # When
        hammr_utils.launch_binary(paramiko.SSHClient(), "command to launch")

        # Then
        mock_exec_command.assert_called_with("command to launch")

    def test_validate_builder_file_with_no_template_id_return_None_when_stack_is_missing(self):
        # Given
        yaml_path = find_relative_path_for("tests/integration/data/publish_builder.yml")

        # When
        data = hammr_utils.validate_builder_file_with_no_template_id(yaml_path)

        # Then
        self.assertEqual(data, None)

    def test_validate_builder_file_with_no_template_id_return_None_when_builder_is_missing(self):
        # Given
        yaml_path = find_relative_path_for("tests/integration/data/test-parsing.yml")

        # When
        data = hammr_utils.validate_builder_file_with_no_template_id(yaml_path)

        # Then
        self.assertEqual(data, None)

    def test_validate_validate_builder_file_with_no_template_id_return_data_when_stack_and_builder_are_not_missing(self):
        # Given
        json_path = find_relative_path_for("tests/integration/data/templatePXE.json")

        # When
        data = hammr_utils.validate_builder_file_with_no_template_id(json_path)

        # Then
        self.assertNotEqual(data, None)

    def test_validate_builder_file_with_no_template_id_return_None_when_stack_and_builder_are_missing(self):
        # Given
        yaml_path = find_relative_path_for("tests/integration/data/deploy_aws.yml")

        # When
        data = hammr_utils.validate_builder_file_with_no_template_id(yaml_path)

        # Then
        self.assertEqual(data, None)

if __name__ == '__main__':
    unittest.main()
