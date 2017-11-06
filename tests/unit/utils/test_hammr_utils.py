__author__ = 'UshareSoft'

import unittest
import json
import yaml
from mock import patch

from hammr.utils import hammr_utils


class TestFiles(unittest.TestCase):
    def test_pythonObjectFromYamlParsingShouldBeTheSameAsJsonParsing(self):
        # Given
        json_path = "tests/integration/data/test-parsing.json"
        yaml_path = "tests/integration/data/test-parsing.yml"
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

if __name__ == '__main__':
    unittest.main()
