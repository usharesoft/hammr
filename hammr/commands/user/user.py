# Copyright (c) 2007-2018 UShareSoft, All rights reserved
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

from texttable import Texttable
from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from ussclicore.utils import generics_utils, printer
from hammr.utils.hammr_utils import *

class User(Cmd, CoreGlobal):
    """Lists information about a user, including login, email, name, date created, and status"""

    cmd_name="user"

    def __init__(self):
        super(User, self).__init__()

    def arg_info(self):
        doParser = ArgumentParser(prog=self.cmd_name+" info", add_help = True, description="Displays informations of provided user")
        return doParser

    def do_info(self, args):
        try:
            #call UForge API
            printer.out("Getting user ["+self.login+"] ...")
            user = self.api.Users(self.login).Get()
            if user is None:
                printer.out("user "+ self.login +"does not exist", printer.ERROR)
            else:
                table = Texttable(200)
                table.set_cols_align(["c", "l", "c", "c", "c", "c", "c", "c"])
                table.header(["Login", "Email", "Lastname",  "Firstname",  "Created", "Active", "Promo Code", "Creation Code"])
                table.add_row([user.loginName, user.email, user.surname , user.firstName, user.created.strftime("%Y-%m-%d %H:%M:%S"), "X", user.promoCode, user.creationCode])
                print table.draw() + "\n"
            return 0
        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
            self.help_info()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_info(self):
        doParser = self.arg_info()
        doParser.print_help()
                