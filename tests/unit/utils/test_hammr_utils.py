__author__ = 'UshareSoft'

import unittest
import json
import yaml
from mock import patch

from hammr.utils import hammr_utils

class TestFiles(unittest.TestCase):

    def test_pythonObjectFromYamlParsingShouldBeTheSameAsJsonParsing(self):
        #Given
        jsonPath = "tests/integration/data/test-parsing.json"
        yamlPath = "tests/integration/data/test-parsing.yml"
        #When
        jsonData = json.load(open(jsonPath))
        yamlData = yaml.load(open(yamlPath))
        #Then
        self.assertEqual(jsonData, yamlData, 'Error : python object made from json parsing is different from yaml parsing')


    @patch("hammr.utils.hammr_utils.validate_configurations_file")
    def test_check_extension_and_validate_json(self, mock_method):
        #Given
        jsonPath = "test.json"
        #When
        hammr_utils.validate(jsonPath)
        #Then
        mock_method.assert_called_with(jsonPath, isJson=True)


    @patch("hammr.utils.hammr_utils.validate_configurations_file")
    def test_check_extension_and_validate_yaml(self, mock_method):
        #Given
        yamlPath = "test.yml"
        #When
        hammr_utils.validate(yamlPath)
        #Then
        mock_method.assert_called_with(yamlPath, isJson=False)


if __name__ == '__main__':
    unittest.main()


