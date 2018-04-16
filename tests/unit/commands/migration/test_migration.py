# -*- coding: utf-8 -*-
# Copyright 2007-2017 UShareSoft SAS, All rights reserved
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
import shlex
import unittest

import pyxb
from mock import patch, Mock
from mock import ANY
from uforge.application import Api
from uforge.objects import uforge

from hammr.commands.migration import migration
from hammr.utils import constants


class TestMigration(unittest.TestCase):
    @patch('hammr.utils.migration_utils.migration_table')
    @patch('uforge.application.Api._Users._Migrations.Getall')
    def test_migration_table_return_the_list_of_migrations_when_there_are_migrations(self, mock_api_getall, mock_migration_table):
        # given
        m = migration.Migration()
        m.api = Api("url", username="username", password="password", headers=None,
                    disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        m.login = "login"
        m.password = "password"

        migrations = uforge.migrations()
        migrations.migrations = pyxb.BIND()
        migration1 = self.create_migration(1, "a migration", 50, "In Progress", False, False, False)

        migrations.migrations.append(migration1)
        mock_api_getall.return_value = migrations

        # when
        m.do_list("")

        # then
        mock_migration_table.assert_called_with(migrations.migrations.migration)

    @patch('hammr.utils.migration_utils.migration_table')
    @patch("ussclicore.utils.printer.out")
    @patch('uforge.application.Api._Users._Migrations.Getall')
    def test_do_list_return_no_migration_message_when_there_is_no_migration(self, mock_api_getall, mock_message, mock_migration_table):
        # given
        m = migration.Migration()
        m.api = Api("url", username="username", password="password", headers=None,
                    disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        m.login = "login"
        m.password = "password"
        migrations = uforge.migrations()
        migrations.migrations = pyxb.BIND()
        mock_api_getall.return_value = migrations

        # when
        m.do_list("")

        # then
        mock_message.assert_called_with("No migrations available")
        mock_migration_table(ANY).assert_not_called()

    @patch("hammr.utils.hammr_utils.download_binary_in_local_temp_dir")
    @patch("hammr.utils.migration_utils.retrieve_migration_configuration")
    @patch("hammr.utils.migration_utils.retrieve_target_format")
    @patch("hammr.utils.migration_utils.retrieve_image")
    @patch("hammr.utils.migration_utils.retrieve_publish_image")
    @patch("hammr.utils.migration_utils.retrieve_account")
    @patch("hammr.commands.migration.Migration.create_migration")
    @patch("hammr.commands.migration.Migration.upload_and_launch_migration_binary")
    @patch("uforge.application.Api._Users._Migrations.Create")
    @patch("ussclicore.utils.printer.out")
    @patch("shutil.rmtree")
    def test_do_launch_succeed_when_all_parameters_are_ok(self, mock_rmtree, mock_out, mock_api_create, mock_upload_and_launch_migration_binary, mock_create_migration, mock_retrieve_account, mock_retrieve_publish_image, mock_retrieve_image, mock_retrieve_target_format, mock_retrieve_migration_configuration, mock_download_binary):
        # given
        m = migration.Migration()
        m.api = Api("url", username="username", password="password", headers=None,
                    disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        m.login = "login"
        m.password = "password"

        mock_retrieve_migration_configuration.return_value = self.get_migration_config()
        mock_retrieve_target_format.return_value = self.create_targetFormat("targetFormatRetrieved")
        mock_retrieve_image.return_value = uforge.Image()
        mock_retrieve_publish_image.return_value = uforge.PublishImageVSphere()
        mock_retrieve_account.return_value = uforge.CredAccountVSphere()
        migration_to_create = uforge.migration()
        mock_create_migration.return_value = migration_to_create
        mock_upload_and_launch_migration_binary.return_value(0)

        # when
        m.do_launch("--file config.json")

        # then
        self.assertEquals(mock_api_create.call_count, 1)
        self.assertEquals(mock_download_binary.call_count, 1)
        self.assertEquals(mock_upload_and_launch_migration_binary.call_count, 1)
        self.assertEquals(mock_rmtree.call_count, 1)
        mock_out.assert_called_with("Migration launched successfully, please go to the platform to follow steps of the migration.", "OK")

    @patch("ussclicore.utils.printer.out")
    def test_do_launch_display_message_error_when_apikeys_given(self, mock_out):
        # given
        m = migration.Migration()
        m.api = Api("url", username="username", password="password", headers=None,
                    disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        m.login = "login"
        m.apikeys = {"publickey": "the_public_key", "secretkey": "the_secret_key"}

        # when
        m.do_launch("--file config.json")

        # then
        mock_out.assert_called_with("Using API keys with command 'hammr migration launch' is not yet supported. Please use password.", "ERROR")

    @patch("ussclicore.utils.printer.out")
    def test_do_launch_display_message_error_when_file_not_given(self, mock_out):
        # given
        m = migration.Migration()

        # when
        m.do_launch("--file")

        # then
        mock_out.assert_called_with("ERROR: In Arguments: argument --file: expected one argument", "ERROR")

    @patch("ussclicore.utils.generics_utils.get_file")
    @patch("ussclicore.utils.printer.out")
    def test_do_launch_display_message_error_when_file_is_not_found(self, mock_out, mock_get_file):
        # given
        m = self.prepare_migrate_command()
        mock_get_file.return_value = None

        # when
        m.do_launch("--file config.json")

        # then
        mock_out.assert_called_with("No such file or directory: config.json", "ERROR")

    @patch("ussclicore.utils.generics_utils.get_file")
    @patch("ussclicore.utils.printer.out")
    @patch("hammr.utils.hammr_utils.load_data")
    def test_do_launch_display_message_error_when_configuration_file_do_not_contain_migration_parameter(self, mock_load_data, mock_out, mock_get_file):
        # given
        m = self.prepare_migrate_command()
        mock_get_file.return_value = "a file"
        mock_load_data.return_value = "something wrong"

        # when
        m.do_launch("--file config.json")

        # then
        mock_out.assert_called_with("no migration section found", "ERROR")

    @patch("hammr.utils.hammr_utils.launch_binary")
    @patch("hammr.utils.hammr_utils.upload_binary_to_client")
    def test_upload_and_launch_migration_binary_succeed_empty_exclude(self, mock_upload_binary, mock_launch_binary):
        # given
        m = migration.Migration()
        m.api = Api("url", username="username", password="password", headers=None,
                    disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        m.login = "login"
        m.password = "password"

        migration_config = self.get_migration_config()

        # when
        m.upload_and_launch_migration_binary(m.login, m.password, migration_config, "local_uforge_migration_path", m.api.getUrl())

        # then
        mock_upload_binary.assert_called_with(migration_config["source"]["host"], migration_config["source"]["ssh-port"], migration_config["source"]["user"], migration_config["source"]["password"], "local_uforge_migration_path", "/tmp/" + constants.MIGRATION_BINARY_NAME)

        command_launch = 'chmod +x ' + '/tmp/' + constants.MIGRATION_BINARY_NAME + '; nohup ' + '/tmp/' + constants.MIGRATION_BINARY_NAME + ' -u login -p password -U url -n \'' +  migration_config["name"] + '\' ' + ' >/dev/null 2>&1 &'
        mock_launch_binary.assert_called_with(ANY, command_launch)

    @patch("hammr.utils.hammr_utils.launch_binary")
    @patch("hammr.utils.hammr_utils.upload_binary_to_client")
    def test_upload_and_launch_migration_binary_succeed_with_exclude(self, mock_upload_binary, mock_launch_binary):
        # given
        m = migration.Migration()
        m.api = Api("url", username="username", password="password", headers=None,
                    disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        m.login = "login"
        m.password = "password"

        migration_config = self.get_migration_config(["/folder_to_exclude", "/folder/file_to_exclude.txt", "/folder/file to exclude with space.txt"])

        # when
        m.upload_and_launch_migration_binary(m.login, m.password, migration_config, "local_uforge_migration_path",
                                             m.api.getUrl())

        # then
        mock_upload_binary.assert_called_with(migration_config["source"]["host"],
                                              migration_config["source"]["ssh-port"],
                                              migration_config["source"]["user"],
                                              migration_config["source"]["password"], "local_uforge_migration_path",
                                              "/tmp/" + constants.MIGRATION_BINARY_NAME)

        exclude_parameter = "-e '/folder_to_exclude' -e '/folder/file_to_exclude.txt' -e '/folder/file to exclude with space.txt' "
        command_launch = 'chmod +x ' + '/tmp/' + constants.MIGRATION_BINARY_NAME + '; nohup ' + '/tmp/' + constants.MIGRATION_BINARY_NAME + ' -u login -p password -U url -n \'' + \
                         migration_config["name"] + '\' ' + exclude_parameter + ' >/dev/null 2>&1 &'
        mock_launch_binary.assert_called_with(ANY, command_launch)

    def test_create_migration_create_a_migration_with_all_stages(self):
        # given
        m = migration.Migration()
        data = {
            "migration": {
                "name": "myMigrationTest",
                "os": "linux"
            }
        }
        target_format = self.create_targetFormat("nameTargetFormat")
        cred_account = uforge.CredAccountVSphere()
        install_profile = uforge.InstallProfile()
        image = uforge.Image()
        image.installProfile = install_profile
        publish_image = uforge.PublishImageVSphere()
        publish_image.credAccount = cred_account

        # when
        my_migration = m.create_migration(data["migration"]["name"], data["migration"]["os"], target_format.name, image, publish_image)

        # then
        self.assertEqual(my_migration.name, "myMigrationTest")
        self.assertEqual(my_migration.stages.stage[0].family, data["migration"]["os"])
        self.assertEqual(my_migration.stages.stage[1].image.targetFormat.name, target_format.name)
        self.assertEqual(my_migration.stages.stage[1].image.installProfile, install_profile)
        self.assertEqual(my_migration.stages.stage[2].publishImage.targetFormat.name, target_format.name)
        self.assertEqual(my_migration.stages.stage[2].publishImage.credAccount, cred_account)

    @patch('hammr.utils.migration_utils.migration_table')
    @patch('uforge.application.Api._Users._Migrations.Get')
    @patch("ussclicore.utils.printer.out")
    def test_do_delete_not_launch_migration_table_when_the_migration_does_not_exist(self, mock_message, mock_api_get,
                                                                                    mock_migration_table):
        # given
        m, args = self.prepare_migrate_run_command("100")
        mock_api_get.return_value = None

        # when
        m.do_delete(args)

        # then
        mock_migration_table(ANY).assert_not_called()
        mock_message.assert_called_with("No migration available with id 100")

    @patch('hammr.utils.migration_utils.migration_table')
    @patch('uforge.application.Api._Users._Migrations.Delete')
    @patch('uforge.application.Api._Users._Migrations.Get')
    @patch('ussclicore.utils.generics_utils.query_yes_no')
    @patch("ussclicore.utils.printer.out")
    def test_do_delete_launch_migration_table_when_the_migration_does_exist(self, mock_message, mock_query_yes_no, mock_api_get,
                                                                            mock_api_delete, mock_migration_table):
        # given
        m, args = self.prepare_migrate_run_command("100")
        migration = self.create_migration(1, "a migration", 50, "In Progress", False, False, False)
        mock_api_get.return_value = migration
        mock_query_yes_no.return_value = True

        # when
        m.do_delete(args)

        # then
        mock_message.assert_called_with("Migration deleted", "OK")
        mock_migration_table.assert_called_with([migration])
        mock_api_delete.assert_called_with()

    @patch('hammr.utils.migration_utils.migration_table')
    @patch('uforge.application.Api._Users._Migrations.Delete')
    @patch('uforge.application.Api._Users._Migrations.Get')
    @patch('ussclicore.utils.generics_utils.query_yes_no')
    def test_do_delete_do_not_ask_to_confirm_delete_migration_when_the_command_contain_no_confirm_argument(self, mock_query_yes_no, mock_api_get, mock_api_delete, mock_migration_table):
        # given
        m, args = self.prepare_migrate_run_command("100", no_confirm = True)
        migration = self.create_migration(1, "a migration", 50, "In Progress", False, False, False)
        mock_api_get.return_value = migration

        # when
        m.do_delete(args)

        # then
        mock_query_yes_no.assert_not_called()
        mock_api_delete.assert_called_with()

    def create_migration(self, id, name, percentage, statusMessage, complete, error, cancelled):
        migration = uforge.migration()
        migration.dbId = id
        migration.name = name

        status = uforge.status()
        status.message = statusMessage
        status.percentage = percentage
        status.complete = complete
        status.error = error
        status.cancelled = cancelled

        migration.status = status
        return migration

    def prepare_migrate_command(self):
        m = migration.Migration()
        m.api = Api("url", username="username", password="password", headers=None,
                    disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        m.login = "login"
        m.password = "password"

        return m

    def prepare_migrate_run_command(self, id=0, no_confirm=False):
        m = self.prepare_migrate_command()

        args = "--id " + id
        if no_confirm:
            args = "--id " + id + " --no-confirm"

        return m, args

    def createAccounts(self, account):
        target_platform = uforge.targetPlatform()
        target_platform.name = "targetPlatformName"

        account.targetPlatform = target_platform
        accounts = uforge.credAccounts()
        accounts.credAccounts = pyxb.BIND()
        accounts.credAccounts.append(account)
        return accounts

    def create_targetFormat(self, name):
        target_format = uforge.TargetFormat()
        target_format.name = name
        return target_format

    def get_migration_config(self, exclude_list=[]):
        migration_config = {
            "migration": {
                "name": "myMigration",
                "os": "linux",
                "source": {
                    "host": "127.0.0.1",
                    "ssh-port": 22,
                    "user": "root",
                    "password": "password",
                    "exclude": exclude_list
                },
                "target": {
                    "builder": {
                        "type": "VMware vCenter format",
                        "displayName": "vcenter-vm-name",
                        "esxHost": "esxhost_vcenter",
                        "datastore": "datastore_vcenter",
                        "network": "network_vcenter",
                        "account": {
                            "name": "credAccountTest"
                        }
                    }
                }
            }
        }
        return migration_config["migration"]