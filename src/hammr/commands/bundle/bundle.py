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

from texttable import Texttable
from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from ussclicore.utils import generics_utils, printer
from hammr.utils.hammr_utils import *
from uforge.objects.uforge import *
from hurry.filesize import size

class Bundle(Cmd, CoreGlobal):
    """List or delete existing bundles (mysoftware) on UForge"""

    cmd_name="bundle"

    def __init__(self):
        super(Bundle, self).__init__()

    def arg_list(self):
        doParser = ArgumentParser(prog=self.cmd_name+" list", add_help = True, description="Lists all the bundles that have been registered in the UForge server")
        return doParser

    def do_list(self, args):
        try:
            #call UForge API
            printer.out("Getting all your bundles ...")
            bundles = self.api.Users(self.login).Mysoftware.Getall()
            bundles = bundles.mySoftwareList.mySoftware
            if bundles is None or len(bundles) == 0:
                printer.out("No bundles available")
            else:
                table = Texttable(800)
                table.set_cols_dtype(["t","t","t", "t","t", "t"])
                table.header(["Id", "Name", "Version", "Description", "Size", "Imported"])
                bundles = generics_utils.order_list_object_by(bundles, "name")
                for bundle in bundles:
                    table.add_row([bundle.dbId, bundle.name, bundle.version, bundle.description, size(bundle.size), "X" if bundle.imported else ""])
                print table.draw() + "\n"
                printer.out("Found "+str(len(bundles))+" bundles")

            return 0
        except Exception as e:
            return handle_uforge_exception(e)



    def help_list(self):
        doParser = self.arg_list()
        doParser.print_help()


    def arg_delete(self):
        doParser = ArgumentParser(prog=self.cmd_name+" delete", add_help = True, description="Deletes an existing bundle")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--id', dest='id', required=True, help="the ID of the bundle to delete")
        return doParser

    def do_delete(self, args):
        try:
            #add arguments
            doParser = self.arg_delete()
            try:
                doArgs = doParser.parse_args(args.split())
            except SystemExit as e:
                return
            #call UForge API
            printer.out("Searching bundle with id ["+doArgs.id+"] ...")
            myBundle = self.api.Users(self.login).Mysoftware(doArgs.id).Get()
            if myBundle is None or type(myBundle) is not MySoftware:
                printer.out("Bundle not found", printer.WARNING)
            else:
                table = Texttable(800)
                table.set_cols_dtype(["t","t","t", "t","t", "t"])
                table.header(["Id", "Name", "Version", "Description", "Size", "Imported"])
                table.add_row([myBundle.dbId, myBundle.name, myBundle.version, myBundle.description, size(myBundle.size), "X" if myBundle.imported else ""])
                print table.draw() + "\n"
                if generics_utils.query_yes_no("Do you really want to delete bundle with id "+str(myBundle.dbId)):
                    self.api.Users(self.login).Mysoftware(myBundle.dbId).Delete()
                    printer.out("Bundle deleted", printer.OK)


        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
            self.help_delete()
        except Exception as e:
            return handle_uforge_exception(e)



    def help_delete(self):
        doParser = self.arg_delete()
        doParser.print_help()
        