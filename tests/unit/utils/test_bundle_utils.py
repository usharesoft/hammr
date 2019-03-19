from __future__ import absolute_import
__author__ = 'UshareSoft'

import unittest
import json
import yaml
from mock import patch

from ussclicore.utils import generics_utils
from hammr.utils import bundle_utils
from tests.unit.utils.file_utils import find_relative_path_for

class TestFiles(unittest.TestCase):

    @patch("ussclicore.utils.printer.out")
    def test_check_bundle_should_failed_when_no_name(self, mock_method):
        #Given
        jsonPath = find_relative_path_for("tests/integration/data/bundle/bundleWithoutName.json")
        #When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle_utils.check_bundle(bundle)
        #Then
        mock_method.assert_called_with("There is no attribute [name] for a [bundle]", "ERROR")

    @patch("ussclicore.utils.printer.out")
    def test_check_bundle_should_failed_when_no_version(self, mock_method):
        #Given
        jsonPath = find_relative_path_for("tests/integration/data/bundle/bundleWithoutVersion.json")
        #When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle_utils.check_bundle(bundle)
        #Then
        mock_method.assert_called_with("no attribute [version] for [bundle]", "ERROR")

    @patch("ussclicore.utils.printer.out")
    def test_check_bundle_should_failed_when_no_files(self, mock_method):
        #Given
        jsonPath = find_relative_path_for("tests/integration/data/bundle/bundleWithoutFiles.json")
        #When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle_utils.check_bundle(bundle)
        #Then
        mock_method.assert_called_with("no attribute [files] for [bundle]", "ERROR")

    @patch("ussclicore.utils.printer.out")
    def test_check_bundle_should_failed_when_files_no_name(self, mock_method):
        #Given
        jsonPath = find_relative_path_for("tests/integration/data/bundle/bundleFilesWithoutName.json")
        #When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle_utils.check_bundle(bundle)
        #Then
        mock_method.assert_called_with("There is no attribute [name] for a [file]", "ERROR")

    @patch("ussclicore.utils.printer.out")
    def test_check_bundle_should_failed_when_files_no_source(self, mock_method):
        #Given
        jsonPath = find_relative_path_for("tests/integration/data/bundle/bundleFilesWithoutSource.json")
        #When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle_utils.check_bundle(bundle)
        #Then
        mock_method.assert_called_with("There is no attribute [source] for a [file]", "ERROR")

    @patch("ussclicore.utils.printer.out")
    def test_check_bundle_should_failed_when_tag_softwarefile_and_bootorder(self, mock_method):
        #Given
        jsonPath = find_relative_path_for("tests/integration/data/bundle/bundleFilesTagSoftwareFileKeyBootOrder.json")
        #When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle_utils.check_bundle(bundle)
        #Then
        mock_method.assert_called_with("There is the attribute [bootOrder] or [bootType] for file 'directoryTest' but is not tagged as 'bootscript'", "ERROR")

    @patch("ussclicore.utils.printer.out")
    def test_check_bundle_should_failed_when_tag_bootscript_and_rights(self, mock_method):
        #Given
        jsonPath = find_relative_path_for("tests/integration/data/bundle/bundleFilesTagBootScriptKeyRights.json")
        #When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle_utils.check_bundle(bundle)
        #Then
        mock_method.assert_called_with("There is the attribute [ownerGroup], [rights] or [symlink] for file 'cleanup_tmp.sh' but is not tagged as 'softwarefile'", "ERROR")

    @patch("ussclicore.utils.printer.out")
    def test_check_bundle_should_failed_when_tag_ospkg_in_directory(self, mock_method):
        #Given
        jsonPath = find_relative_path_for("tests/integration/data/bundle/bundleFilesTagOSPkgInDirectory.json")
        #When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle_utils.check_bundle(bundle)
        #Then
        mock_method.assert_called_with("The file 'iotop-0.6-2.el7.noarch.rpm, with tag 'ospkg' must be in the first level files section", "ERROR")

    def test_check_bundle_should_succeed_when_no_restrictionRule(self):
        # Given
        jsonPath = find_relative_path_for("tests/integration/data/bundle/bundleWithoutRestrictionRule.json")
        # When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle_utils.check_bundle(bundle)
        # Then
        self.assertIsNotNone(bundle)

    def test_check_bundle_should_succeed_when_empty_restrictionRule(self):
        # Given
        jsonPath = find_relative_path_for("tests/integration/data/bundle/bundleWithEmptyRestrictionRule.json")
        # When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle_utils.check_bundle(bundle)
        # Then
        self.assertIsNotNone(bundle)

    def test_check_bundle_should_succeed(self):
        #Given
        jsonPath = find_relative_path_for("tests/integration/data/bundle/bundleFull.json")
        #When
        bundle = generics_utils.check_json_syntax(jsonPath)
        bundle = bundle_utils.check_bundle(bundle)
        #Then
        self.assertIsNotNone(bundle)

    def test_recursively_append_to_archive_should_failed_when_two_files_have_same_archive_path(self):
        # Given
        bundle = { 'name': 'MyBundle', 'version': '1.0' }
        parent_dir = ""
        duplicate_check_list = []
        archive_files = []
        files = {
            'name': 'myDirectory',
            'source': 'tests/integration/data/aDirectory',
            'tag': 'softwarefile',
            'destination': '/usr/local/myBundle',
            'files': [
                {
                    "name": "file.txt",
                    "source": "tests/integration/data/aDirectory/file1of3.txt"
                },
                {
                    "name": "file.txt",
                    "source": "tests/integration/data/aDirectory/file2of3.txt"
                }
            ]
        }
        # When
        with self.assertRaises(ValueError) as context_manager:
            bundle_utils.recursively_append_to_archive(bundle, files, parent_dir, duplicate_check_list, archive_files)

        # Then
        self.assertEqual(
            context_manager.exception.message,
            "Cannot have identical files in the bundles section: bundles/MyBundle/1.0/myDirectory/file.txt from tests/integration/data/aDirectory/file2of3.txt"
        )

    def test_recursively_append_to_archive_should_succeed_when_several_files_have_same_source(self):
        # Given
        bundle = { 'name': 'MyBundle', 'version': '1.0' }
        parent_dir = ""
        duplicate_check_list = []
        archive_files = []
        files = {
            'name': 'myDirectory',
            'source': 'tests/integration/data/aDirectory',
            'tag': 'softwarefile',
            'destination': '/usr/local/myBundle',
            'files': [
                {
                    'name': 'file1.txt',
                    'source': 'tests/integration/data/aDirectory/file1of3.txt'
                },
                {
                    'name': 'file2.txt',
                    'source': 'tests/integration/data/aDirectory/file1of3.txt'
                },
                {
                    'name': 'pkg1.rpm',
                    'source': 'http://myServer.com/pkg1/download',
                    'install': 'true'
                },
                {
                    'name': 'pkg2.rpm',
                    'source': 'http://myServer.com/pkg2/download',
                    'install': 'true'
                }
            ]
        }
        # When
        r_duplicate_check_list, r_archive_files = bundle_utils.recursively_append_to_archive(bundle, files, parent_dir, duplicate_check_list, archive_files)

        # Then
        self.assertEqual(archive_files, [
            ['bundles/MyBundle/1.0/myDirectory', 'tests/integration/data/aDirectory'],
            ['bundles/MyBundle/1.0/myDirectory/file1.txt', 'tests/integration/data/aDirectory/file1of3.txt'],
            ['bundles/MyBundle/1.0/myDirectory/file2.txt', 'tests/integration/data/aDirectory/file1of3.txt'],
            ['bundles/MyBundle/1.0/myDirectory/pkg1.rpm','http://myServer.com/pkg1/download'],
            ['bundles/MyBundle/1.0/myDirectory/pkg2.rpm', 'http://myServer.com/pkg2/download']
        ])
        self.assertEqual(r_archive_files, archive_files)

    def test_recursively_append_to_archive_should_succeed_when_directory_contains_file_already_described(self):
        # Given
        bundle = { 'name': 'MyBundle', 'version': '1.0' }
        parent_dir = ""
        duplicate_check_list = []
        archive_files = []
        files = {
            'name': 'directoryTest',
            'source': 'tests/integration/data/directoryTest',
            'tag': 'softwarefile',
            'destination': '/usr/local/myBundle',
            'files': [
                {
                    'name': 'file1of3.txt',
                    'source': 'tests/integration/data/directoryTest/file1of3.txt',
                    'rights': '625',
                }
            ]
        }
        # When
        r_duplicate_check_list, r_archive_files = bundle_utils.recursively_append_to_archive(bundle, files, parent_dir, duplicate_check_list, archive_files)

        # Then
        self.assertEqual(archive_files, [
            ['bundles/MyBundle/1.0/directoryTest', 'tests/integration/data/directoryTest'],
            ['bundles/MyBundle/1.0/directoryTest/file1of3.txt', 'tests/integration/data/directoryTest/file1of3.txt'],
            ['bundles/MyBundle/1.0/directoryTest/file2of3.txt', 'tests/integration/data/directoryTest/file2of3.txt'],
            ['bundles/MyBundle/1.0/directoryTest/file3of3.txt', 'tests/integration/data/directoryTest/file3of3.txt']
        ])
        self.assertEqual(r_archive_files, archive_files)

if __name__ == '__main__':
    unittest.main()


