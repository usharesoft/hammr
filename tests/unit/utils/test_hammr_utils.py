__author__ = 'UshareSoft'

import unittest
import json
import yaml
from mock import patch

from tests.unit.utils.file_utils import findRelativePathFor
from hammr.utils import hammr_utils


class TestFiles(unittest.TestCase):
    def test_pythonObjectFromYamlParsingShouldBeTheSameAsJsonParsing(self):
        # Given
        json_path = findRelativePathFor("tests/integration/data/test-parsing.json")
        yaml_path = findRelativePathFor("tests/integration/data/test-parsing.yml")
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

if __name__ == '__main__':
    unittest.main()
