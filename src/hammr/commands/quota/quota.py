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

from hurry.filesize import size

from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from ussclicore.utils import generics_utils, printer, ascii_bar_graph
from hammr.utils.hammr_utils import *
from hammr.utils import constants



class Quota(Cmd, CoreGlobal):
    """List the status of all the quotas that can be set for the user (disk usage, generations, scans and number of templates)"""

    cmd_name="quota"

    def __init__(self):
        super(Quota, self).__init__()

    def arg_list(self):
        doParser = ArgumentParser(prog=self.cmd_name+" list", add_help = True, description="Displays the user's quota information")
        return doParser

    def do_list(self, args):
        try:
            #call UForge API
            printer.out("Getting quotas for ["+self.login+"] ...")
            quotas = self.api.Users(self.login).Quotas.Get()
            if quotas is None or len(quotas.quotas.quota) == 0:
                printer.out("No quotas available")
            else:
                values = {}
                for quota in quotas.quotas.quota:
                    if quota.limit == -1:
                        nb = " (" + str(quota.nb) + ")"
                    else:
                        nb = " (" + str(quota.nb) + "/" + str(quota.limit) + ")"

                    if quota.type == constants.QUOTAS_SCAN:
                        text = "Scan" + ("s" if quota.nb > 1 else "") + nb
                    elif quota.type == constants.QUOTAS_TEMPLATE:
                        text = "Template" + ("s" if quota.nb > 1 else "") + nb
                    elif quota.type == constants.QUOTAS_GENERATION:
                        text = "Generation" + ("s" if quota.nb > 1 else "") + nb
                    elif quota.type == constants.QUOTAS_DISK_USAGE:
                        text = "Disk usage (" + size(quota.nb) + ")"

                    if quota.limit != -1:
                        nb = float(quota.nb)
                        limit = float(quota.limit)
                        values[text] = (nb/limit) * 50
                    else:
                        values[text] = -1

                ascii_bar_graph.print_graph(values)
            return 0

        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
            self.help_list()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_list(self):
        doParser = self.arg_list()
        doParser.print_help()
