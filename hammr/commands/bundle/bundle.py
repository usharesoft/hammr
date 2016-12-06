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

import time
import os.path
import ntpath
import tarfile
import shutil

from texttable import Texttable
from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from ussclicore.utils import generics_utils, printer
from progressbar import Bar, Percentage, ProgressBar
from hammr.utils.hammr_utils import *
from hammr.utils.bundle_utils import *
from hammr.utils import constants
from uforge.objects.uforge import *
from hurry.filesize import size
from os.path import realpath

class Bundle(Cmd, CoreGlobal):
    """Create a bundle (mysoftware) on UForge based on your configuration file. List, delete, clone or export/import existing bundles. Validate your configuration file before creating your bundle"""

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
                table.set_cols_dtype(["t","t","t", "t","t","t","t"])
                table.header(["Id", "Name", "Version", "Description", "Category", "Size", "Imported"])
                bundles = generics_utils.order_list_object_by(bundles, "name")
                for bundle in bundles:
                    category = ""
                    if bundle.category is not None:
                        category = bundle.category.name
                    table.add_row([bundle.dbId, bundle.name, bundle.version, bundle.description, category, size(bundle.size), "X" if bundle.imported else ""])
                print table.draw() + "\n"
                printer.out("Found "+str(len(bundles))+" bundles")

            return 0
        except Exception as e:
            return handle_uforge_exception(e)

    def help_list(self):
        doParser = self.arg_list()
        doParser.print_help()


    def arg_export(self):
        doParser = ArgumentParser(prog=self.cmd_name+" export", add_help = True, description="Exports a bundle by creating an archive (compressed tar file) that includes the bundle configuration file")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--id', dest='id', required=True, help="the ID of the bundle to export")
        optional = doParser.add_argument_group("optional arguments")
        optional.add_argument('--file', dest='file', required=False, help="destination path where to store the bundle configuration file on the local filesystem")
        optional.add_argument('--outputFormat', dest='output_format', required=False, help="output format (yaml or json) of the bundle file to export (yaml is the default one)")
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
            printer.out("Exporting bundle with id ["+doArgs.id+"] :")
            mySoftware = self.api.Users(self.login).Mysoftware(doArgs.id).Get()
            if mySoftware is None or type(mySoftware) is not MySoftware:
                printer.out("No bundle")
            else:
                output_format="yaml"
                if doArgs.output_format is not None:
                   output_format=doArgs.output_format
                mySoftwareExport = self.api.Users(self.login).Mysoftware(mySoftware.dbId).Exports().Export(output_format)
                status = mySoftwareExport.status
                progress = ProgressBar(widgets=[Percentage(), Bar()], maxval=100).start()
                while not (status.complete or status.error):
                    progress.update(status.percentage)
                    status = self.api.Users(self.login).Mysoftware(mySoftware.dbId).Exports(mySoftwareExport.dbId).Status.Get()
                    time.sleep(2)
                progress.finish()
                if status.error:
                    printer.out("Export error: "+status.message+"\n"+status.errorMessage, printer.ERROR)
                    if status.detailedError:
                        printer.out(status.detailedErrorMsg)
                else:
                    printer.out("Downloading archive...")
                    if doArgs.file is None:
                        file = open(mySoftware.name+".tar.gz", "w")
                    else:
                        file = open(doArgs.file, "w")
                    self.api.Users(self.login).Mysoftware(mySoftware.dbId).Exports(mySoftwareExport.dbId).Downloads.Download(streamingResponseFile=file)
                    file.close()

                    #Delete export archive on the server
                    self.api.Users(self.login).Mysoftware(mySoftware.dbId).Exports(mySoftwareExport.dbId).Delete()

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
        doParser = ArgumentParser(prog=self.cmd_name+" import", add_help = True, description="Creates a bundle from an archive")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--file', dest='file', required=True, help="the path of the archive")
        optional = doParser.add_argument_group("optional arguments")
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
            return self.import_bundle(doArgs.file, True)
        except ArgumentParserError as e:
            printer.out("In Arguments: "+str(e)+"\n", printer.ERROR)
            self.help_import()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_import(self):
        doParser = self.arg_import()
        doParser.print_help()


    def arg_validate(self):
        doParser = ArgumentParser(prog=self.cmd_name+" validate", add_help = True, description="Validates the syntax of a bundle configuration file")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--file', dest='file', required=True, help="the yaml/json bundle configuration file")
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
            bundle=validate_bundle(file)
            if bundle is None:
                return 2
            print "OK : Syntax of bundle file [" + realpath(file) + "] is ok"
            return 0
        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
            self.help_validate()

    def help_validate(self):
        doParser = self.arg_validate()
        doParser.print_help()


    def arg_create(self):
        doParser = ArgumentParser(prog=self.cmd_name+" create", add_help = True, description="Create a new bundle and save to the UForge server")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--file', dest='file', required=True, help="yaml/json file containing the bundle content")
        optional = doParser.add_argument_group("optional arguments")
        optional.add_argument('--archive-path', dest='archive_path', required=False, help="path of where to store the archive of the created bundle. If provided hammr, creates an archive of the created bundle, equivalent to running bundle export")
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

            bundle = validate_bundle(file)
            if bundle is None:
                return 2
            isJsonFile= check_extension_is_json(file)
            archive_files=[]
            try:
                checkList = []
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

            if os.path.isdir(constants.TMP_WORKING_DIR):
                #delete tmp dir
                shutil.rmtree(constants.TMP_WORKING_DIR)
            os.mkdir(constants.TMP_WORKING_DIR)

            if isJsonFile:
                fileName = constants.BUNDLE_JSON_FILE_NAME
                newFileName = constants.BUNDLE_JSON_NEW_FILE_NAME
            else:
                fileName = constants.BUNDLE_YAML_FILE_NAME
                newFileName = constants.BUNDLE_YAML_NEW_FILE_NAME

            archive_files = dump_data_in_file(bundle, archive_files, isJsonFile, fileName, newFileName)

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
            r = self.import_bundle(tar_path, False)
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


    def import_bundle(self, file, isImport):
        try:
            if isImport:
                printer.out("Importing bundle from ["+file+"] archive ...")
            else:
                if constants.TMP_WORKING_DIR in str(file):
                    printer.out("Creating bundle from temporary ["+file+"] archive ...")
                else:
                    printer.out("Creating bundle from ["+file+"] archive ...")
            file = open(file, "r")

            bundleImport = self.api.Users(self.login).Bundleimports.Import(Imported=isImport)

            if bundleImport is None:
                if isImport:
                    printer.out("error importing bundle", printer.ERROR)
                else:
                    printer.out("error creating bundle", printer.ERROR)
                return 2
            else:
                status = self.api.Users(self.login).Bundleimports(bundleImport.dbId).Uploads.Upload(file)
                progress = ProgressBar(widgets=[Percentage(), Bar()], maxval=100).start()
                while not (status.complete or status.error):
                    progress.update(status.percentage)
                    status = self.api.Users(self.login).Bundleimports(bundleImport.dbId).Status.Get()
                    time.sleep(2)
                progress.finish()
                if status.error:
                    if isImport:
                        printer.out("Bundle import: "+status.message+"\n"+status.errorMessage, printer.ERROR)
                        if status.detailedError:
                            printer.out(status.detailedErrorMsg)
                    else:
                        printer.out("Bundle create: "+status.message+"\n"+status.errorMessage, printer.ERROR)
                else:
                    if isImport:
                        printer.out("Bundle import: DONE", printer.OK)
                    else:
                        printer.out("Bundle create: DONE", printer.OK)

                    #get bundle import
                    bundleImport = self.api.Users(self.login).Bundleimports(bundleImport.dbId).Get()
                    printer.out("Bundle URI: "+bundleImport.referenceUri)
                    printer.out("Bundle Id : "+generics_utils.extract_id(bundleImport.referenceUri))

                return 0
        except IOError as e:
            printer.out("File error: "+str(e), printer.ERROR)
            return 2
        except Exception as e:
            return handle_uforge_exception(e)


    def arg_delete(self):
        doParser = ArgumentParser(prog=self.cmd_name+" delete", add_help = True, description="Deletes an existing bundle")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--id', dest='id', required=True, help="the ID of the bundle to delete")
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


    def arg_clone(self):
        doParser = ArgumentParser(prog=self.cmd_name+" clone", add_help = True, description="Clones the bundle. The clone is copying the meta-data of the bundle")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--id', dest='id', required=True, help="the ID of the bundle to clone")
        mandatory.add_argument('--name', dest='name', required=True, help="the name to use for the new cloned bundle")
        mandatory.add_argument('--version', dest='version', required=True, help="the version to use for the cloned bundle")
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
            printer.out("Clonnig bundle with id ["+doArgs.id+"] ...")
            software = mySoftware()
            software.name = doArgs.name
            software.version = doArgs.version
            rMySoftware = self.clone_mySoftware(doArgs.id, software)
            if type(rMySoftware) is MySoftware:
                printer.out("Clonned successfully", printer.OK)
            else:
                printer.out("Clone error", printer.ERROR)
        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
            self.help_clone()
        except Exception as e:
            return handle_uforge_exception(e)

    def clone_mySoftware(self, id, software):
        return self.api.Users(self.login).Mysoftware(id).Clone.Clone(software)

    def help_clone(self):
        doParser = self.arg_clone()
        doParser.print_help()


    def arg_categories(self):
        doParser = ArgumentParser(prog=self.cmd_name+" categories", add_help = True, description="Lists all the categories available for bundles.")
        return doParser

    def do_categories(self, args):
        try:
            #call UForge API
            printer.out("Getting all categories available for bundles ...")
            orgId = (self.api.Users(self.login).Orgs().Getall()).orgs.org[0].dbId
            categories = self.api.Orgs(orgId).Categories.Getall(Query="type=='PROJECT'")
            categories = generics_utils.order_list_object_by(categories.categories.category, "name")
            if categories is None or len(categories) == 0:
                printer.out("No categories available")
            else:
                table = Texttable(800)
                table.set_cols_dtype(["t"])
                table.header(["Name"])
                for category in categories:
                    table.add_row([category.name])
                print table.draw() + "\n"
                printer.out("Found "+str(len(categories))+" categories")

            return 0
        except Exception as e:
            return handle_uforge_exception(e)

    def help_categories(self):
        doParser = self.arg_list()
        doParser.print_help()