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
from hurry.filesize import size

from texttable import Texttable
from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from argparse import RawTextHelpFormatter
from ussclicore.cmd import Cmd, CoreGlobal
from ussclicore.utils import generics_utils, printer
from hammr.utils.hammr_utils import *



class Os(Cmd, CoreGlobal):
    """List all the OSes the user has access to. Includes, name, version, architecture and release date. You can also search for available packages"""

    cmd_name="os"

    def __init__(self):
        super(Os, self).__init__()


    def arg_list(self):
        doParser = ArgumentParser(prog=self.cmd_name+" list", add_help = True, description="Displays all the operating systems available to use by the use")
        return doParser

    def do_list(self, args):
        try:
            #call UForge API
            printer.out("Getting distributions for ["+self.login+"] ...")
            distributions = self.api.Users(self.login).Distros.Getall()
            distributions = distributions.distributions
            if distributions is None or not hasattr(distributions, "distribution"):
                printer.out("No distributions available")
            else:
                table = Texttable(800)
                table.set_cols_dtype(["t","t","t","t","t", "t"])
                table.header(["Id", "Name", "Version", "Architecture", "Release Date", "Profiles"])
                distributions = generics_utils.order_list_object_by(distributions.distribution, "name")
                for distribution in distributions:
                    profiles = self.api.Distributions(distribution.dbId).Profiles.Getall()
                    profiles = profiles.distribProfiles.distribProfile
                    if len(profiles) > 0:
                        profile_text=""
                        for profile in profiles:
                            profile_text+=profile.name+"\n"
                        table.add_row([distribution.dbId, distribution.name, distribution.version, distribution.arch, distribution.releaseDate.strftime("%Y-%m-%d %H:%M:%S") if distribution.releaseDate is not None else "", profile_text])
                    else:
                        table.add_row([distribution.dbId, distribution.name, distribution.version, distribution.arch, distribution.releaseDate.strftime("%Y-%m-%d %H:%M:%S") if distribution.releaseDate is not None else "", "-"])
                print table.draw() + "\n"
                printer.out("Found "+str(len(distributions))+" distributions")
            return 0
        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
            self.help_list()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_list(self):
        doParser = self.arg_list()
        doParser.print_help()



    def arg_search(self):
        doParser = ArgumentParser(prog=self.cmd_name+" search", add_help = True, description="Search packages from an OS", formatter_class=RawTextHelpFormatter)
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--id', dest='id', required=True, help="Os id")
        mandatory.add_argument('--pkg', dest='pkg', required=True, help='''\
                Regular expression of the package:\n\
                "string" : search all packages which contains "string"\n\
                "*string": search all packages which end with "string"\n\
                "string*": search all packages which start with "string"''')
        return doParser

    def do_search(self, args):
        try:
            #add arguments
            doParser = self.arg_search()
            doArgs = doParser.parse_args(shlex.split(args))

            #if the help command is called, parse_args returns None object
            if not doArgs:
                    return 2

            #call UForge API
            printer.out("Search package '"+doArgs.pkg+"' ...")
            distribution = self.api.Distributions(doArgs.id).Get()
            printer.out("for OS '"+distribution.name+"', version "+distribution.version)
            pkgs = self.api.Distributions(distribution.dbId).Pkgs.Getall(Query="name=="+doArgs.pkg)
            pkgs = pkgs.pkgs.pkg
            if pkgs is None or len(pkgs) == 0:
                printer.out("No package found")
            else:
                table = Texttable(800)
                table.set_cols_dtype(["t","t","t","t","t","t","t"])
                table.header(["Name", "Version", "Arch", "Release", "Build date", "Size", "FullName"])
                pkgs = generics_utils.order_list_object_by(pkgs, "name")
                for pkg in pkgs:
                    table.add_row([pkg.name, pkg.version, pkg.arch, pkg.release, pkg.pkgBuildDate.strftime("%Y-%m-%d %H:%M:%S"), size(pkg.size), pkg.fullName])
                print table.draw() + "\n"
                printer.out("Found "+str(len(pkgs))+" packages")
        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
            self.help_search()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_search(self):
        doParser = self.arg_search()
        doParser.print_help()

