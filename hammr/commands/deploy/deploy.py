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
from ussclicore.utils import generics_utils, printer, progressbar_widget, download_utils
from hammr.utils import *
from uforge.objects.uforge import *
from hammr.utils.hammr_utils import *
from hammr.utils.deployment_utils import *
import shlex
import time
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer, UnknownLength


class Deploy(Cmd, CoreGlobal):
    """Displays all the deployments and instances information"""
    cmd_name = "deploy"
    pbar = None

    def __init__(self):
        super(Deploy, self).__init__()

    def arg_list(self):
        doParser = ArgumentParser(prog=self.cmd_name + " list", add_help=True,
                                  description="Displays all the deployments and instances information")
        return doParser

    def do_list(self, args):
        try:
            printer.out("Getting all deployments for [" + self.login + "] ...")
            deployments = self.api.Users(self.login).Deployments.Getall()
            deployments = deployments.deployments.deployment

            if deployments is None or len(deployments) == 0:
                printer.out("No deployment available")
            else:
                printer.out("Deployments:")
                table = print_deploy_header()
                deployments = generics_utils.order_list_object_by(deployments, "name")
                for deployment in deployments:
                    deployment_id = deployment.applicationId
                    deployment_name = deployment.name
                    deployment_status = deployment.state
                    instances = deployment.instances.instance
                    instance = instances[-1]
                    source_type = source_id = source_name = hostname = location = cloud_provider = str(None)
                    if instance:
                        if instance.sourceSummary and type(instance.sourceSummary) == ScanSummaryLight:
                            source_type = "Scan"
                            source_id = str(extract_scannedinstance_id(instance.sourceSummary.uri))
                            source_name = instance.sourceSummary.name
                        elif instance.sourceSummary and type(instance.sourceSummary) == ApplianceSummary:
                            source_type = "Template"
                            source_id = str(generics_utils.extract_id(instance.sourceSummary.uri))
                            source_name = instance.sourceSummary.name
                        if instance.hostname:
                            hostname = instance.hostname
                        if instance.location:
                            location = instance.location.provider
                        if instance.cloudProvider:
                            cloud_provider = format_cloud_provider(instance.cloudProvider)

                    table.add_row([deployment_name, deployment_id, cloud_provider, location, hostname, source_type, source_id,
                                   source_name, deployment_status])

                print table.draw() + "\n"
                printer.out("Found " + str(len(deployments)) + " deployments")

            return 0
        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_list()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_list(self):
        doParser = self.arg_list()
        doParser.print_help()

    def arg_terminate(self):
        doParser = ArgumentParser(prog=self.cmd_name + " terminate", add_help=True,
                                  description="Terminate a deployment")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--id', dest='id', required=True,
                               help="id of the deployment to terminate")
        optional = doParser.add_argument_group("optional arguments")
        optional.add_argument('--force', '-f', dest='force', required=False, action='store_true',
                              help='Terminate the deployment without asking for confirmation')
        return doParser

    def do_terminate(self, args):
        try:
            # add arguments
            doParser = self.arg_terminate()
            doArgs = doParser.parse_args(shlex.split(args))

            deployment = self.api.Users(self.login).Deployments(doArgs.id).Get()
            if doArgs.force or generics_utils.query_yes_no("Do you really want to terminate deployment with id '" + str(
                    doArgs.id) + "' named '" + deployment.name + "'"):
                # When terminating a running deployment, we stop if the status goes to on-fire.
                # But when terminating an on-fire deployment we stop if it is terminated.
                # So we need to get the status before invoking the terminate.
                status = self.api.Users(self.login).Deployments(doArgs.id).Status.Getdeploystatus()
                initial_status = status.message
                self.api.Users(self.login).Deployments(doArgs.id).Terminate()
                printer.out("Terminating the deployment")
                bar = ProgressBar(widgets=[BouncingBar()], maxval=UnknownLength)
                bar.start()
                i = 1
                while (True):
                    deployment = self.get_deployment(doArgs.id)
                    if deployment is None:
                        break;
                    if initial_status != "on-fire":
                        if deployment.state == "on-fire":
                            # If the deployment went from running to on-fire, we stop and print an error message
                            break
                    time.sleep(1)
                    bar.update(i)
                    i += 2
                bar.finish()

                if deployment:
                    printer.out("Could not terminate the deployment.", printer.ERROR)
                    status = self.api.Users(self.login).Deployments(doArgs.id).Status.Getdeploystatus()
                    if status.message == "on-fire" and status.detailedError:
                        printer.out(status.detailedErrorMsg, printer.ERROR)
                    return 1
                else:
                    printer.out("Deployment terminated", printer.OK)

            return 0
        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_terminate()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_terminate(self):
        doParser = self.arg_terminate()
        doParser.print_help()

    def get_deployment(self, searched_deploy_id):
        deployments = self.api.Users(self.login).Deployments.Getall()
        deployments = deployments.deployments.deployment

        if deployments is None or len(deployments) == 0:
            return None
        else:
            for deployment in deployments:
                deployment_id = deployment.applicationId
                if deployment_id == searched_deploy_id:
                    return deployment
        return None