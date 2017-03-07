# Copyright 2007-2015 UShareSoft SAS, All rights reserved
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
from texttable import Texttable
from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from ussclicore.utils import generics_utils, printer
from hammr.utils.hammr_utils import *
from uforge.objects.uforge import *
from hammr.utils import account_utils


class Account(Cmd, CoreGlobal):
    """List, create or delete a cloud account"""

    cmd_name = "account"

    def __init__(self):
        super(Account, self).__init__()

    def arg_list(self):
        doParser = ArgumentParser(prog=self.cmd_name + " list", add_help=True,
                                  description="Displays all the cloud accounts for the user")
        return doParser

    def do_list(self, args):
        try:
            # call UForge API
            printer.out("Getting all your accounts ...")
            accounts = self.api.Users(self.login).Accounts.Getall()
            accounts = accounts.credAccounts.credAccount
            if accounts is None or len(accounts) == 0:
                printer.out("No accounts available")
            else:
                table = Texttable(800)
                table.set_cols_dtype(["t", "t", "t", "t"])
                table.header(["Id", "Name", "Type", "Created"])
                accounts = generics_utils.order_list_object_by(accounts, "name")
                for account in accounts:
                    table.add_row(
                        [account.dbId, account.name, account.targetPlatform.name, account.created.strftime("%Y-%m-%d %H:%M:%S")])
                print table.draw() + "\n"
                printer.out("Found " + str(len(accounts)) + " accounts")
            return 0
        except Exception as e:
            return handle_uforge_exception(e)

    def help_list(self):
        doParser = self.arg_list()
        doParser.print_help()

    def arg_create(self):
        doParser = ArgumentParser(prog=self.cmd_name + " create", add_help=True,
                                  description="Creates a new cloud account")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--file', dest='file', required=True,
                               help="yaml/json file providing the cloud account parameters")
        return doParser

    def do_create(self, args):
        try:
            # add arguments
            doParser = self.arg_create()
            doArgs = doParser.parse_args(shlex.split(args))

            #if the help command is called, parse_args returns None object
            if not doArgs:
                    return 2

            # --
            file = generics_utils.get_file(doArgs.file)
            if file is None:
                return 2
            data = load_data(file)
            if data is None:
                return 2
            if "builders" in data:
                accounts_file_type = "builders"
                iterables = check_mandatory_create_account(data["builders"], accounts_file_type)
            elif "accounts" in data:
                accounts_file_type = "accounts"
                iterables = check_mandatory_create_account(data["accounts"], accounts_file_type)
            else:
                printer.out("Error: no builders or accounts section found", printer.ERROR)
                return 2
            if iterables is None:
                return 2
            try:
                for iterable in iterables:
                    myCredAccount = None
                    if "account" in iterable:
                        account_type = iterable["account"]["type"]
                    elif "type" in iterable:
                        account_type = iterable["type"]

                    targetPlatform = account_utils.get_target_platform_object(self.api, self.login, account_type)
                    if targetPlatform is None:
                        printer.out("Platform type unknown: "+account_type, printer.ERROR)
                        return 2

                    func = getattr(account_utils, generics_utils.remove_special_chars(targetPlatform.type), None)
                    if func:
                        if accounts_file_type == "builders" and "account" in iterable:
                            myCredAccount = func(iterable["account"])
                        elif accounts_file_type == "accounts":
                            myCredAccount = func(iterable)
                        else:
                            pass
                            # DO NOTHING - no account in builder to create

                            # TODO
                            # the account type must be in the account part, if no builder part (independant file)
                        if myCredAccount is not None:
                            myCredAccount = account_utils.assign_target_platform_account(myCredAccount, targetPlatform.name)
                            printer.out("Create account for '" + account_type + "'...")
                            self.api.Users(self.login).Accounts.Create(body=myCredAccount, element_name="ns1:credAccount")
                            printer.out("Account create successfully for [" + account_type + "]", printer.OK)
                return 0

            except KeyError as e:
                printer.out("unknown error template file", printer.ERROR)

        except IOError as e:
            printer.out("File error: " + str(e), printer.ERROR)
        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_create()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_create(self):
        doParser = self.arg_create()
        doParser.print_help()

    def arg_delete(self):
        doParser = ArgumentParser(prog=self.cmd_name + " delete", add_help=True,
                                  description="Deletes an existing cloud account")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--id', dest='id', required=True, help="the ID of the cloud account to delete")
        optional = doParser.add_argument_group("optional arguments")
        optional.add_argument('--no-confirm', dest='no_confirm', action='store_true', required=False,
                              help="do not ask before delete the cloud account")
        doParser.set_defaults(no_confirm=False)
        return doParser

    def do_delete(self, args):
        try:
            # add arguments
            doParser = self.arg_delete()
            doArgs = doParser.parse_args(shlex.split(args))

            #if the help command is called, parse_args returns None object
            if not doArgs:
                    return 2

            # call UForge API
            printer.out("Searching account with id [" + doArgs.id + "] ...")
            account = self.api.Users(self.login).Accounts(doArgs.id).Get()
            if account is None:
                printer.out("No Account available", printer.WARNING)
            else:
                table = Texttable(800)
                table.set_cols_dtype(["t", "t", "t", "t"])
                table.header(["Id", "Name", "Type", "Created"])
                table.add_row(
                    [account.dbId, account.name, account.targetPlatform.name, account.created.strftime("%Y-%m-%d %H:%M:%S")])
                print table.draw() + "\n"
                if doArgs.no_confirm:
                    self.api.Users(self.login).Accounts(doArgs.id).Delete()
                    printer.out("Account deleted", printer.OK)
                elif generics_utils.query_yes_no("Do you really want to delete account with id " + str(account.dbId)):
                    self.api.Users(self.login).Accounts(doArgs.id).Delete()
                    printer.out("Account deleted", printer.OK)
            return 0

        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_delete()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_delete(self):
        doParser = self.arg_delete()
        doParser.print_help()
