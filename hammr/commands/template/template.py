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

import time
import tarfile
import os.path
import ntpath
import shutil
import shlex
from junit_xml import TestSuite, TestCase

from texttable import Texttable
from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer
from uforge.objects.uforge import *
from ussclicore.utils import generics_utils, printer, progressbar_widget
from hammr.utils.hammr_utils import *
from hammr.utils.bundle_utils import *
from hammr.utils import constants
from hammr.utils import generate_utils
from os.path import realpath


class Template(Cmd, CoreGlobal):
    """Create a template based on your configuration file. List, delete, clone or export/import existing templates. Generate an image from your configuration file. Validate your configuration file before building your template"""

    cmd_name="template"

    def __init__(self):
        super(Template, self).__init__()

    def arg_list(self):
        doParser = ArgumentParser(prog=self.cmd_name+" list", add_help = True, description="Displays all the created templates")
        return doParser

    def do_list(self, args):
        try:
            #call UForge API
            printer.out("Getting templates for ["+self.login+"] ...")
            appliances = self.api.Users(self.login).Appliances().Getall()
            appliances = appliances.appliances
            if appliances is None or not hasattr(appliances, 'appliance'):
                printer.out("No template")
            else:
                images = self.api.Users(self.login).Images.Getall()
                images = images.images
                table = Texttable(800)
                table.set_cols_dtype(["t","t","t","t","t","t","t","t","t","t"])
                table.header(["Id", "Name", "Version", "OS", "Created", "Last modified", "# Imgs", "Updates", "Imp", "Shared"])
                appliances = generics_utils.order_list_object_by(appliances.appliance, "name")
                for appliance in appliances:
                    nbImage=0
                    if images is not None and hasattr(images, 'image'):
                        for image in images.image:
                            if hasattr(image, 'applianceUri') and image.applianceUri == appliance.uri:
                                nbImage+=1
                    table.add_row([appliance.dbId, appliance.name, str(appliance.version), appliance.distributionName+" "+appliance.archName,
                                   appliance.created.strftime("%Y-%m-%d %H:%M:%S"), appliance.lastModified.strftime("%Y-%m-%d %H:%M:%S"), nbImage, appliance.nbUpdates, "X" if appliance.imported else "", "X" if appliance.shared else ""])
                print table.draw() + "\n"
                printer.out("Found "+str(len(appliances))+" templates")
            return 0
        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
            self.help_list()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_list(self):
        doParser = self.arg_list()
        doParser.print_help()

    def arg_export(self):
        doParser = ArgumentParser(prog=self.cmd_name+" export", add_help = True, description="Exports a template by creating an archive (compressed tar file) that includes the template configuration file")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--id', dest='id', required=True, help="the ID of the template to export")
        optional = doParser.add_argument_group("optional arguments")
        optional.add_argument('--file', dest='file', required=False, help="destination path where to store the template configuration file on the local filesystem")
        optional.add_argument('--outputFormat', dest='output_format', required=False, help="output format (yaml or json) of the template file to export (yaml is the default one)")
        return doParser

    def do_export(self, args):
        try:
            #add arguments
            doParser = self.arg_export()
            doArgs = doParser.parse_args(shlex.split(args))

            #if the help command is called, parse_args returns None object
            if not doArgs:
                    return 2

            #call UForge API
            printer.out("Exporting template with id ["+doArgs.id+"] :")
            myAppliance = self.api.Users(self.login).Appliances(doArgs.id).Get()
            if myAppliance is None or type(myAppliance) is not Appliance:
                printer.out("No template")
            else:
                output_format="yaml"
                if doArgs.output_format is not None:
                    output_format=doArgs.output_format

                applianceExport = self.api.Users(self.login).Appliances(myAppliance.dbId).Exports().Export(output_format)
                status = applianceExport.status
                progress = ProgressBar(widgets=[Percentage(), Bar()], maxval=100).start()
                while not (status.complete or status.error):
                    progress.update(status.percentage)
                    status = self.api.Users(self.login).Appliances(myAppliance.dbId).Exports(applianceExport.dbId).Status.Get()
                    time.sleep(2)
                progress.finish()
                if status.error:
                    printer.out("Export error: "+status.message+"\n"+status.errorMessage, printer.ERROR)
                    if status.detailedError:
                        printer.out(status.detailedErrorMsg)
                else:
                    printer.out("Downloading archive...")
                    if doArgs.file is None:
                        file = open("archive.tar.gz", "w")
                    else:
                        file = open(doArgs.file, "w")
                    self.api.Users(self.login).Appliances(myAppliance.dbId).Exports(applianceExport.dbId).Downloads.Download(streamingResponseFile=file)
                    file.close()

                    #Delete export archive on the server
                    self.api.Users(self.login).Appliances(myAppliance.dbId).Exports(applianceExport.dbId).Delete()

                    printer.out("Download complete of file ["+file.name+"]", printer.OK)
            return 0
        except IOError as e:
            printer.out("File error: "+str(e), printer.ERROR)
        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
            self.help_export()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_export(self):
        doParser = self.arg_export()
        doParser.print_help()


    def arg_import(self):
        doParser = ArgumentParser(prog=self.cmd_name+" import", add_help = True, description="Creates a template from an archive")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--file', dest='file', required=True, help="the path of the archive")
        optional = doParser.add_argument_group("optional arguments")
        optional.add_argument('-f', '--force', dest='force', action='store_true', help='force template creation (delete template/bundle if already exist)', required = False)
        optional.add_argument('-r', '--rbundles', dest='rbundles', action='store_true', help='if a bundle already exists, use it in the new template. Warning: this option ignore the content of the bundle described in the template file', required = False)
        optional.add_argument('--usemajor', dest='use_major', action='store_true', help='use distribution major version if exit', required = False)
        optional.set_defaults(force=False)
        optional.set_defaults(use_major=False)
        return doParser

    def do_import(self, args):
        try:
            #add arguments
            doParser = self.arg_import()
            doArgs = doParser.parse_args(shlex.split(args))

            #if the help command is called, parse_args returns None object
            if not doArgs:
                    return 2

            #call UForge API
            return self.import_stack(doArgs.file, True, doArgs.force, doArgs.rbundles, doArgs.use_major)
        except ArgumentParserError as e:
            printer.out("In Arguments: "+str(e)+"\n", printer.ERROR)
            self.help_import()
        except Exception as e:
            return handle_uforge_exception(e)


    def help_import(self):
        doParser = self.arg_import()
        doParser.print_help()


    def arg_validate(self):
        doParser = ArgumentParser(prog=self.cmd_name+" validate", add_help = True, description="Validates the syntax of a template configuration file")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--file', dest='file', required=True, help="the yaml/json template configuration file")
        return doParser

    def do_validate(self, args):
        try:
            #add arguments
            doParser = self.arg_validate()
            doArgs = doParser.parse_args(shlex.split(args))

            #if the help command is called, parse_args returns None object
            if not doArgs:
                    return 2

            file = generics_utils.get_file(doArgs.file)
            if file is None:
                return 2
            template=validate(file)
            if template is None:
                return 2
            print "OK : Syntax of template file [" + realpath(file) + "] is ok"
            return 0
        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
            self.help_validate()

    def help_validate(self):
        doParser = self.arg_validate()
        doParser.print_help()


    def arg_create(self):
        doParser = ArgumentParser(prog=self.cmd_name+" create", add_help = True, description="Create a new template and save to the UForge server")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--file', dest='file', required=True, help="yaml/json file containing the template content")
        optional = doParser.add_argument_group("optional arguments")
        optional.add_argument('--archive-path', dest='archive_path', required=False, help="path of where to store the archive of the created template. If provided hammr, creates an archive of the created template, equivalent to running template export")
        optional.add_argument('-f', '--force', dest='force', action='store_true', help='force template creation (delete template/bundle if already exist)', required = False)
        optional.add_argument('-r', '--rbundles', dest='rbundles', action='store_true', help='if a bundle already exists, use it in the new template. Warning: this option ignore the content of the bundle described in the template file', required = False)
        optional.add_argument('--usemajor', dest='use_major', action='store_true', help='use distribution major version if exit', required = False)
        optional.set_defaults(force=False)
        optional.set_defaults(use_major=False)
        return doParser

    def do_create(self, args):
        try:
            #add arguments
            doParser = self.arg_create()
            doArgs = doParser.parse_args(shlex.split(args))

            #if the help command is called, parse_args returns None object
            if not doArgs:
                    return 2

            #--
            #get file (remote or local)
            file = generics_utils.get_file(doArgs.file)
            if file is None:
                return 2
            #validate parsing and mandatory fields
            template = validate(file)
            if template is None:
                return 2
            isJsonFile= check_extension_is_json(file)

            if "builders" in template:
                template["builders"]=None
            archive_files=[]
            if "config" in template["stack"]:
                for config in template["stack"]["config"]:
                    #add to list of file to tar
                    if "source" in config:
                        file_tar_path=constants.FOLDER_CONFIGS + os.sep + generics_utils.remove_URI_forbidden_char(ntpath.basename(config["source"]))
                        archive_files.append([file_tar_path,config["source"]])
                        #changing source path to archive related source path
                        config["source"]=file_tar_path
                    else:
                        printer.out("No source file found in config", printer.ERROR)
                        return 2
            try:
                checkList = []
                if "bundles" in template["stack"]:
                    for bundle in template["stack"]["bundles"]:
                        if "files" in bundle:
                            for files in bundle["files"]:
                                checkList,archive_files = recursivelyAppendToArchive(bundle, files, "", checkList, archive_files)
                        else:
                            printer.out("No files section found for bundle", printer.ERROR)
                            return 2
                        if "license" in bundle and "source" in bundle["license"]:
                            #add to list of file to tar
                            file_tar_path=constants.FOLDER_BUNDLES + os.sep + generics_utils.remove_URI_forbidden_char(bundle["name"]) + os.sep + generics_utils.remove_URI_forbidden_char(ntpath.basename(bundle["license"]["source"]))
                            archive_files.append([file_tar_path,bundle["license"]["source"]])
                            #changing source path to archive related source path
                            bundle["license"]["source"]=file_tar_path
                        if "sourceLogo" in bundle:
                            #add to list of file to tar
                            file_tar_path=constants.FOLDER_BUNDLES + os.sep + generics_utils.remove_URI_forbidden_char(bundle["name"]) + os.sep + generics_utils.remove_URI_forbidden_char(ntpath.basename(bundle["sourceLogo"]))
                            archive_files.append([file_tar_path,bundle["sourceLogo"]])
                            #changing source path to archive related source path
                            bundle["sourceLogo"]=file_tar_path
            except KeyError as e:
                printer.out("Error in bundle", printer.ERROR)
                return 2
            if "source_logo" in template["stack"]:
                #add to list of file to tar
                file_tar_path=constants.FOLDER_LOGO + os.sep + generics_utils.remove_URI_forbidden_char(ntpath.basename(template["stack"]["source_logo"]))
                archive_files.append([file_tar_path,template["stack"]["source_logo"]])
                #changing source path to archive related source path
                template["stack"]["source_logo"]=file_tar_path

            if os.path.isdir(constants.TMP_WORKING_DIR):
                #delete tmp dir
                shutil.rmtree(constants.TMP_WORKING_DIR)
            os.mkdir(constants.TMP_WORKING_DIR)

            if isJsonFile:
                fileName = constants.TEMPLATE_JSON_FILE_NAME
                newFileName = constants.TEMPLATE_JSON_NEW_FILE_NAME
            else:
                fileName = constants.TEMPLATE_YAML_FILE_NAME
                newFileName = constants.TEMPLATE_YAML_NEW_FILE_NAME

            archive_files = dump_data_in_file(template, archive_files, isJsonFile, fileName, newFileName)

            if doArgs.archive_path is not None:
                tar_path = doArgs.archive_path
            else:
                tar_path = constants.TMP_WORKING_DIR+os.sep+"archive.tar.gz"
            tar = tarfile.open(tar_path, "w|gz")
            for file_tar_path,file_global_path in archive_files:
                if not os.path.isdir(file_global_path):
                    file = generics_utils.get_file(file_global_path, constants.TMP_WORKING_DIR+os.sep+os.path.basename(file_global_path))
                    if file is None:
                        printer.out("Downloaded bunlde file not found", printer.ERROR)
                        return 2
                    tar.add(file, arcname=file_tar_path)
                else:
                    tar.add(file_global_path, arcname=file_tar_path)
            tar.close()

            #arhive is created, doing import
            r = self.import_stack(tar_path, False, doArgs.force, doArgs.rbundles, doArgs.use_major)
            if r != 0:
                return r

            #delete tmp dir
            shutil.rmtree(constants.TMP_WORKING_DIR)
            return 0
        except OSError as e:
            printer.out("OSError: "+str(e), printer.ERROR)
        except IOError as e:
            printer.out("File error: "+str(e), printer.ERROR)
        except ArgumentParserError as e:
            printer.out("In Arguments: "+str(e), printer.ERROR)
            self.help_create()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_create(self):
        doParser = self.arg_create()
        doParser.print_help()


    def arg_build(self):
        doParser = ArgumentParser(prog=self.cmd_name+" build", add_help = True, description="Builds a machine image from the template")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--file', dest='file', required=True, help="yaml/json file providing the builder parameters")
        optional = doParser.add_argument_group("optional arguments")
        optional.add_argument('--id',dest='id',required=False, help="id of the template to build")
        optional.add_argument('--junit',dest='junit',required=False, help="name of junit XML output file")
        optional.add_argument('--simulate', dest='simulated', action='store_true', help='Simulate the generation (only the Checking Dependencies process will be executed)', required = False)
        optional.add_argument('--force', dest='forced', action='store_true', help='Force the checking dependencies', required = False)
        return doParser

    def do_build(self, args):
        try:
            #add arguments
            doParser = self.arg_build()
            doArgs = doParser.parse_args(shlex.split(args))

            #if the help command is called, parse_args returns None object
            if not doArgs:
                    return 2

            #--
            template=validate(doArgs.file)
            if template is None:
                return 2

            if doArgs.id:
                myAppliance = self.api.Users(self.login).Appliances().Getall(Query="dbId=="+doArgs.id)
                myAppliance = myAppliance.appliances.appliance
            else:
                #Get template which correpond to the template file
                myAppliance = self.api.Users(self.login).Appliances().Getall(Query="name=='"+template["stack"]["name"]+"';version=='"+template["stack"]["version"]+"'")
                myAppliance = myAppliance.appliances.appliance
            if myAppliance is None or len(myAppliance)!=1:
                printer.out("No template found on the plateform")
                return 0
            myAppliance=myAppliance[0]
            rInstallProfile = self.api.Users(self.login).Appliances(myAppliance.dbId).Installprofile("").Getdeprecated()
            if rInstallProfile is None:
                printer.out("No installation found on the template '"+template["stack"]["name"]+"'", printer.ERROR)
                return 0
            try:
                i=1
                if doArgs.junit is not None:
                    test_results=[]
                for builder in template["builders"]:
                    try:
                        printer.out("Generating '"+builder["type"]+"' image ("+str(i)+"/"+str(len(template["builders"]))+")")
                        if doArgs.junit is not None:
                            test = TestCase('Generation '+builder["type"])
                            test_results.append(test)
                            start_time = time.time()

                        format_type = builder["type"]
                        targetFormat = generate_utils.get_target_format_object(self.api, self.login, format_type)
                        if targetFormat is None:
                            printer.out("Builder type unknown: "+format_type, printer.ERROR)
                            return 2

                        myimage = image()
                        myinstallProfile = installProfile()
                        if rInstallProfile.partitionAuto:
                            if "installation" in builder:
                                if "swapSize" in builder["installation"]:
                                    myinstallProfile.swapSize = builder["installation"]["swapSize"]
                                if "diskSize" in builder["installation"]:
                                    myinstallProfile.diskSize = builder["installation"]["diskSize"]
                            else:
                                myinstallProfile.swapSize = rInstallProfile.swapSize
                                myinstallProfile.diskSize = rInstallProfile.partitionTable.disks.disk[0].size

                        func = getattr(generate_utils, "generate_"+generics_utils.remove_special_chars(targetFormat.format.name), None)
                        if func:
                            myimage,myinstallProfile = func(myimage, builder, myinstallProfile, self.api, self.login)
                        else:
                            printer.out("Builder type unknown: "+format_type, printer.ERROR)
                            return 2


                        if myimage is None:
                            return 2

                        myimage.targetFormat = targetFormat
                        myimage.installProfile = myinstallProfile
                        if doArgs.simulated is not None and doArgs.simulated:
                            myimage.simulated=True
                        if doArgs.forced is not None and doArgs.forced:
                            myimage.forceCheckingDeps=True

                        rImage = self.api.Users(self.login).Appliances(myAppliance.dbId).Images().Generate(myimage)

                        status = rImage.status
                        statusWidget = progressbar_widget.Status()
                        statusWidget.status = status
                        widgets = [Bar('>'), ' ', statusWidget, ' ', ReverseBar('<')]
                        progress = ProgressBar(widgets=widgets, maxval=100).start()
                        while not (status.complete or status.error or status.cancelled):
                            statusWidget.status = status
                            progress.update(status.percentage)
                            status = self.api.Users(self.login).Appliances(myAppliance.dbId).Images(rImage.dbId).Status.Get()
                            time.sleep(2)
                        statusWidget.status = status
                        progress.finish()
                        if status.error:
                            printer.out("Generation '"+builder["type"]+"' error: "+status.message+"\n"+status.errorMessage, printer.ERROR)
                            if status.detailedError:
                                printer.out(status.detailedErrorMsg)
                            if doArgs.junit is not None:
                                test.elapsed_sec=time.time() - start_time
                                test.add_error_info("Error", status.message+"\n"+status.errorMessage)
                        elif status.cancelled:
                            printer.out("Generation '"+builder["type"]+"' canceled: "+status.message, printer.WARNING)
                            if doArgs.junit is not None:
                                test.elapsed_sec=time.time() - start_time
                                test.add_failure_info("Canceled", status.message)
                        else:
                            printer.out("Generation '"+builder["type"]+"' ok", printer.OK)
                            printer.out("Image URI: "+rImage.uri)
                            printer.out("Image Id : "+generics_utils.extract_id(rImage.uri))
                            if doArgs.junit is not None:
                                test.elapsed_sec=time.time() - start_time
                                #the downloadUri already contains downloadKey at the end
                                if rImage.downloadUri is not None:
                                    test.stdout=self.api._url+"/"+rImage.downloadUri
                        i+=1
                    except Exception as e:
                        if  is_uforge_exception(e):
                            print_uforge_exception(e)
                            if doArgs.junit is not None and "test_results" in locals() and len(test_results)>0:
                                test=test_results[len(test_results)-1]
                                test.elapsed_sec=time.time() - start_time
                                test.add_error_info("Error", get_uforge_exception(e))
                        else:
                            raise
                if doArgs.junit is not None:
                    testName = myAppliance.distributionName+" "+myAppliance.archName
                    ts = TestSuite("Generation "+testName, test_results)
                    with open(doArgs.junit, 'w') as f:
                        TestSuite.to_file(f, [ts], prettyprint=False)
                return 0
            except KeyError as e:
                printer.out("unknown error in template file", printer.ERROR)

        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
            self.help_build()
        except KeyboardInterrupt:
            printer.out("\n")
            if generics_utils.query_yes_no("Do you want to cancel the job ?"):
                if 'myAppliance' in locals() and 'rImage' in locals() and hasattr(myAppliance, 'dbId') and hasattr(rImage, 'dbId'):
                    self.api.Users(self.login).Appliances(myAppliance.dbId).Images(rImage.dbId).Status.Cancel()
                else:
                    printer.out("Impossible to cancel", printer.WARNING)
            else:
                printer.out("Exiting command")
        except Exception as e:
            print_uforge_exception(e)
            if doArgs.junit is not None and "test_results" in locals() and len(test_results)>0:
                test=test_results[len(test_results)-1]
                if "start_time" in locals():
                    elapse=time.time() - start_time
                else:
                    elapse=0
                test.elapsed_sec=elapse
                test.add_error_info("Error", get_uforge_exception(e))
            else:
                return 2
        finally:
            if "doArgs" in locals() and doArgs.junit is not None and "test_results" in locals() and len(test_results)>0:
                if "myAppliance" in locals():
                    testName = myAppliance.distributionName+" "+myAppliance.archName
                else:
                    testName = ""
                ts = TestSuite("Generation "+testName, test_results)
                with open(doArgs.junit, 'w') as f:
                    TestSuite.to_file(f, [ts], prettyprint=False)


    def help_build(self):
        doParser = self.arg_build()
        doParser.print_help()



    def import_stack(self, file, isImport, isForce, rbundles, isUseMajor):
        try:
            if isImport:
                printer.out("Importing template from ["+file+"] archive ...")
            else:
                if constants.TMP_WORKING_DIR in str(file):
                    printer.out("Creating template from temporary ["+file+"] archive ...")
                else:
                    printer.out("Creating template from ["+file+"] archive ...")
            file = open(file, "r")

            # The following code could not be used for the moment
            # appImport = applianceImport()
            # appImport.imported = isImport
            # appImport.forceRw = isForce
            # appImport.reuseBundles = rbundles
            # appImport.useMajor = isUseMajor
            # appImport = self.api.Users(self.login).Imports.Import(appImport)

            appImport = self.api.Users(self.login).Imports.Import(Imported=isImport, Force=isForce, Reusebundles=rbundles, Usemajor=isUseMajor)
            if appImport is None:
                if isImport:
                    printer.out("error importing appliance", printer.ERROR)
                else:
                    printer.out("error creating appliance", printer.ERROR)
                return 2
            else:
                status = self.api.Users(self.login).Imports(appImport.dbId).Uploads.Upload(file)
                progress = ProgressBar(widgets=[Percentage(), Bar()], maxval=100).start()
                while not (status.complete or status.error):
                    progress.update(status.percentage)
                    status = self.api.Users(self.login).Imports(appImport.dbId).Status.Get()
                    time.sleep(2)
                progress.finish()
                if status.error:
                    if isImport:
                        printer.out("Template import: "+status.message+"\n"+status.errorMessage, printer.ERROR)
                        if status.detailedError:
                            printer.out(status.detailedErrorMsg)
                    else:
                        printer.out("Template create: "+status.message+"\n"+status.errorMessage, printer.ERROR)
                else:
                    if isImport:
                        printer.out("Template import: DONE", printer.OK)
                    else:
                        printer.out("Template create: DONE", printer.OK)

                    #get appliance import
                    appImport = self.api.Users(self.login).Imports(appImport.dbId).Get()
                    printer.out("Template URI: "+appImport.referenceUri)
                    printer.out("Template Id : "+generics_utils.extract_id(appImport.referenceUri))

                return 0
        except IOError as e:
            printer.out("File error: "+str(e), printer.ERROR)
            return 2
        except Exception as e:
            return handle_uforge_exception(e)


    def arg_delete(self):
        doParser = ArgumentParser(prog=self.cmd_name+" delete", add_help = True, description="Deletes an existing template")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--id', dest='id', required=True, help="the ID of the template to delete")
        optional = doParser.add_argument_group("optional arguments")
        optional.add_argument('--no-confirm',dest='no_confirm',action='store_true', required=False, help="do not print confirmation dialog")
        optional.set_defaults(no_confirm=False)
        return doParser


    def do_delete(self, args):
        try:
            #add arguments
            doParser = self.arg_delete()
            doArgs = doParser.parse_args(shlex.split(args))

            #if the help command is called, parse_args returns None object
            if not doArgs:
                    return 2

            #call UForge API
            printer.out("Searching template with id ["+doArgs.id+"] ...")
            myAppliance = self.api.Users(self.login).Appliances(doArgs.id).Get()
            if myAppliance is None or type(myAppliance) is not Appliance:
                printer.out("Template not found")
            else:
                table = Texttable(800)
                table.set_cols_dtype(["t","t","t","t","t","t","t","t","t","t"])
                table.header(["Id", "Name", "Version", "OS", "Created", "Last modified", "# Imgs", "Updates", "Imp", "Shared"])
                table.add_row([myAppliance.dbId, myAppliance.name, str(myAppliance.version), myAppliance.distributionName+" "+myAppliance.archName,
                               myAppliance.created.strftime("%Y-%m-%d %H:%M:%S"), myAppliance.lastModified.strftime("%Y-%m-%d %H:%M:%S"), len(myAppliance.imageUris.uri),myAppliance.nbUpdates, "X" if myAppliance.imported else "", "X" if myAppliance.shared else ""])
                print table.draw() + "\n"

                if doArgs.no_confirm:
                    self.api.Users(self.login).Appliances(myAppliance.dbId).Delete()
                    printer.out("Template deleted", printer.OK)
                elif generics_utils.query_yes_no("Do you really want to delete template with id "+str(myAppliance.dbId)):
                    self.api.Users(self.login).Appliances(myAppliance.dbId).Delete()
                    printer.out("Template deleted", printer.OK)
            return 0
        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
            self.help_delete()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_delete(self):
        doParser = self.arg_delete()
        doParser.print_help()


    def arg_clone(self):
        doParser = ArgumentParser(prog=self.cmd_name+" clone", add_help = True, description="Clones the template. The clone is copying the meta-data of the template")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--id', dest='id', required=True, help="the ID of the template to clone")
        mandatory.add_argument('--name', dest='name', required=True, help="the name to use for the new cloned template")
        mandatory.add_argument('--version', dest='version', required=True, help="the version to use for the cloned template")
        return doParser


    def do_clone(self, args):
        try:
            #add arguments
            doParser = self.arg_clone()
            doArgs = doParser.parse_args(shlex.split(args))

            #if the help command is called, parse_args returns None object
            if not doArgs:
                    return 2

            #call UForge API
            printer.out("Clonnig template with id ["+doArgs.id+"] ...")
            myAppliance = appliance()
            myAppliance.name = doArgs.name
            myAppliance.version = doArgs.version
            rAppliance = self.clone_appliance(doArgs.id, myAppliance)
            if type(rAppliance) is Appliance:
                printer.out("Clonned successfully", printer.OK)
            else:
                printer.out("Clone error", printer.ERROR)
        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
            self.help_clone()
        except Exception as e:
            return handle_uforge_exception(e)

    def clone_appliance(self, id, appliance):
        return self.api.Users(self.login).Appliances(id).Clones.Clone(appliance)

    def help_clone(self):
        doParser = self.arg_clone()
        doParser.print_help()
