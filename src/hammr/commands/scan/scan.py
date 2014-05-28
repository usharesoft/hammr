
__author__="UShareSoft"

import urllib
import os.path
import shutil
import paramiko
import getpass
import sys
import time

from texttable import Texttable
from hammr.lib.argumentParser import ArgumentParser, ArgumentParserError
from hammr.lib.cmdHamr import Cmd, HammrGlobal
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer
from hammr.utils import *
from uforge.objects.xsd0 import *



class Scan(Cmd, HammrGlobal):
        """List or delete existing scan images, build an image from a scan, launch the scan of a live system, or import a scan as an image"""
    
        cmd_name="scan"
    
        def __init__(self):
                super(Scan, self).__init__()
                
        
        def arg_list(self):
                doParser = ArgumentParser(prog=self.cmd_name+" list", add_help = True, description="Displays all the scans for the user")
                return doParser        
                
                
        def do_list(self, args):
                try:                        
                        #call UForge API
                        printer.out("Getting scans for ["+self.login+"] ...")
                        myScannedInstances = self.api.Users(self.login).Scannedinstances.Get(None, Includescans="true")
                        if myScannedInstances is None or not hasattr(myScannedInstances, 'get_scannedInstance'):
                                printer.out("No scans available")
                                return
                        else:
                                table = Texttable(800)
                                table.set_cols_dtype(["t","t","t","t"])
                                table.header(["Id", "Name", "Status", "Distribution"])
                                myScannedInstances = generics_utils.oder_list_object_by(myScannedInstances.get_scannedInstance(), "name")
                                for myScannedInstance in myScannedInstances:
                                            table.add_row([myScannedInstance.dbId, myScannedInstance.name, "", myScannedInstance.distribution.name + " "+ myScannedInstance.distribution.version + " " + myScannedInstance.distribution.arch])
                                            scans = generics_utils.oder_list_object_by(myScannedInstance.get_scans().get_scan(), "name")
                                            for scan in scans:
                                                        if (scan.status.complete and not scan.status.error and not scan.status.cancelled):
                                                                status = "Done"
                                                        elif(not scan.status.complete and not scan.status.error and not scan.status.cancelled):
                                                                status = str(scan.status.percentage)+"%"
                                                        else:
                                                                status = "Error"
                                                        table.add_row([scan.dbId, "\t"+scan.name, status, "" ])
                                                        
                                print table.draw() + "\n"
                                printer.out("Found "+str(len(myScannedInstances))+" scans")
                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
                        self.help_list()
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
                        
                        
        def help_list(self):
                doParser = self.arg_list()
                doParser.print_help()
                
        def arg_run(self):
                doParser = ArgumentParser(prog=self.cmd_name+" run", add_help = True, description="Executes a deep scan of a running system")
                mandatory = doParser.add_argument_group("mandatory arguments")
                mandatory.add_argument('--ip', dest='ip', required=True, help="the IP address or fully qualified hostname of the running system")
                mandatory.add_argument('--login', dest='login', required=True, help="the root user name (normally root)")
                mandatory.add_argument('--name', dest='name', required=True, help="the scan name to use when creating the scan meta-data")
                optional = doParser.add_argument_group("optional arguments")
                optional.add_argument('--password', dest='password', required=False, help="the root password to authenticate to the running system")
                optional.add_argument('--dir', dest='dir', required=False, help="the directory where to install the uforge-scan.bin binary used to execute the deep scan")
                optional.add_argument('--exclude', dest='exclude', nargs='+', required=False, help="a list of directories or files to exclude during the deep scan")
                return doParser


        def do_run(self, args):
                try:              
                        #add arguments
                        doParser = self.arg_run()
                        try:
                                doArgs = doParser.parse_args(args.split())
                        except SystemExit as e:
                                return
                        #download scan binary
                        uri = generics_utils.get_uforge_url_from_ws_url(self.api._url)                                
                        download_url = uri+constants.URI_SCAN_BINARY
                        
                        if os.path.isdir(constants.TMP_WORKING_DIR):
                                #delete tmp dir
                                shutil.rmtree(constants.TMP_WORKING_DIR)
                        os.mkdir(constants.TMP_WORKING_DIR)
                        local_uforge_scan_path=constants.TMP_WORKING_DIR+os.sep+constants.SCAN_BINARY_NAME
                        try:
                                urllib.urlretrieve(download_url, filename=local_uforge_scan_path)
                        except Exception, e:
                                printer.out("error downloading "+download_url+": "+ e, printer.ERROR)
                                
                        
                        r_code = self.deploy_and_launch_agent(self.login, self.password, doArgs, local_uforge_scan_path, self.api._url)
                        
                        if r_code!=0:
                                return
                        
                        #delete tmp dir
                        shutil.rmtree(constants.TMP_WORKING_DIR)
                        
                        printer.out("Searching scan on uforge ...")
                        running=True
                        while running:
                                myScannedInstance = self.api.Users(self.login).Scannedinstances.Get(None, Includescans="true", Name=doArgs.name)
                                if myScannedInstance is None or not type(myScannedInstance) is scannedInstance:
                                        time.sleep(5)
                                else:
                                        if not hasattr(myScannedInstance, 'get_scans') or not hasattr(myScannedInstance.get_scans(), 'scan'):
                                                time.sleep(5)
                                        else:
                                                for scan in myScannedInstance.scans.scan:
                                                        if(not scan.status.complete and not scan.status.error and not scan.status.cancelled):
                                                                status = scan.status
                                                                statusWidget = progressbar_widget.Status()
                                                                statusWidget.status = status
                                                                widgets = [Bar('>'), ' ', statusWidget, ' ', ReverseBar('<')]
                                                                progress = ProgressBar(widgets=widgets, maxval=100).start()
                                                                while not (status.complete or status.error or status.cancelled):
                                                                        statusWidget.status = status
                                                                        progress.update(status.percentage)
                                                                        status = (self.api.Users(self.login).Scannedinstances(myScannedInstance.dbId).Scans(scan.dbId).Get("false", "false", "false", "false", None, None, None, None, None)).status
                                                                        time.sleep(2)
                                                                statusWidget.status = status
                                                                progress.finish()
                                                                if status.error:
                                                                        printer.out("Scan  error: "+status.message+"\n"+status.errorMessage, printer.ERROR)
                                                                        if status.detailedError:
                                                                                printer.out(status.detailedErrorMsg)
                                                                elif status.cancelled:
                                                                        printer.out("Scan canceled: "+status.message, printer.WARNING)
                                                                else:        
                                                                        printer.out("Scan successfully", printer.OK)
                                                                running=False
                                                                break
                                                        else:
                                                                pass
                        
                        
                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
                        self.help_run()
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
                    
        def help_run(self):
                doParser = self.arg_run()
                doParser.print_help()
                
        
        def arg_build(self):
                doParser = ArgumentParser(prog=self.cmd_name+" build", add_help = True, description="Builds a machine image from a scan")
                mandatory = doParser.add_argument_group("mandatory arguments")
                mandatory.add_argument('--id', dest='id', required=True, help="the ID of the scan to generate the machine image from")
                mandatory.add_argument('--file', dest='file', required=True, help="json file providing the builder parameters")                
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
                        file = generics_utils.get_file(doArgs.file)
                        if file is None:
                                return 2
                        data = generics_utils.check_json_syntax(file)
                        if "builders" in data:
                                builders=generics_utils.check_mandatory_builders(data["builders"])
                                builders=generics_utils.check_mandatory_generate_scan(builders)
                        else:
                                printer.out("no builder section found", printer.ERROR)
                                return
                        if builders is None:
                                return
                        try:
                                myScannedInstances = self.api.Users(self.login).Scannedinstances.Get(None, Includescans="true")
                                if myScannedInstances is None or not hasattr(myScannedInstances, 'get_scannedInstance'):
                                        printer.out("scan not found", printer.ERROR)
                                        return
                                else:    
                                        myScan=None
                                        for myScannedInstance in myScannedInstances.get_scannedInstance():
                                                for scan in myScannedInstance.scans.scan:
                                                        if str(scan.dbId) == doArgs.id:
                                                                myScan = scan
                                                                myRScannedInstance = myScannedInstance
                                                                break
                                                if myScan is not None:
                                                        break
                            
                                if myScan is not None and myScan.status.complete and not myScan.status.error and not myScan.status.cancelled:
                                        i=1
                                        for builder in builders:
                                                printer.out("Generating '"+builder["type"]+"' image ("+str(i)+"/"+str(len(builders))+")")
                                                format_type = builder["type"]
                                                myimage = image()

                                                myinstallProfile = installProfile()
                                                if "swapSize" in builder["installation"]:
                                                        myinstallProfile.swapSize = builder["installation"]["swapSize"]
                                                myinstallProfile.diskSize = builder["installation"]["diskSize"]

                                                if format_type in generate_utils.CLOUD_FORMATS:
                                                        func = getattr(generate_utils, "generate_"+generics_utils.remove_special_chars(format_type), None)
                                                        if func:
                                                                myimage,myimageFormat,myinstallProfile = func(myimage, builder, myinstallProfile, self.api, self.login)
                                                        else:
                                                                printer.out("Builder type unknown: "+format_type , printer.ERROR)
                                                                return
                                                elif format_type in generate_utils.VIRTUAL_FORMATS:
                                                        func = getattr(generate_utils, "generate_"+generics_utils.remove_special_chars(format_type), None)
                                                        if func:
                                                                myimage,myimageFormat,myinstallProfile = func(myimage, builder, myinstallProfile)
                                                        else:
                                                                printer.out("Builder type unknown: "+format_type , printer.ERROR)
                                                                return
                                                elif format_type in generate_utils.PHYSICAL_FORMATS:
                                                        func = getattr(generate_utils, "generate_"+generics_utils.remove_special_chars(format_type), None)
                                                        if func:
                                                                myimage,myimageFormat,myinstallProfile = func(myimage, builder, myinstallProfile)
                                                        else:
                                                                printer.out("Builder type unknown: "+format_type , printer.ERROR)
                                                                return
                                                else:                                                
                                                        printer.out("Builder type unknown: "+format_type , printer.ERROR)
                                                        return

                                                myimage.format = myimageFormat
                                                myimage.installProfile = myinstallProfile
                                                rImage = self.api.Users(self.login).Scannedinstances(myRScannedInstance.dbId).Scans(myScan.dbId).Images().Generate(myimage)
                                                status = rImage.status
                                                statusWidget = progressbar_widget.Status()
                                                statusWidget.status = status
                                                widgets = [Bar('>'), ' ', statusWidget, ' ', ReverseBar('<')]
                                                progress = ProgressBar(widgets=widgets, maxval=100).start()
                                                while not (status.complete or status.error or status.cancelled):
                                                        statusWidget.status = status
                                                        progress.update(status.percentage)
                                                        status = self.api.Users(self.login).Scannedinstances(myRScannedInstance.dbId).Scans(myScan.dbId).Images(Sitid=rImage.dbId).Status.Get()
                                                        time.sleep(2)
                                                statusWidget.status = status
                                                progress.finish()
                                                if status.error:
                                                        printer.out("Generation '"+builder["type"]+"' error: "+status.message+"\n"+status.errorMessage, printer.ERROR)
                                                        if status.detailedError:
                                                                printer.out(status.detailedErrorMsg)
                                                elif status.cancelled:
                                                        printer.out("Generation '"+builder["type"]+"' canceled: "+status.message, printer.ERROR)
                                                else:     
                                                        printer.out("Generation '"+builder["type"]+"' ok", printer.OK)
                                                i+=1
                                else:
                                        printer.out("Impossible to generate this scan", printer.ERROR)

                        except KeyError as e:
                                printer.out("unknown error template json file", printer.ERROR)
                        
                        
                        
                        
                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
                        self.help_build()
                except KeyboardInterrupt:
                                printer.out("\n")
                                if generics_utils.query_yes_no("Do you want to cancel the job ?"):
                                        if 'myRScannedInstance' in locals() and 'myScan' in locals() and 'rImage' in locals()\
                                        and hasattr(myRScannedInstance, 'dbId') and hasattr(myScan, 'dbId') and hasattr(rImage, 'dbId'):
                                                self.api.Users(self.login).Scannedinstances(myRScannedInstance.dbId).Scans(myScan.dbId).Images(Sitid=rImage.dbId).Status.Cancel()
                                else:
                                        print "Exiting command"
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
           
        def help_build(self):
                doParser = self.arg_build()
                doParser.print_help()
                
                
        def arg_import(self):
                doParser = ArgumentParser(prog=self.cmd_name+" import", add_help = True, description="Imports (or transforms) the scan to a template")
                mandatory = doParser.add_argument_group("mandatory arguments")
                mandatory.add_argument('--id', dest='id', required=True, help="the ID of the scan to import")
                mandatory.add_argument('--name', dest='name', required=True, help="the name to use for the template created from the scan")
                mandatory.add_argument('--version', dest='version', required=True, help="the version to use for the template created from the scan")
                return doParser
        
        def do_import(self, args):
                try:            
                        #add arguments
                        doParser = self.arg_import()
                        #doParser.add_argument('--org', dest='org', required=False)
                        try:
                                doArgs = doParser.parse_args(args.split())
                        except SystemExit as e:
                                return
                        
                        printer.out("Import scan id ["+doArgs.id+"] ...")
                        myScannedInstances = self.api.Users(self.login).Scannedinstances.Get(None, Includescans="true")
                        if myScannedInstances is None or not hasattr(myScannedInstances, 'get_scannedInstance'):
                                printer.out("scan not found", printer.ERROR)
                                return
                        else:    
                                myScan=None
                                for myScannedInstance in myScannedInstances.get_scannedInstance():
                                        for scan in myScannedInstance.scans.scan:
                                                if str(scan.dbId) == doArgs.id:
                                                        myScan = scan
                                                        myRScannedInstance = myScannedInstance
                                                        break
                                        if myScan is not None:
                                                break

                        if myScan is not None and myScan.status.complete and not myScan.status.error and not myScan.status.cancelled:
                                myScanImport = scanImport()
                                myScanImport.applianceName=doArgs.name
                                myScanImport.applianceVersion=doArgs.version
                                myScanImport.orgUri=(self.api.Users(self.login).Orgs().Getall()).org[0].uri
                                rScanImport = self.api.Users(self.login).Scannedinstances(myRScannedInstance.dbId).Scans(myScan.dbId).Imports().Import(myScanImport)
                                status = rScanImport.status
                                statusWidget = progressbar_widget.Status()
                                statusWidget.status = status
                                widgets = [Bar('>'), ' ', statusWidget, ' ', ReverseBar('<')]
                                progress = ProgressBar(widgets=widgets, maxval=100).start()
                                while not (status.complete or status.error or status.cancelled):
                                        statusWidget.status = status
                                        progress.update(status.percentage)
                                        status = (self.api.Users(self.login).Scannedinstances(myRScannedInstance.dbId).Scans(myScan.dbId).Imports().Get(Status="true", I=rScanImport.uri)).status[0]
                                        time.sleep(2)
                                statusWidget.status = status
                                progress.finish()
                                if status.error:
                                        printer.out("Importing error: "+status.message+"\n"+status.errorMessage, printer.ERROR)
                                        if status.detailedError:
                                                printer.out(status.detailedErrorMsg)
                                elif status.cancelled:
                                        printer.out("Importing canceled: "+status.message, printer.WARNING)
                                else:        
                                        printer.out("Importing ok", printer.OK)
                                        
                except KeyboardInterrupt:
                                printer.out("\n")
                                if generics_utils.query_yes_no("Do you want to cancel the job ?"):
                                        if 'myRScannedInstance' in locals() and 'myScan' in locals() and 'rScanImport' in locals()\
                                        and hasattr(myRScannedInstance, 'dbId') and hasattr(myScan, 'dbId') and hasattr(rScanImport, 'dbId'):
                                                self.api.Users(self.login).Scannedinstances(myRScannedInstance.dbId).Scans(myScan.dbId).Imports(rScanImport.dbId).Status.Cancel()
                                else:
                                        printer.out("Exiting command")
                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
                        self.help_import()
                except Exception as e:
                        print generics_utils.print_uforge_exception(e)        
                        
        def help_import(self):
                doParser = self.arg_import()
                doParser.print_help()
                
                
        def arg_delete(self):
                doParser = ArgumentParser(prog=self.cmd_name+" delete", add_help = True, description="Deletes an existing scan")
                mandatory = doParser.add_argument_group("mandatory arguments")
                mandatory.add_argument('--id', dest='id', required=True, help="the ID of the scan to delete")
                return doParser        
                
        def do_delete(self, args):
                try:
                        doParser = self.arg_delete()
                        try:
                                doArgs = doParser.parse_args(args.split())
                        except SystemExit as e:
                                return
                        #call UForge API
                        printer.out("Searching scan with id ["+doArgs.id+"] ...")
                        myScannedInstances = self.api.Users(self.login).Scannedinstances.Get(None, Includescans="true")
                        if myScannedInstances is None or not hasattr(myScannedInstances, 'get_scannedInstance'):
                                printer.out("No scan found")
                                return
                        else:    
                                object_=None
                                for myScannedInstance in myScannedInstances.get_scannedInstance():                                        
                                        if str(myScannedInstance.dbId)==doArgs.id:
                                                object_=myScannedInstance
                                                break
                                        if object_ is not None:
                                                break
                                        else:
                                                for scan in myScannedInstance.scans.scan:
                                                        if str(scan.dbId) == doArgs.id:
                                                                object_=scan
                                                                id_=myScannedInstance.dbId
                                                                break
                        
                        
                        if object_ is None:
                                printer.out("Scan not found", printer.ERROR)
                        else:
                                table = Texttable(800)
                                table.set_cols_dtype(["t","t","t","t"])
                                table.header(["Id", "Name", "Status", "Distribution"])
                                
                                if type(object_)is scannedInstance:
                                        table.add_row([object_.dbId, object_.name, "", object_.distribution.name + " "+ object_.distribution.version + " " + object_.distribution.arch])
                                        print table.draw() + "\n"
                                        if generics_utils.query_yes_no("Do you really want to delete scan with id "+str(doArgs.id)):
                                                printer.out("Please wait...")
                                                self.api.Users(self.login).Scannedinstances(doArgs.id).Delete()
                                                printer.out("Scan deleted", printer.OK)
                                else:
                                        if (object_.status.complete and not object_.status.error and not object_.status.cancelled):
                                                status = "Done"
                                        elif(not object_.status.complete and not object_.status.error and not object_.status.cancelled):
                                                status = str(object_.status.percentage)+"%"
                                        else:
                                                status = "Error"
                                        table.add_row([object_.dbId, "\t"+object_.name, status, "" ])
                                        print table.draw() + "\n"
                                        if generics_utils.query_yes_no("Do you really want to delete scan with id "+str(doArgs.id)):
                                                printer.out("Please wait...")
                                                self.api.Users(self.login).Scannedinstances(id_).Scans(doArgs.id).Delete()
                                                printer.out("Scan deleted", printer.OK)
                         
                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
                        self.help_delete()
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
                    
        def help_delete(self):
                doParser = self.arg_delete()
                doParser.print_help()
        
                
        def deploy_and_launch_agent(self, uforge_login, uforge_password, args, file_src_path, uforge_url):
                hostname= args.ip
                username= args.login
                if not args.password:
                        passW = getpass.getpass('Password for %s@%s: ' % (username, hostname))
                else:
                        passW = args.password
                        
                #paramiko.util.log_to_file('/tmp/ssh.log') # sets up logging
                
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

                
                #if host_keys.has_key(hostname):
                #        hostkeytype = host_keys[hostname].keys()[0]
                #        hostkey = host_keys[hostname][hostkeytype]
                #        print 'Using host key of type %s' % hostkeytype
                
                # now, connect and use paramiko Transport to negotiate SSH2 across the connection
                try:
                        if not args.dir:
                                dir="/tmp"
                        else:
                                dir=args.dir
                        t = paramiko.Transport((hostname, 22))
                        t.connect(username=username, password=passW, hostkey=hostkey)
                        sftp = paramiko.SFTPClient.from_transport(t)
                        
                        #upload uforge scan binary
                        sftp.put(file_src_path, dir+"/"+constants.SCAN_BINARY_NAME)
                        t.close()
                        
                        client = paramiko.SSHClient()
                        client.load_system_host_keys()
                        client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
                        client.connect(hostname, 22, username, passW)
                        
                        #test service
                        stdin, stdout, stderr = client.exec_command('chmod +x '+dir+'/'+constants.SCAN_BINARY_NAME+'; '+dir+'/'+constants.SCAN_BINARY_NAME+' -u '+uforge_login+' -p '+uforge_password+' -U '+uforge_url+' -P')
                        for line in stdout:
                                print '... ' + line.strip('\n')
                        #launch scan                       
                        exclude=""
                        if args.exclude:
                                for ex in args.exclude:
                                        exclude+="-e "+ex+" "
                        client.exec_command('chmod +x '+dir+'/'+constants.SCAN_BINARY_NAME+'; nohup '+dir+'/'+constants.SCAN_BINARY_NAME+' -u '+uforge_login+' -p '+uforge_password+' -U '+uforge_url+' -n '+args.name+' '+exclude+' >/dev/null 2>&1 &')
                        client.close()
                        
                except paramiko.AuthenticationException as e:
                        printer.out("Authentification error: "+e[0], printer.ERROR)
                        return 2
                except Exception, e:
                        printer.out("Caught exception: "+str(e), printer.ERROR)
                        #traceback.print_exc()
                        try:
                                t.close()
                                client.close()
                        except:
                                pass
                        return 2
                
                
                return 0