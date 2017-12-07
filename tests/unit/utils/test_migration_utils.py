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
from uforge.objects import uforge
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
