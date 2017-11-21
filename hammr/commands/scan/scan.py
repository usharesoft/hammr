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

import urllib
import os.path
import shutil
import paramiko
import getpass
import shlex
import sys
import time

from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer
from ussclicore.utils import generics_utils, printer, progressbar_widget, download_utils
from hammr.utils import *
from uforge.objects.uforge import *
from hammr.utils.hammr_utils import *


class Scan(Cmd, CoreGlobal):
    """List or delete existing scan images, build an image from a scan, launch the scan of a live system, or import a scan as an image"""

    cmd_name = "scan"

    def __init__(self):
        super(Scan, self).__init__()

    def arg_list(self):
        doParser = ArgumentParser(prog=self.cmd_name + " list", add_help=True,
                                  description="Displays all the scans for the user")
        return doParser

    def do_list(self, args):
        try:
            # call UForge API
            printer.out("Getting scans for [" + self.login + "] ...")
            myScannedInstances = self.api.Users(self.login).Scannedinstances.Getall(Includescans="true")
            myScannedInstances = myScannedInstances.scannedInstances.scannedInstance
            if myScannedInstances is None or len(myScannedInstances) == 0:
                printer.out("No scans available")
                return
            print scan_utils.scan_table(myScannedInstances).draw() + "\n"
            printer.out("Found " + str(len(myScannedInstances)) + " scans")
        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_list()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_list(self):
        doParser = self.arg_list()
        doParser.print_help()

    def arg_run(self):
        doParser = ArgumentParser(prog=self.cmd_name + " run", add_help=True,
                                  description="Executes a deep scan of a running system")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--ip', dest='ip', required=True,
                               help="the IP address or fully qualified hostname of the running system")
        mandatory.add_argument('--scan-login', dest='login', required=True, help="the root user name (normally root)")
        mandatory.add_argument('--name', dest='name', required=True,
                               help="the scan name to use when creating the scan meta-data")
        optional = doParser.add_argument_group("optional arguments")
        optional.add_argument('--scan-port', dest='port', required=False,
                              help="the ssh port of the running system")
        optional.add_argument('--scan-password', dest='password', required=False,
                              help="the root password to authenticate to the running system")
        optional.add_argument('--dir', dest='dir', required=False,
                              help="the directory where to install the uforge-scan.bin binary used to execute the deep scan")
        optional.add_argument('--exclude', dest='exclude', nargs='+', required=False,
                              help="a list of directories or files to exclude during the deep scan")
        optional.add_argument('-o', '--overlay', dest='overlay', action='store_true', required=False, help="perform a scan with overlay into the given scanned instance")
        return doParser

    def do_run(self, args):
        try:
            # add arguments
            doParser = self.arg_run()
            doArgs = doParser.parse_args(shlex.split(args))

            #if the help command is called, parse_args returns None object
            if not doArgs:
                    return 2

            if not self.check_overlay_option_is_allowed(doArgs.name, doArgs.overlay):
                return 2

            # download scan binary
            uri = generics_utils.get_uforge_url_from_ws_url(self.api.getUrl())
            download_url = uri + constants.URI_SCAN_BINARY

            if os.path.isdir(constants.TMP_WORKING_DIR):
                # delete tmp dir
                shutil.rmtree(constants.TMP_WORKING_DIR)
            os.mkdir(constants.TMP_WORKING_DIR)
            local_uforge_scan_path = constants.TMP_WORKING_DIR + os.sep + constants.SCAN_BINARY_NAME

            dlUtils = download_utils.Download(download_url, local_uforge_scan_path, not self.api.getDisableSslCertificateValidation())
            try:
                dlUtils.start()
            except Exception, e:
                return 2

            r_code = self.deploy_and_launch_agent(self.login, self.password, doArgs, local_uforge_scan_path,
                                                  self.api.getUrl())

            if r_code != 0:
                return

            # delete tmp dir
            shutil.rmtree(constants.TMP_WORKING_DIR)

            printer.out("Searching scan on uforge ...")
            running = True
            while running:
                myScannedInstances = self.api.Users(self.login).Scannedinstances.Getall(Includescans="true",
                                                                                    Name=doArgs.name)
                myScannedInstances = myScannedInstances.scannedInstances.scannedInstance
                if myScannedInstances is None or len(myScannedInstances) == 0:
                    time.sleep(5)
                else:
                    if len(myScannedInstances) > 1:
                        printer.out("A scan with the same name already exists", printer.ERROR)
                    myScannedInstance = myScannedInstances[0]
                    if len(myScannedInstance.scans.scan) == 0:
                        time.sleep(5)
                    else:
                        for scan in myScannedInstance.scans.scan:
                            if (not scan.status.complete and not scan.status.error and not scan.status.cancelled):
                                status = scan.status
                                statusWidget = progressbar_widget.Status()
                                statusWidget.status = status
                                widgets = [Bar('>'), ' ', statusWidget, ' ', ReverseBar('<')]
                                progress = ProgressBar(widgets=widgets, maxval=100).start()
                                while not (status.complete or status.error or status.cancelled):
                                    statusWidget.status = status
                                    progress.update(status.percentage)
                                    status = (self.api.Users(self.login).Scannedinstances(myScannedInstance.dbId).Scans(
                                        scan.dbId).Get("false", "false", "false", "false", None, None, None, None,
                                                       None)).status
                                    time.sleep(2)
                                statusWidget.status = status
                                progress.finish()
                                if status.error:
                                    printer.out("Scan  error: " + status.message + "\n" + status.errorMessage,
                                                printer.ERROR)
                                    if status.detailedError:
                                        printer.out(status.detailedErrorMsg)
                                elif status.cancelled:
                                    printer.out("Scan canceled: " + status.message, printer.WARNING)
                                else:
                                    printer.out("Scan successfully", printer.OK)
                                running = False
                                break
                            else:
                                pass


        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_run()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_run(self):
        doParser = self.arg_run()
        doParser.print_help()

    def check_overlay_option_is_allowed(self, name, overlay):
        myScannedInstance = self.api.Users(self.login).Scannedinstances.Getall(Includescans="true", Name=name)
        myScannedInstance = myScannedInstance.scannedInstances.scannedInstance
        if myScannedInstance is not None and len(myScannedInstance) > 0:
            myScannedInstance = myScannedInstance[0]
            if ((overlay and not myScannedInstance.overlayIncluded) or (
                not overlay and myScannedInstance.overlayIncluded)):
                scanTypeString = 'regular scan'
                if overlay:
                    scanTypeString = 'scan with overlay'
                printer.out(
                    "Performing {0} into the scanned instance [{1}] is not allowed. Please retry with another one.".format(
                        scanTypeString, name), printer.ERROR)
                return False
        return True

    def arg_build(self):
        doParser = ArgumentParser(prog=self.cmd_name + " build", add_help=True,
                                  description="Builds a machine image from a scan")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--id', dest='id', required=True,
                               help="the ID of the scan to generate the machine image from")
        mandatory.add_argument('--file', dest='file', required=True, help="yaml/json file providing the builder parameters")
        return doParser

    def do_build(self, args):
        try:
            # add arguments
            doParser = self.arg_build()
            try:
                doArgs = doParser.parse_args(shlex.split(args))
            except SystemExit as e:
                return
            # --
            file = generics_utils.get_file(doArgs.file)
            if file is None:
                return 2
            data = load_data(file)
            if "builders" in data:
                builders = hammr_utils.check_mandatory_builders(data["builders"])
                builders = hammr_utils.check_mandatory_generate_scan(builders)
            else:
                printer.out("no builder section found", printer.ERROR)
                return
            if builders is None:
                return
            try:
                myScannedInstances = self.api.Users(self.login).Scannedinstances.Getall(Includescans="true")
                if myScannedInstances is None or not hasattr(myScannedInstances, 'scannedInstances'):
                    printer.out("scan not found", printer.ERROR)
                    return
                else:
                    myScan = None
                    for myScannedInstance in myScannedInstances.scannedInstances.scannedInstance:
                        for scan in myScannedInstance.scans.scan:
                            if str(scan.dbId) == doArgs.id:
                                myScan = scan
                                myRScannedInstance = myScannedInstance
                                break
                        if myScan is not None:
                            break

                if myScan is not None and myScan.status.complete and not myScan.status.error and not myScan.status.cancelled:
                    i = 1
                    for builder in builders:
                        printer.out(
                            "Generating '" + builder["type"] + "' image (" + str(i) + "/" + str(len(builders)) + ")")
                        format_type = builder["type"]
                        targetFormat = generate_utils.get_target_format_object(self.api, self.login, format_type)

                        if targetFormat is None:
                            printer.out("Builder type unknown: "+format_type, printer.ERROR)
                            return 2
                        myimage = image()

                        myinstallProfile = installProfile()
                        if "swapSize" in builder["installation"]:
                            myinstallProfile.swapSize = builder["installation"]["swapSize"]
                        myinstallProfile.diskSize = builder["installation"]["diskSize"]


                        func = getattr(generate_utils, "generate_"+generics_utils.remove_special_chars(targetFormat.format.name), None)
                        if func:
                            myimage, myinstallProfile = func(myimage, builder, myinstallProfile, self.api, self.login)
                        else:
                            printer.out("Builder type unknown: "+format_type, printer.ERROR)
                            return 2

                        myimage.targetFormat = targetFormat
                        myimage.installProfile = myinstallProfile
                        rImage = self.api.Users(self.login).Scannedinstances(myRScannedInstance.dbId).Scans(
                            myScan.dbId).Images().Generate(myimage)
                        status = rImage.status
                        statusWidget = progressbar_widget.Status()
                        statusWidget.status = status
                        widgets = [Bar('>'), ' ', statusWidget, ' ', ReverseBar('<')]
                        progress = ProgressBar(widgets=widgets, maxval=100).start()
                        while not (status.complete or status.error or status.cancelled):
                            statusWidget.status = status
                            progress.update(status.percentage)
                            status = self.api.Users(self.login).Scannedinstances(myRScannedInstance.dbId).Scans(
                                myScan.dbId).Images(Sitid=rImage.dbId).Status.Get()
                            time.sleep(2)
                        statusWidget.status = status
                        progress.finish()
                        if status.error:
                            printer.out("Generation '" + builder[
                                "type"] + "' error: " + status.message + "\n" + status.errorMessage, printer.ERROR)
                            if status.detailedError:
                                printer.out(status.detailedErrorMsg)
                        elif status.cancelled:
                            printer.out("Generation '" + builder["type"] + "' canceled: " + status.message,
                                        printer.ERROR)
                        else:
                            printer.out("Generation '" + builder["type"] + "' ok", printer.OK)
                        i += 1
                else:
                    printer.out("Impossible to generate this scan", printer.ERROR)

            except KeyError as e:
                printer.out("unknown error template file", printer.ERROR)




        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_build()
        except KeyboardInterrupt:
            printer.out("\n")
            if generics_utils.query_yes_no("Do you want to cancel the job ?"):
                if 'myRScannedInstance' in locals() and 'myScan' in locals() and 'rImage' in locals() \
                        and hasattr(myRScannedInstance, 'dbId') and hasattr(myScan, 'dbId') and hasattr(rImage, 'dbId'):
                    self.api.Users(self.login).Scannedinstances(myRScannedInstance.dbId).Scans(myScan.dbId).Images(
                        Sitid=rImage.dbId).Status.Cancel()
            else:
                print "Exiting command"
        except Exception as e:
            return handle_uforge_exception(e)

    def help_build(self):
        doParser = self.arg_build()
        doParser.print_help()

    def arg_import(self):
        doParser = ArgumentParser(prog=self.cmd_name + " import", add_help=True,
                                  description="Imports (or transforms) the scan to a template")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--id', dest='id', required=True, help="the ID of the scan to import")
        mandatory.add_argument('--name', dest='name', required=True, nargs='+',
                               help="the name to use for the template created from the scan")
        mandatory.add_argument('--version', dest='version', required=True,
                               help="the version to use for the template created from the scan")
        return doParser

    def do_import(self, args):
        try:
            # add arguments
            doParser = self.arg_import()
            try:
                doArgs = doParser.parse_args(shlex.split(args))
                doArgs.name = " ".join(doArgs.name)
            except SystemExit as e:
                return

            printer.out("Import scan id [" + doArgs.id + "] ...")
            myScannedInstances = self.api.Users(self.login).Scannedinstances.Getall(Includescans="true")
            if myScannedInstances is None or not hasattr(myScannedInstances, 'scannedInstances'):
                printer.out("scan not found", printer.ERROR)
                return
            else:
                myScan = None
                for myScannedInstance in myScannedInstances.scannedInstances.scannedInstance:
                    for scan in myScannedInstance.scans.scan:
                        if str(scan.dbId) == doArgs.id:
                            myScan = scan
                            myRScannedInstance = myScannedInstance
                            break
                    if myScan is not None:
                        break

            if myScan is not None and myScan.status.complete and not myScan.status.error and not myScan.status.cancelled:
                myScanImport = scanImport()
                myScanImport.importedObjectName = doArgs.name
                myScanImport.importedObjectVersion = doArgs.version
                myScanImport.orgUri = (self.api.Users(self.login).Orgs().Getall()).orgs.org[0].uri
                rScanImport = self.api.Users(self.login).Scannedinstances(myRScannedInstance.dbId).Scans(
                    myScan.dbId).Imports().Import(myScanImport)
                status = rScanImport.status
                statusWidget = progressbar_widget.Status()
                statusWidget.status = status
                widgets = [Bar('>'), ' ', statusWidget, ' ', ReverseBar('<')]
                progress = ProgressBar(widgets=widgets, maxval=100).start()
                while not (status.complete or status.error or status.cancelled):
                    statusWidget.status = status
                    progress.update(status.percentage)
                    status = (self.api.Users(self.login).Scannedinstances(myRScannedInstance.dbId).Scans(
                        myScan.dbId).Imports().Status.Get(I=rScanImport.uri)).statuses.status[0]
                    time.sleep(2)
                statusWidget.status = status
                progress.finish()
                if status.error:
                    printer.out("Importing error: " + status.message + "\n" + status.errorMessage, printer.ERROR)
                    if status.detailedError:
                        printer.out(status.detailedErrorMsg)
                elif status.cancelled:
                    printer.out("Importing canceled: " + status.message, printer.WARNING)
                else:
                    printer.out("Importing ok", printer.OK)

        except KeyboardInterrupt:
            printer.out("\n")
            if generics_utils.query_yes_no("Do you want to cancel the job ?"):
                if 'myRScannedInstance' in locals() and 'myScan' in locals() and 'rScanImport' in locals() \
                        and hasattr(myRScannedInstance, 'dbId') and hasattr(myScan, 'dbId') and hasattr(rScanImport,
                                                                                                        'dbId'):
                    self.api.Users(self.login).Scannedinstances(myRScannedInstance.dbId).Scans(myScan.dbId).Imports(
                        rScanImport.dbId).Status.Cancel()
            else:
                printer.out("Exiting command")
        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_import()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_import(self):
        doParser = self.arg_import()
        doParser.print_help()

    def arg_delete(self):
        doParser = ArgumentParser(prog=self.cmd_name + " delete", add_help=True, description="Deletes an existing instance or scan")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--id', dest='id', required=True, help="the ID of the instance or scan to delete")
        optional = doParser.add_argument_group("optional arguments")
        optional.add_argument('--scantype', dest='scantype', required=False,
                              help="the scan type, values is [instance|scan|all] (default is scan)")
        optional.add_argument('--scansonly', dest='scansonly', required=False, action='store_true',
                              help="if scan type is instance, and this argument is used, will only remove the scans not the instance itself")
        return doParser

    def do_delete(self, args):
        try:
            doParser = self.arg_delete()
            try:
                doArgs = doParser.parse_args(shlex.split(args))
            except SystemExit as e:
                return
            # call UForge API
            searchedScanType = 'scan'
            extraInfo = "Retrieving scan with id [" + doArgs.id + "] ..."
            if doArgs.scantype:
                if doArgs.scantype != 'scan' and doArgs.scantype != 'instance' and doArgs.scantype != 'all':
                    printer.out(
                        "ERROR: scantype can only be 'scan', 'instance' or 'all' not: '" + doArgs.scantype + "'",
                        printer.ERROR)
                    return
                searchedScanType = doArgs.scantype
            if searchedScanType != 'instance' and doArgs.scansonly:
                printer.out(
                    "ERROR: 'scansonly' can only be used with 'instance' scantype but not with '" + searchedScanType + "'",
                    printer.ERROR)
                return
            if searchedScanType == 'instance':
                extraInfo = "Retrieving scan instance with id [" + doArgs.id + "] ..."
            else:
                if searchedScanType == 'all':
                    extraInfo = 'Retrieving all scan instances and associated scans'
            printer.out(extraInfo)
            myScannedInstances = self.api.Users(self.login).Scannedinstances.Getall(Includescans="true")
            myScannedInstances = myScannedInstances.scannedInstances.scannedInstance
            if myScannedInstances is None or len(myScannedInstances) == 0:
                printer.out("Nothing found")
                return
            if searchedScanType == 'all':
                print scan_utils.scan_table(myScannedInstances).draw() + "\n"
                if generics_utils.query_yes_no("Do you really want to delete all scan instances"):
                    printer.out("Please wait...")
                    self.api.Users(self.login).Scannedinstances().Deleteall()
                    printer.out("All instances and scans deleted", printer.OK)
                return
            for myScannedInstance in myScannedInstances:
                if searchedScanType == 'instance' and str(myScannedInstance.dbId) == doArgs.id:
                    print scan_utils.scan_table([myScannedInstance]).draw() + "\n"
                    if doArgs.scansonly:
                        extraInfo = "Do you really want to delete all scans in instance with id " + str(doArgs.id)
                    else:
                        extraInfo = "Do you really want to delete scan instance with id " + str(
                            doArgs.id) + " and all associated scans"
                    if generics_utils.query_yes_no(extraInfo):
                        printer.out("Please wait...")
                        if doArgs.scansonly:
                            self.api.Users(self.login).Scannedinstances(doArgs.id).Scans().Deleteall()
                            printer.out("Instance scans deleted", printer.OK)
                        else:
                            self.api.Users(self.login).Scannedinstances(doArgs.id).Delete()
                            printer.out("Instance deleted", printer.OK)
                        return
                    return
                if searchedScanType == 'scan':
                    for scan in myScannedInstance.scans.scan:
                        if str(scan.dbId) == doArgs.id:
                            print scan_utils.scan_table([myScannedInstance], scan).draw() + "\n"
                            if generics_utils.query_yes_no(
                                            "Do you really want to delete scan with id " + str(doArgs.id)):
                                printer.out("Please wait...")
                                self.api.Users(self.login).Scannedinstances(myScannedInstance.dbId).Scans(
                                    doArgs.id).Delete()
                                printer.out("Scan deleted", printer.OK)
                            return
            printer.out("Scan not found", printer.ERROR)
        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_delete()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_delete(self):
        doParser = self.arg_delete()
        doParser.print_help()

    def deploy_and_launch_agent(self, uforge_login, uforge_password, args, file_src_path, uforge_url):
        hostname = args.ip
        username = args.login
        if not args.password:
            passW = getpass.getpass('Password for %s@%s: ' % (username, hostname))
        else:
            passW = args.password
        if not args.port:
            port = 22
        else:
            port = int(args.port)

        # paramiko.util.log_to_file('/tmp/ssh.log') # sets up logging

        # get host key, if we know one
        hostkeytype = None
        hostkey = None
        try:
            host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
            try:
                # try ~/ssh/ too, because windows can't have a folder named ~/.ssh/
                host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
            except IOError:
                printer.out("Unable to open host keys file", printer.ERROR)
                host_keys = {}


        # if host_keys.has_key(hostname):
        #        hostkeytype = host_keys[hostname].keys()[0]
        #        hostkey = host_keys[hostname][hostkeytype]
        #        print 'Using host key of type %s' % hostkeytype

        # now, connect and use paramiko Transport to negotiate SSH2 across the connection
        try:
            if not args.dir:
                dir = "/tmp"
            else:
                dir = args.dir
            t = paramiko.Transport((hostname, port))
            t.connect(username=username, password=passW, hostkey=hostkey)
            sftp = paramiko.SFTPClient.from_transport(t)

            # upload uforge scan binary
            sftp.put(file_src_path, dir + "/" + constants.SCAN_BINARY_NAME)
            t.close()

            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
            client.connect(hostname, port, username, passW)

            # test service
            stdin, stdout, stderr = client.exec_command(
                'chmod +x ' + dir + '/' + constants.SCAN_BINARY_NAME + '; ' + dir + '/' + constants.SCAN_BINARY_NAME + ' -u ' + uforge_login + ' -p ' + uforge_password + ' -U ' + uforge_url + ' -P')
            for line in stdout:
                print '... ' + line.strip('\n')
            # launch scan
            exclude = ""
            if args.exclude:
                for ex in args.exclude:
                    exclude += "-e " + ex + " "
            overlay = ""
            if args.overlay:
                overlay = "-o"
            client.exec_command(
                'chmod +x ' + dir + '/' + constants.SCAN_BINARY_NAME + '; nohup ' + dir + '/' + constants.SCAN_BINARY_NAME + ' -u ' + uforge_login + ' -p ' + uforge_password + ' -U ' + uforge_url + ' ' + overlay + ' -n \'' + args.name + '\' ' + exclude + ' >/dev/null 2>&1 &')
            client.close()

        except paramiko.AuthenticationException as e:
            printer.out("Authentification error: " + e[0], printer.ERROR)
            return 2
        except Exception, e:
            printer.out("Caught exception: " + str(e), printer.ERROR)
            # traceback.print_exc()
            try:
                t.close()
                client.close()
            except:
                pass
            return 2

        return 0