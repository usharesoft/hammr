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

from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from hammr.utils.hammr_utils import *
from hammr.utils import migration_utils


class Migration(Cmd, CoreGlobal):
    """List existing migrations"""

    cmd_name = "migration"

    def __init__(self):
        super(Migration, self).__init__()

    def arg_list(self):
        doParser = ArgumentParser(prog=self.cmd_name + " list", add_help=True,
                                  description="Displays all the migrations for the user")
        return doParser

    def do_list(self, args):
        try:
            # call UForge API
            printer.out("Getting migrations for [" + self.login + "] ...")
            migrations = self.api.Users(self.login).Migrations.Getall()
            migrations = migrations.migrations.migration

            if len(migrations) == 0:
                printer.out("No migrations available")
                return
            print migration_utils.migration_table(migrations).draw() + "\n"

        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_list()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_list(self):
        doParser = self.arg_list()
        doParser.print_help()
