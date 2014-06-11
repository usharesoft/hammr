__author__="UShareSoft"

import time
import tarfile
import os.path
import ntpath
import shutil
import json
from junit_xml import TestSuite, TestCase

from texttable import Texttable
from hammr.lib.argumentParser import ArgumentParser, ArgumentParserError
from hammr.lib.cmdHamr import Cmd, HammrGlobal
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer
#from objects.mapper import *
from uforge.objects.xsd0 import *
from hammr.utils import *


class Template(Cmd, HammrGlobal):
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
                        if appliances is None or not hasattr(appliances, 'get_appliance'):
                                printer.out("No template")                  
                        else:
                            images = self.api.Users(self.login).Images.Get()
                            table = Texttable(800)
                            table.set_cols_dtype(["t","t","t","t","t","t","t","t","t","t"])
                            table.header(["Id", "Name", "Version", "OS", "Created", "Last modified", "# Imgs", "Updates", "Imp", "Shared"])  
                            appliances = generics_utils.oder_list_object_by(appliances.get_appliance(), "name")
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
                        print generics_utils.print_uforge_exception(e)
                    
        def help_list(self):
                doParser = self.arg_list()
                doParser.print_help()
                
        def arg_export(self):
                doParser = ArgumentParser(prog=self.cmd_name+" export", add_help = True, description="Exports a template by creating an archive (compressed tar file) that includes the json template configuration file")
                mandatory = doParser.add_argument_group("mandatory arguments")
                mandatory.add_argument('--id', dest='id', required=True, help="the ID of the template to export")
                optional = doParser.add_argument_group("optional arguments")
                optional.add_argument('--file', dest='file', required=False, help="destination path where to store the template configuration file on the local filesystem")
                return doParser
                
        def do_export(self, args):
                try:
                        #add arguments
                        doParser = self.arg_export()
                        try:
                                doArgs = doParser.parse_args(args.split())
                        except SystemExit as e:
                                return                        
                         #call UForge API
                        printer.out("Exporting template with id ["+doArgs.id+"] :")
                        myAppliance = self.api.Users(self.login).Appliances(doArgs.id).Get()
                        if myAppliance is None or type(myAppliance) is not appliance:
                                printer.out("No template")
                        else:
                                applianceExport = self.api.Users(self.login).Appliances(myAppliance.dbId).Exports().Exports()
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
                                        data = self.api.Users(self.login).Appliances(myAppliance.dbId).Exports(applianceExport.dbId).Downloads.Applianceexportdownloadresource()
                                        if doArgs.file is None:
                                                file = open("archive.tar.gz", "w")
                                        else:
                                                file = open(doArgs.file, "w")
                                        file.write(data)
                                        file.close()
                                        printer.out("Download complete of file ["+file.name+"]", printer.OK)
                        return 0
                except IOError as e:
                        printer.out("File error: "+e.strerror, printer.ERROR)
                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
                        self.help_export()
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
        
        def help_export(self):
                doParser = self.arg_export()
                doParser.print_help()
                
                
        def arg_import(self):
                doParser = ArgumentParser(prog=self.cmd_name+" import", add_help = True, description="Creates a template from an archive")
                mandatory = doParser.add_argument_group("mandatory arguments")
                mandatory.add_argument('--file', dest='file', required=True, help="the path of the archive")
                return doParser
                        
        def do_import(self, args):                
                try:
                        #add arguments
                        doParser = self.arg_import()
                        try:
                                doArgs = doParser.parse_args(args.split())
                        except SystemExit as e:
                                return
                         #call UForge API
                        return self.import_stack(doArgs.file, True, False)
                except ArgumentParserError as e:
                        printer.out("In Arguments: "+str(e)+"\n", printer.ERROR)
                        self.help_import()
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
                        
                        
        def help_import(self):
                doParser = self.arg_import()
                doParser.print_help()
            
        
        def arg_validate(self):
                doParser = ArgumentParser(prog=self.cmd_name+" validate", add_help = True, description="Validates the syntax of a template configuration file")
                mandatory = doParser.add_argument_group("mandatory arguments")
                mandatory.add_argument('--file', dest='file', required=True, help="the json template configuration file")
                return doParser        
                
        def do_validate(self, args):                
                try:                    
                        #add arguments
                        doParser = self.arg_validate()
                        try:
                                doArgs = doParser.parse_args(args.split())
                        except SystemExit as e:
                                return
                        file = generics_utils.get_file(doArgs.file)
                        if file is None:
                                return 2
                        template=generics_utils.validate_json_file(file)
                        if template is None:
                                return 2
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
                mandatory.add_argument('--file', dest='file', required=True, help="json file containing the template content")  
                optional = doParser.add_argument_group("optional arguments")
                optional.add_argument('--archive-path', dest='archive_path', required=False, help="path of where to store the archive of the created template. If provided hammr, creates an archive of the created template, equivalent to running template export")
                optional.add_argument('-f', '--force', dest='force', action='store_true', help='force template creation (delete template/bundle if already exist)', required = False)
                optional.set_defaults(force=False)
                return doParser
        
        def do_create(self, args):
                try:            
                        #add arguments
                        doParser = self.arg_create()
                        try:
                                doArgs = doParser.parse_args(args.split())
                        except SystemExit as e:
                                return
                        #--
                        #get json file (remote or local)
                        file = generics_utils.get_file(doArgs.file)
                        if file is None:
                                return 2
                        template=generics_utils.validate_json_file(file)
                        if template is None:
                                return 2
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
                                                printer.out("No source file found in config", printer.WARNING)
                        try:
                                if "bundles" in template["stack"]:
                                        for bundle in template["stack"]["bundles"]:
                                                if "files" in bundle:
                                                        for files in bundle["files"]:
                                                                #add to list of file to tar
                                                                file_tar_path=constants.FOLDER_BUNDLES + os.sep + generics_utils.remove_URI_forbidden_char(bundle["name"]) + os.sep + generics_utils.remove_URI_forbidden_char(bundle["version"]) + os.sep + generics_utils.remove_URI_forbidden_char(ntpath.basename(files["source"]))
                                                                archive_files.append([file_tar_path,files["source"]])
                                                                #changing source path to archive related source path
                                                                files["source"]=file_tar_path
                                                else:
                                                        printer.out("No files found for bundle", printer.WARNING)
                                                if "license" in bundle and "source" in bundle["license"]:
                                                        #add to list of file to tar
                                                        file_tar_path=constants.FOLDER_BUNDLES + os.sep + generics_utils.remove_URI_forbidden_char(bundle["name"]) + os.sep + generics_utils.remove_URI_forbidden_char(ntpath.basename(bundle["license"]["source"])) 
                                                        archive_files.append([file_tar_path,bundle["license"]["source"]])
                                                        #changing source path to archive related source path
                                                        bundle["license"]["source"]=file_tar_path                                              
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
                        file = open(constants.TMP_WORKING_DIR + os.sep + constants.TEMPLATE_JSON_NEW_FILE_NAME, "w")
                        json.dump(template, file, indent=4, separators=(',', ': '))
                        file.close()
                        archive_files.append([constants.TEMPLATE_JSON_FILE_NAME, constants.TMP_WORKING_DIR+ os.sep +constants.TEMPLATE_JSON_NEW_FILE_NAME])
                        
                        
                        if doArgs.archive_path is not None:
                                tar_path = doArgs.archive_path
                        else:
                                tar_path = constants.TMP_WORKING_DIR+os.sep+"archive.tar.gz"
                        tar = tarfile.open(tar_path, "w|gz")
                        for file_tar_path,file_global_path in archive_files:
                                file = generics_utils.get_file(file_global_path)                                        
                                if file is None:
                                        return 2
                                tar.add(file, arcname=file_tar_path)
                        tar.close()
                        
                        #arhive is created, doing import
                        self.import_stack(tar_path, False, doArgs.force)
                        
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
                        print generics_utils.print_uforge_exception(e)
            
        def help_create(self):
                doParser = self.arg_create()
                doParser.print_help()
                
        
        def arg_build(self):
                doParser = ArgumentParser(prog=self.cmd_name+" build", add_help = True, description="Builds a machine image from the template")
                mandatory = doParser.add_argument_group("mandatory arguments")
                mandatory.add_argument('--file', dest='file', required=True, help="json file providing the builder parameters")
                optional = doParser.add_argument_group("optional arguments")
                optional.add_argument('--id',dest='id',required=False, help="id of the template to build")
                optional.add_argument('--junit',dest='junit',required=False, help="name of junit XML output file")
                return doParser
        
        def do_build(self, args):
                try:            
                        #add arguments
                        doParser = self.arg_build()
                        try:
                                doArgs = doParser.parse_args(args.split())
                        except SystemExit as e:
                                return
                        #--
                        template=generics_utils.validate_json_file(doArgs.file)
                        if template is None:
                                return 2
                        
                        if doArgs.id:
                                myAppliance = self.api.Users(self.login).Appliances(doArgs.id).Get()
                        else:
                                #Get template which correpond to the template file
                                myAppliance = self.api.Users(self.login).Appliances().Getall(Name=template["stack"]["name"], Version=template["stack"]["version"])
                        if myAppliance is None or type(myAppliance) is not appliance:
                                printer.out("No template found on the plateform")
                                return 0
                        rInstallProfile = self.api.Users(self.login).Appliances(myAppliance.dbId).Installprofile("").Get()
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

                                                if format_type in generate_utils.CLOUD_FORMATS:
                                                        func = getattr(generate_utils, "generate_"+generics_utils.remove_special_chars(format_type), None)
                                                        if func:
                                                                myimage,myimageFormat,myinstallProfile = func(myimage, builder, myinstallProfile, self.api, self.login)
                                                        else:
                                                                printer.out("Builder type unknown: "+format_type, printer.ERROR)
                                                                return 2
                                                elif format_type in generate_utils.VIRTUAL_FORMATS:
                                                        func = getattr(generate_utils, "generate_"+generics_utils.remove_special_chars(format_type), None)
                                                        if func:
                                                                myimage,myimageFormat,myinstallProfile = func(myimage, builder, myinstallProfile)
                                                        else:
                                                                printer.out("Builder type unknown: "+format_type, printer.ERROR)
                                                                return 2
                                                elif format_type in generate_utils.PHYSICAL_FORMATS:
                                                        func = getattr(generate_utils, "generate_"+generics_utils.remove_special_chars(format_type), None)
                                                        if func:
                                                                myimage,myimageFormat,myinstallProfile = func(myimage, builder, myinstallProfile)
                                                        else:
                                                                printer.out("Builder type unknown: "+format_type, printer.ERROR)
                                                                return 2
                                                else:
                                                        printer.out("Builder type unknown: "+format_type, printer.ERROR)
                                                        return 2

                                                if myimage is None:
                                                        return 2

                                                myimage.format = myimageFormat
                                                myimage.installProfile = myinstallProfile
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
                                                if  generics_utils.is_uforge_exception(e):
                                                        print generics_utils.print_uforge_exception(e)
                                                        if doArgs.junit is not None and "test_results" in locals() and len(test_results)>0:
                                                                test=test_results[len(test_results)-1]
                                                                test.elapsed_sec=time.time() - start_time
                                                                test.add_error_info("Error", generics_utils.print_uforge_exception(e))
                                                else:
                                                        raise
                                if doArgs.junit is not None:
                                        testName = myAppliance.distributionName+" "+myAppliance.archName
                                        ts = TestSuite("Generation "+testName, test_results)
                                        with open(doArgs.junit, 'w') as f:
                                                TestSuite.to_file(f, [ts], prettyprint=False)
                                return 0  
                        except KeyError as e:
                                printer.out("unknown error in template json file", printer.ERROR)
                                                
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
                        print generics_utils.print_uforge_exception(e)
                        if doArgs.junit is not None and "test_results" in locals() and len(test_results)>0:
                                test=test_results[len(test_results)-1]
                                if "start_time" in locals():
                                        elapse=time.time() - start_time
                                else:
                                        elapse=0
                                test.elapsed_sec=elapse
                                test.add_error_info("Error", generics_utils.print_uforge_exception(e))
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
                
                
                
        def import_stack(self, file, isImport, isForce):
                try:
                        if isImport:
                                printer.out("Importing template from ["+file+"] archive ...")
                        else:
                                if constants.TMP_WORKING_DIR in str(file):
                                        printer.out("Creating template from temporary ["+file+"] archive ...")
                                else:
                                        printer.out("Creating template from ["+file+"] archive ...")
                        file = open(file, "r")
                        applianceImport = self.api.Users(self.login).Imports.Import(None, None, "true" if isImport else "false", "true" if isForce else "false")
                        if applianceImport is None:
                                if isImport:
                                        printer.out("error importing appliance", printer.ERROR)
                                else:
                                        printer.out("error creating appliance", printer.ERROR)
                                return 2
                        else:
                                status = self.api.Users(self.login).Imports(applianceImport.dbId).Uploads.Upload(file)
                                progress = ProgressBar(widgets=[Percentage(), Bar()], maxval=100).start()
                                while not (status.complete or status.error):                                
                                        progress.update(status.percentage)
                                        status = self.api.Users(self.login).Imports(applianceImport.dbId).Status.Get()
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
                                        applianceImport = self.api.Users(self.login).Imports(applianceImport.dbId).Get()
                                        printer.out("Template URI: "+applianceImport.referenceUri)
                                        printer.out("Template Id : "+generics_utils.extract_id(applianceImport.referenceUri))
                                                
                                return 0
                except IOError as e:
                        printer.out("File error: "+e.strerror, printer.ERROR)
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
                     
                        
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
                        try:
                                doArgs = doParser.parse_args(args.split())
                        except SystemExit as e:
                                return
                        #call UForge API
                        printer.out("Searching template with id ["+doArgs.id+"] ...")
                        myAppliance = self.api.Users(self.login).Appliances(doArgs.id).Get()
                        if myAppliance is None or type(myAppliance) is not appliance:
                                printer.out("Template not found")
                        else:
                                table = Texttable(800)
                                table.set_cols_dtype(["t","t","t","t","t","t","t","t","t","t"])
                                table.header(["Id", "Name", "Version", "OS", "Created", "Last modified", "# Imgs", "Updates", "Imp", "Shared"])  
                                table.add_row([myAppliance.dbId, myAppliance.name, str(myAppliance.version), myAppliance.distributionName+" "+myAppliance.archName,
                                myAppliance.created.strftime("%Y-%m-%d %H:%M:%S"), myAppliance.lastModified.strftime("%Y-%m-%d %H:%M:%S"), len(myAppliance.imageUris.get_uri()),myAppliance.nbUpdates, "X" if myAppliance.imported else "", "X" if myAppliance.shared else ""])
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
                        print generics_utils.print_uforge_exception(e)
                    
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
                        try:
                                doArgs = doParser.parse_args(args.split())
                        except SystemExit as e:
                                return
                         #call UForge API
                        printer.out("Clonnig template with id ["+doArgs.id+"] ...")
                        myAppliance = appliance()
                        myAppliance.name = doArgs.name
                        myAppliance.version = doArgs.version
                        rAppliance = self.api.Users(self.login).Appliances(doArgs.id).Clones.Clone(myAppliance)
                        if type(rAppliance) is appliance:
                                printer.out("Clonned successfully", printer.OK)
                        else:
                                printer.out("Clone error", printer.ERROR)
                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
                        self.help_clone()
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
                        
                        
        def help_clone(self):
                doParser = self.arg_clone()
                doParser.print_help()