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

import unittest

import pyxb
from mock import patch
from uforge.application import Api
from uforge.objects import uforge

from hammr.utils import constants
from hammr.utils import migration_utils


class TestMigrationTable(unittest.TestCase):
    @patch('texttable.Texttable.add_row')
    def test_migration_table_add_all_migration_in_progress_in_the_table(self, mock_table_add_row):
        # given
        migrations = uforge.migrations()
        migrations.migrations = pyxb.BIND()
        migration1 = self.create_migration(1, "a migration", 50, "In Progress", False, False, False)
        migrations.migrations.append(migration1)
        migration2 = self.create_migration(2, "a second migration", 55, "In Progress", False, False, False)
        migrations.migrations.append(migration2)

        # when
        migration_utils.migration_table(migrations.migrations.migration)

        # then
        self.assertEquals(mock_table_add_row.call_count, 2)
        mock_table_add_row.assert_any_call([1, "a migration", "In Progress (50%)"])
        mock_table_add_row.assert_any_call([2, "a second migration", "In Progress (55%)"])

    @patch('texttable.Texttable.add_row')
    def test_migration_table_add_the_migration_done_in_the_table(self, mock_table_add_row):
        # given
        migrations = uforge.migrations()
        migrations.migrations = pyxb.BIND()
        migration1 = self.create_migration(1, "a migration", 50, "Done", True, False, False)
        migrations.migrations.append(migration1)

        # when
        migration_utils.migration_table(migrations.migrations.migration)

        # then
        self.assertEquals(mock_table_add_row.call_count, 1)
        mock_table_add_row.assert_any_call([1, "a migration", "Done"])

    @patch('texttable.Texttable.add_row')
    def test_migration_table_add_the_migration_failed_in_the_table(self, mock_table_add_row):
        # given
        migrations = uforge.migrations()
        migrations.migrations = pyxb.BIND()
        migration1 = self.create_migration(1, "a migration", 50, "Failed", False, True, False)
        migrations.migrations.append(migration1)

        # when
        migration_utils.migration_table(migrations.migrations.migration)

        # then
        self.assertEquals(mock_table_add_row.call_count, 1)
        mock_table_add_row.assert_any_call([1, "a migration", "Failed"])

    @patch('texttable.Texttable.add_row')
    def test_migration_table_add_the_migration_cancelled_in_the_table(self, mock_table_add_row):
        # given
        migrations = uforge.migrations()
        migrations.migrations = pyxb.BIND()
        migration1 = self.create_migration(1, "a migration", 50, "Cancelled", False, False, True)
        migrations.migrations.append(migration1)

        # when
        migration_utils.migration_table(migrations.migrations.migration)

        # then
        self.assertEquals(mock_table_add_row.call_count, 1)
        mock_table_add_row.assert_any_call([1, "a migration", "Cancelled"])

    @patch("ussclicore.utils.generics_utils.get_file")
    def test_retrieve_migration_configuration_raise_exception_if_no_file_is_retrieved(self, mock_get_file):
        # given
        args_file = "file_no_present.json"
        mock_get_file.return_value = None

        # when
        with self.assertRaises(Exception) as e:
            migration_utils.retrieve_migration_configuration(args_file)

        # then
        self.assertTrue("No such file or directory: " + args_file in e.exception)

    @patch("ussclicore.utils.generics_utils.get_file")
    @patch("hammr.utils.hammr_utils.load_data")
    def test_retrieve_migration_configuration_raise_exception_if_file_contain_no_migration(self, mock_load_data, mock_get_file):
        # given
        args_file = "file_present.json"
        mock_get_file.return_value = "a file"
        mock_load_data.return_value = self.get_migration_config(migration_key="noMigration")

        # when
        with self.assertRaises(Exception) as e:
            migration_utils.retrieve_migration_configuration(args_file)

        # then
        self.assertTrue("no migration section found" in e.exception)

    @patch("ussclicore.utils.generics_utils.get_file")
    @patch("hammr.utils.hammr_utils.load_data")
    @patch("hammr.utils.migration_utils.check_mandatory_migrate")
    def test_retrieve_migration_configuration_check_mandatory_migrate_if_file_contain_migration(self, mock_check_mandatory_migrate, mock_load_data, mock_get_file):
        # given
        args_file = "file_present.json"
        mock_get_file.return_value = "a file"
        data = self.get_migration_config()
        mock_load_data.return_value = data

        # when
        migration_utils.retrieve_migration_configuration(args_file)

        #  then
        mock_check_mandatory_migrate.assert_called_with(data["migration"])

    def test_check_mandatory_migrate_raise_exception_if_not_contain_name(self):
        # given
        data = self.get_migration_config(name_key="noName")

        # when
        with self.assertRaises(Exception) as e:
            migration_utils.check_mandatory_migrate(data["migration"])

        # then
        self.assertTrue("check yours parameters in file, no attribute [name] for [migration]" in e.exception)

    def test_check_mandatory_migrate_raise_exception_if_not_contain_os(self):
        # given
        data = self.get_migration_config(os_key="noOS")

        # when
        with self.assertRaises(Exception) as e:
            migration_utils.check_mandatory_migrate(data["migration"])

        # then
        self.assertTrue("check yours parameters in file, no attribute [os] for [migration]" in e.exception)

    def test_check_mandatory_migrate_raise_exception_if_os_value_not_valid(self):
        # given
        data = self.get_migration_config(os_value="Windows")

        # when
        with self.assertRaises(Exception) as e:
            migration_utils.check_mandatory_migrate(data["migration"])

        # then
        self.assertTrue("check yours parameters in file, attribute [os] for [migration] is not correct. Only 'linux' is supported" in e.exception)

    def test_check_mandatory_migrate_raise_exception_if_not_contain_source(self):
        # given
        data = self.get_migration_config(source_key="noSource")

        # when
        with self.assertRaises(Exception) as e:
            migration_utils.check_mandatory_migrate(data["migration"])

        # then
        self.assertTrue("check yours parameters in file, no attribute [source] for [migration]" in e.exception)

    def test_check_mandatory_migrate_raise_exception_if_not_contain_target(self):
        # given
        data = self.get_migration_config(target_key="noTarget")

        # when
        with self.assertRaises(Exception) as e:
            migration_utils.check_mandatory_migrate(data["migration"])

        # then
        self.assertTrue("check yours parameters in file, no attribute [target] for [migration]" in e.exception)

    @patch("hammr.utils.migration_utils.check_mandatory_target")
    @patch("hammr.utils.migration_utils.check_mandatory_source")
    def test_check_mandatory_migrate_check_mandatory_source_target_if_contain_source_target(self, mock_check_mandatory_source, mock_check_mandatory_target):
        # given
        data = self.get_migration_config()

        # when
        migration_utils.check_mandatory_migrate(data["migration"])

        #  then
        mock_check_mandatory_source.assert_called_with(data["migration"]["source"])
        mock_check_mandatory_target.assert_called_with(data["migration"]["target"])

    def test_check_mandatory_source_raise_exception_if_not_contain_host(self):
        # given
        data = self.get_migration_config(host_key="noHost")

        # when
        with self.assertRaises(Exception) as e:
            migration_utils.check_mandatory_source(data["migration"]["source"])

        # then
        self.assertTrue("check yours parameters in file, no attribute [host] for [migration][source]" in e.exception)

    def test_check_mandatory_source_raise_exception_if_not_contain_user(self):
        # given
        data = self.get_migration_config(user_key="noUser")

        # when
        with self.assertRaises(Exception) as e:
            migration_utils.check_mandatory_source(data["migration"]["source"])

        # then
        self.assertTrue("check yours parameters in file, no attribute [user] for [migration][source]" in e.exception)

    def test_check_mandatory_target_raise_exception_if_not_contain_builder(self):
        # given
        data = self.get_migration_config(builder_key="noBuilder")

        # when
        with self.assertRaises(Exception) as e:
            migration_utils.check_mandatory_target(data["migration"]["target"])

        # then
        self.assertTrue("check yours parameters in file, no attribute [builder] for [migration][target]" in e.exception)

    @patch("hammr.utils.migration_utils.check_mandatory_builder")
    def test_check_mandatory_target_check_mandatory_builder_if_contain_builder(self, mock_check_mandatory_builder):
        # given
        data = self.get_migration_config()

        # when
        migration_utils.check_mandatory_target(data["migration"]["target"])

        #  then
        mock_check_mandatory_builder.assert_called_with(data["migration"]["target"]["builder"])

    def test_check_mandatory_builder_raise_exception_if_not_contain_type(self):
        # given
        data = self.get_migration_config(type_key="noType")

        # when
        with self.assertRaises(Exception) as e:
            migration_utils.check_mandatory_builder(data["migration"]["target"]["builder"])

        # then
        self.assertTrue("check yours parameters in file, no attribute [type] for [migration][target][builder]" in e.exception)

    def test_check_mandatory_builder_raise_exception_if_not_contain_account(self):
        # given
        data = self.get_migration_config(account_key="noAccount")

        # when
        with self.assertRaises(Exception) as e:
            migration_utils.check_mandatory_builder(data["migration"]["target"]["builder"])

        # then
        self.assertTrue("check yours parameters in file, no attribute [account] for [migration][target][builder]" in e.exception)

    @patch("hammr.utils.migration_utils.check_mandatory_account")
    def test_check_mandatory_builder_check_mandatory_account_if_contain_account(self, mock_check_mandatory_account):
        # given
        data = self.get_migration_config()

        # when
        migration_utils.check_mandatory_builder(data["migration"]["target"]["builder"])

        #  then
        mock_check_mandatory_account.assert_called_with(data["migration"]["target"]["builder"]["account"])

    def test_check_mandatory_account_raise_exception_if_not_contain_name(self):
        # given
        data = self.get_migration_config(account_name_key="noAccountName")

        # when
        with self.assertRaises(Exception) as e:
            migration_utils.check_mandatory_account(data["migration"]["target"]["builder"]["account"])

        # then
        self.assertTrue("check yours parameters in file, no attribute [name] for [migration][target][builder][account]" in e.exception)

    @patch("hammr.utils.generate_utils.get_target_format_object")
    def test_retrieve_target_format_return_the_target_format_found(self, mock_get_target_format_object):
        # given
        api = Api("url", username="username", password="password", headers=None,
                  disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        target_format = uforge.TargetFormat()
        mock_get_target_format_object.return_value = target_format


        # when
        target_format_retrieved = migration_utils.retrieve_target_format(api, "login", "targetFormatName")

        # then
        self.assertEqual(target_format_retrieved, target_format)

    @patch("hammr.utils.generate_utils.get_target_format_object")
    def test_retrieve_target_format_raise_exception_when_the_target_format_not_found(self, mock_get_target_format_object):
        # given
        api = Api("url", username="username", password="password", headers=None,
                  disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        mock_get_target_format_object.return_value = None

        # when
        with self.assertRaises(Exception) as e:
            migration_utils.retrieve_target_format(api, "login", "targetFormatName")

        # then
        self.assertTrue("TargetFormat type unknown: targetFormatName" in e.exception)

    def test_retrieve_image_return_the_image_created(self):
        # given
        api = Api("url", username="username", password="password", headers=None,
                    disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        target_format = uforge.TargetFormat()
        image_format = uforge.ImageFormat()
        image_format.name = "vcenter"
        target_format.format = image_format

        builder = {
            "hardwareSettings": {
                "memory": 512,
                "hwType": 4
            }
        }

        # when
        image_retrieved = migration_utils.retrieve_image(builder, target_format, api, "login")

        # then
        self.assertEqual(image_retrieved.installProfile.memorySize, 512)
        self.assertEqual(image_retrieved.installProfile.hwType, "4")
        self.assertFalse(image_retrieved.compress)

    @patch("ussclicore.utils.generics_utils.remove_special_chars")
    def test_retrieve_image_raise_exception_when_format_name_not_found(self, mock_remove_special_chars):
        # given
        api = Api("url", username="username", password="password", headers=None,
                  disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        target_format = uforge.TargetFormat()
        image_format = uforge.ImageFormat()
        image_format.name = "vcenter"
        target_format.format = image_format

        builder = {
            "hardwareSettings": {
                "memory": 512,
                "hwType": 4
            }
        }

        mock_remove_special_chars.return_value = "vcenternotfound"

        # when
        with self.assertRaises(Exception) as e:
            migration_utils.retrieve_image(builder, target_format, api, "login")

        # then
        self.assertTrue("TargetFormat type is unsupported: vcenter" in e.exception)

    def test_check_mandatory_installation_raise_exception_when_no_installation_for_format_aws(self):
        # given
        install_profile = uforge.InstallProfile()
        install_profile.diskSize = 0

        builder = {
            "type": "Amazon AWS"
        }

        # when
        with self.assertRaises(Exception) as e:
            migration_utils.check_mandatory_installation("aws", builder)

        # then
        self.assertTrue("check yours parameters in file, no attribute [installation] for [migration][target][builder], mandatory to migrate to [Amazon AWS]" in e.exception)

    def test_set_install_profile_disk_size_set_disk_size_when_format_aws(self):
        # given
        install_profile = uforge.InstallProfile()
        install_profile.diskSize = 0

        builder = {
            "installation": {
                "diskSize": 12
            }
        }

        # when
        install_profile = migration_utils.set_install_profile_disk_size(install_profile, builder, "aws")

        # then
        self.assertEqual(install_profile.diskSize, 12)

    def test_set_install_profile_disk_size_not_set_disk_size_when_format_vcenter(self):
        # given
        install_profile = uforge.InstallProfile()
        install_profile.diskSize = 0

        builder = {
            "installation": {
                "diskSize": 12
            }
        }

        # when
        install_profile = migration_utils.set_install_profile_disk_size(install_profile, builder, "vcenter")

        # then
        self.assertEqual(install_profile.diskSize, 0)

    def test_set_install_profile_disk_size_raise_exception_when_no_diskSize(self):
        # given
        install_profile = uforge.InstallProfile()
        install_profile.diskSize = 0

        builder = {
            "type": "Amazon AWS",
            "installation": {}
        }

        # when
        with self.assertRaises(Exception) as e:
            migration_utils.set_install_profile_disk_size(install_profile, builder, "aws")

        # then
        self.assertTrue("check yours parameters in file, no attribute [disksize] for [migration][target][builder][installation], mandatory to migrate to [Amazon AWS]" in e.exception)

    @patch("hammr.utils.publish_builders.publish_vcenter")
    def test_build_publish_image_return_the_publish_image_created(self, mock_publish_vcenter):
        # given
        builder = {
            "displayName": "vcenter-vm-name",
            "esxHost": "esxhost_vcenter",
            "datastore": "datastore_vcenter",
            "network": "network_vcenter"
        }

        cred_account = uforge.CredAccountVSphere()

        publish_image = uforge.PublishImageVSphere()
        publish_image.displayName = builder["displayName"]
        publish_image.esxHost = builder["esxHost"]
        publish_image.datastore = builder["datastore"]
        publish_image.network = builder["network"]

        mock_publish_vcenter.return_value = publish_image

        # when
        publish_image_retrieved = migration_utils.build_publish_image(builder, self.create_target_format("vcenter"), cred_account)

        # then
        mock_publish_vcenter.assert_called_with(builder, cred_account)
        self.assertEqual(publish_image_retrieved.displayName, builder["displayName"])
        self.assertEqual(publish_image_retrieved.esxHost, builder["esxHost"])
        self.assertEqual(publish_image_retrieved.datastore, builder["datastore"])
        self.assertEqual(publish_image_retrieved.network, builder["network"])

    @patch("ussclicore.utils.generics_utils.remove_special_chars")
    def test_build_publish_image_raise_exception_when_format_name_not_found(self, mock_remove_special_chars):
        # given
        builder = {
            "displayName": "vcenter-vm-name",
            "esxHost": "esxhost_vcenter",
            "datastore": "datastore_vcenter",
            "network": "network_vcenter"
        }

        cred_account = uforge.CredAccountVSphere()

        mock_remove_special_chars.return_value = "vcenternotfound"

        # when
        with self.assertRaises(Exception) as e:
            migration_utils.build_publish_image(builder, self.create_target_format("vcenter"), cred_account)

        # then
        self.assertTrue("TargetFormat type is unsupported: vcenter" in e.exception)

    @patch("uforge.application.Api._Users._Accounts.Getall")
    def test_retrieve_account_return_the_cred_account_found(self, mock_api_get_all):
        # given
        api = Api("url", username="username", password="password", headers=None, disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        cred_account = uforge.CredAccountVSphere()
        cred_account.name = "accountName"
        cred_account.uri = "/uri/credAccount"
        cred_accounts = self.create_accounts(cred_account, "vsphere")
        mock_api_get_all.return_value = cred_accounts

        # when
        cred_account_retrieved = migration_utils.retrieve_account(api, "login", cred_account.name)

        # then
        self.assertEqual(cred_account_retrieved.name, cred_account.name)
        self.assertEqual(cred_account_retrieved.uri, cred_account.uri)

    @patch("uforge.application.Api._Users._Accounts.Getall")
    def test_retrieve_account_from_platform_raise_exception_when_no_accounts(self, mock_api_get_all):
        # given
        api = Api("url", username="username", password="password", headers=None,
                  disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        accounts = uforge.CredAccounts()
        accounts.credAccounts = pyxb.BIND()
        mock_api_get_all.return_value = accounts

        # when
        with self.assertRaises(Exception) as e:
            migration_utils.retrieve_account(api, "login", "account")

        # then
        self.assertTrue("No CredAccounts available.\n You can use the command 'hammr account create' to create an account." in e.exception)

    @patch("uforge.application.Api._Users._Accounts.Getall")
    def test_retrieve_account_from_platform_raise_exception_when_account_not_found(self, mock_api_get_all):
        # given
        api = Api("url", username="username", password="password", headers=None, disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        cred_account = uforge.CredAccountVSphere()
        cred_account.name = "accountName"
        cred_account.uri = "/uri/credAccount"
        cred_accounts = self.create_accounts(cred_account, "vsphere")
        mock_api_get_all.return_value = cred_accounts

        # when
        with self.assertRaises(Exception) as e:
            migration_utils.retrieve_account(api, "login", "accountNotFound")

        # then
        self.assertTrue("CredAccount unknown: accountNotFound\n You can use the command 'hammr account create' to create an account." in e.exception)

    def create_migration(self, id, name, percentage, statusMessage, complete, error, cancelled):
        newMigration = uforge.migration()
        newMigration.dbId = id
        newMigration.name = name

        status = uforge.status()
        status.message = statusMessage
        status.percentage = percentage
        status.complete = complete
        status.error = error
        status.cancelled = cancelled

        newMigration.status = status
        return newMigration

    def create_accounts(self, account, target_platform_type):
        target_platform = uforge.TargetPlatform()
        target_platform.name = "targetPlatformName"
        target_platform.type = target_platform_type

        account.targetPlatform = target_platform

        accounts = uforge.CredAccounts()
        accounts.credAccounts = pyxb.BIND()
        accounts.credAccounts.append(account)
        return accounts

    def create_target_format(self, image_format_name):
        image_format = uforge.ImageFormat()
        image_format.name = image_format_name

        target_format = uforge.TargetFormat()
        target_format.format = image_format

        return target_format

    def get_migration_config(self, migration_key="migration", name_key="name", os_key="os", os_value="linux",
                             source_key="source", host_key="host", user_key="user",
                             target_key="target", builder_key="builder", type_key="type", account_key="account", account_name_key="name"):
        migration_config = {
            migration_key: {
                name_key: "myMigration",
                os_key: os_value,
                source_key: {
                    host_key: "127.0.0.1",
                    user_key: "root",
                },
                target_key: {
                    builder_key: {
                        type_key: "VMware vCenter format",
                        account_key: {
                            account_name_key: "credAccountTest"
                        }
                    }
                }
            }
        }
        return migration_config
