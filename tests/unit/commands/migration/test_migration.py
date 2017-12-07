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

import unittest

import pyxb
from mock import patch
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
