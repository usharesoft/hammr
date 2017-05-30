__author__ = 'UshareSoft'

import unittest
import json
import yaml
from mock import patch

from ussclicore.utils import generics_utils
from hammr.utils import bundle_utils

class TestFiles(unittest.TestCase):

    @patch("ussclicore.utils.printer.out")
    def test_check_bundle_should_failed_when_no_name(self, mock_method):
        #Given
        jsonPath = "tests/integration/data/bundle/bundleWithoutName.json"
        #When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle_utils.check_bundle(bundle)
        #Then
        mock_method.assert_called_with("There is no attribute [name] for a [bundle]", "ERROR")

    @patch("ussclicore.utils.printer.out")
    def test_check_bundle_should_failed_when_no_version(self, mock_method):
        #Given
        jsonPath = "tests/integration/data/bundle/bundleWithoutVersion.json"
        #When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle_utils.check_bundle(bundle)
        #Then
        mock_method.assert_called_with("no attribute [version] for [bundle]", "ERROR")

    @patch("ussclicore.utils.printer.out")
    def test_check_bundle_should_failed_when_no_files(self, mock_method):
        #Given
        jsonPath = "tests/integration/data/bundle/bundleWithoutFiles.json"
        #When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle_utils.check_bundle(bundle)
        #Then
        mock_method.assert_called_with("no attribute [files] for [bundle]", "ERROR")

    @patch("ussclicore.utils.printer.out")
    def test_check_bundle_should_failed_when_files_no_name(self, mock_method):
        #Given
        jsonPath = "tests/integration/data/bundle/bundleFilesWithoutName.json"
        #When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle_utils.check_bundle(bundle)
        #Then
        mock_method.assert_called_with("There is no attribute [name] for a [file]", "ERROR")

    @patch("ussclicore.utils.printer.out")
    def test_check_bundle_should_failed_when_files_no_source(self, mock_method):
        #Given
        jsonPath = "tests/integration/data/bundle/bundleFilesWithoutSource.json"
        #When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle_utils.check_bundle(bundle)
        #Then
        mock_method.assert_called_with("There is no attribute [source] for a [file]", "ERROR")

    @patch("ussclicore.utils.printer.out")
    def test_check_bundle_should_failed_when_tag_softwarefile_and_bootorder(self, mock_method):
        #Given
        jsonPath = "tests/integration/data/bundle/bundleFilesTagSoftwareFileKeyBootOrder.json"
        #When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle_utils.check_bundle(bundle)
        #Then
        mock_method.assert_called_with("There is the attribute [bootOrder] or [bootType] for file 'directoryTest' but is not tagged as 'bootscript'", "ERROR")

    @patch("ussclicore.utils.printer.out")
    def test_check_bundle_should_failed_when_tag_bootscript_and_rights(self, mock_method):
        #Given
        jsonPath = "tests/integration/data/bundle/bundleFilesTagBootScriptKeyRights.json"
        #When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle_utils.check_bundle(bundle)
        #Then
        mock_method.assert_called_with("There is the attribute [ownerGroup], [rights] or [symlink] for file 'cleanup_tmp.sh' but is not tagged as 'softwarefile'", "ERROR")

    @patch("ussclicore.utils.printer.out")
    def test_check_bundle_should_failed_when_tag_ospkg_in_directory(self, mock_method):
        #Given
        jsonPath = "tests/integration/data/bundle/bundleFilesTagOSPkgInDirectory.json"
        #When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle_utils.check_bundle(bundle)
        #Then
        mock_method.assert_called_with("The file 'iotop-0.6-2.el7.noarch.rpm, with tag 'ospkg' must be in the first level files section", "ERROR")

    def test_check_bundle_should_succeed_when_no_restrictionRule(self):
        # Given
        jsonPath = "tests/integration/data/bundle/bundleWithoutRestrictionRule.json"
        # When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle_utils.check_bundle(bundle)
        # Then
        self.assertIsNotNone(bundle)

    def test_check_bundle_should_succeed_when_empty_restrictionRule(self):
        # Given
        jsonPath = "tests/integration/data/bundle/bundleWithEmptyRestrictionRule.json"
        # When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle_utils.check_bundle(bundle)
        # Then
        self.assertIsNotNone(bundle)

    def test_check_bundle_should_succeed(self):
        #Given
        jsonPath = "tests/integration/data/bundle/bundleFull.json"
        #When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle = bundle_utils.check_bundle(bundle)
        #Then
        self.assertIsNotNone(bundle)

if __name__ == '__main__':
    unittest.main()


