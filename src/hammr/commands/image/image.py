
__author__="UShareSoft"

import time
import urllib
from hurry.filesize import size

from texttable import Texttable
from hammr.lib.argumentParser import ArgumentParser, ArgumentParserError
from hammr.lib.cmdHamr import Cmd, HammrGlobal
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer
from hammr.utils import *
from uforge.objects.xsd0 import *


class Image(Cmd, HammrGlobal):
        """List, download or delete existing machine images. Publish new machine image to cloud account from configuration file"""
    
        cmd_name="image"
        pbar=None
    
        def __init__(self):
                super(Image, self).__init__()
                
        def arg_list(self):
                doParser = ArgumentParser(prog=self.cmd_name+" list", add_help = True, description="Displays all the machine images built and publish information of those machine images to their respective target platforms")
                return doParser   

        def do_list(self, args):
                try:                        
                        #call UForge API
                        #get images
                        printer.out("Getting all images and publications for ["+self.login+"] ...")
                        images = self.api.Users(self.login).Images.Get()
                        #get publications                        
                        pimages = self.api.Users(self.login).Pimages.Get()
                        if images is None or not hasattr(images, 'get_image'):
                                printer.out("No images available")
                        else:
                                printer.out("Images:")
                                table = Texttable(800)
                                table.set_cols_dtype(["t","t","t","t","t","t","t","c","t"])
                                table.header(["Id", "Name", "Version", "Rev.", "Format", "Created", "Size", "Compressed", "Generation Status"])
                                images = generics_utils.oder_list_object_by(images.get_image(), "name")
                                for image in images:
                                        imgStatus=self.get_image_status(image.status)
                                        table.add_row([image.dbId, image.name, image.version, image.revision, generate_utils.map_format(image.format.name), image.created.strftime("%Y-%m-%d %H:%M:%S"), size(image.size), "X" if image.compress else "", imgStatus])
                                print table.draw() + "\n"
                                printer.out("Found "+str(len(images))+" images")
                         
                         
                        if pimages is None or not hasattr(pimages, 'get_publishImage'):
                                printer.out("No publication available")
                        else:
                                printer.out("Publications:")
                                table = Texttable(800)
                                table.set_cols_dtype(["t","t","t","t","t","t"])
                                table.header(["Template name", "Image ID","Account name", "Format", "Cloud ID", "Status"])
                                pimages = generics_utils.oder_list_object_by(pimages.get_publishImage(), "name")
                                for pimage in pimages:
                                        pubStatus=self.get_publish_status(pimage.status)
                                        table.add_row([pimage.name, generics_utils.extract_id(pimage.imageUri), pimage.credAccount.name if pimage.credAccount is not None else "-", generate_utils.map_format(pimage.format.name), pimage.cloudId if pimage.cloudId is not None else "-", pubStatus])
                                print table.draw() + "\n"
                                printer.out("Found "+str(len(pimages))+" publications")
                             
                        
                        return 0
                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
                        self.help_list()
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
                    
        def help_list(self):
                doParser = self.arg_list()
                doParser.print_help()
                
        def arg_publish(self):
                doParser = ArgumentParser(prog=self.cmd_name+" publish", add_help = True, description="Publish (upload and register) a built machine image to a target environment")
                mandatory = doParser.add_argument_group("mandatory arguments")
                mandatory.add_argument('--file', dest='file', required=True, help="json file providing the cloud account parameters required for upload and registration")        
                optional = doParser.add_argument_group("optional arguments")
                optional.add_argument('--id',dest='id',required=False, help="id of the image to publish")
                return doParser             
                
        def do_publish(self, args):
                try:            
                        #add arguments
                        doParser = self.arg_publish()
                        try:
                                doArgs = doParser.parse_args(args.split())
                        except SystemExit as e:
                                return
                        #--
                        file = generics_utils.get_file(doArgs.file)
                        if file is None:
                                return 2
                        template=generics_utils.validate_json_file(file)
                        if template is None:
                                return
                                               
                        try:
                                if doArgs.id:
                                        images = self.api.Users(self.login).Images.Get()
                                        if images is None or not hasattr(images, 'get_image'):
                                                printer.out("No images available")
                                        else:
                                                for iimage in images.get_image():
                                                        if str(iimage.dbId) == str(doArgs.id):
                                                                image=iimage
                                        if image is None:
                                                 printer.out("image not found", printer.ERROR)
                                                 return 2
                                        if not self.is_image_ready_to_publish(image, None):
                                                printer.out("Image with name '"+image.name+" can not be published", printer.ERROR)
                                                return  2
                                        appliance = self.api.Users(self.login).Appliances(generics_utils.extract_id(image.applianceUri)).Get()
                                        if appliance is None or not hasattr(appliance, 'dbId'):
                                                printer.out("No template found for image", printer.ERROR)
                                                return
                                        rInstallProfile = self.api.Users(self.login).Appliances(appliance.dbId).Installprofile("").Get()
                                        if rInstallProfile is None:
                                                printer.out("No installation found on the template '"+template["stack"]["name"]+"'", printer.ERROR)
                                                return
                                        builder = self.find_builder(image, template)
                                        if builder is None:
                                                #TODO unmap image format
                                                printer.out("No builder part found for image with format type: "+str(image.format.name), printer.ERROR)
                                                return 2
                                        self.publish_builder(builder, template, appliance, rInstallProfile, 1, image)
                                else:
                                        #Get template which correpond to the template file
                                        appliance = self.api.Users(self.login).Appliances().Getall(Name=template["stack"]["name"], Version=template["stack"]["version"])
                                        if appliance is None or not hasattr(appliance, 'dbId'):
                                                printer.out("No template found on the plateform", printer.ERROR)
                                                return
                                        rInstallProfile = self.api.Users(self.login).Appliances(appliance.dbId).Installprofile("").Get()
                                        if rInstallProfile is None:
                                                printer.out("No installation found on the template '"+template["stack"]["name"]+"'", printer.ERROR)
                                                return    
                                            
                                        i=1
                                        for builder in template["builders"]:
                                                rCode = self.publish_builder(builder, template, appliance, rInstallProfile, i, None)
                                                if rCode>=2:
                                                        return
                                                i+=1
                                                                   
                        except KeyError as e:
                                printer.out("unknown error template json file, key: "+str(e), printer.ERROR)                                
                                                        
                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
                        self.help_publish()
                except KeyboardInterrupt:
                        pass
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
                        
                        
        def help_publish(self):
                doParser = self.arg_publish()
                doParser.print_help()
        
        
        def arg_delete(self):
                doParser = ArgumentParser(prog=self.cmd_name+" delete", add_help = True, description="Deletes a machine image or publish information")
                mandatory = doParser.add_argument_group("mandatory arguments")
                mandatory.add_argument('--id', dest='id', required=True, help="the ID of the machine image to delete")
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
                        printer.out("Searching image with id ["+doArgs.id+"] ...")
                        images = self.api.Users(self.login).Images.Get()
                        if images is None or not hasattr(images, 'get_image'):
                                printer.out("No images available")
                        else:
                                table = Texttable(800)
                                table.set_cols_dtype(["t","t","t","t","t","t","t","c","t"])
                                table.header(["Id", "Name", "Version", "Rev.", "Format", "Created", "Size", "Compressed", "Status"])  
                                deleteImage = None
                                for image in images.get_image():
                                        if str(image.dbId) == str(doArgs.id):
                                                imgStatus=self.get_image_status(image.status)
                                                table.add_row([image.dbId, image.name, image.version, image.revision, generate_utils.map_format(image.format.name), image.created.strftime("%Y-%m-%d %H:%M:%S"), size(image.size), "X" if image.compress else "", imgStatus])
                                                deleteImage=image
                                if deleteImage is not None:
                                        print table.draw() + "\n"
                                        if generics_utils.query_yes_no("Do you really want to delete image with id "+str(deleteImage.dbId)):
                                                self.api.Users(self.login).Appliances(generics_utils.extract_id(deleteImage.applianceUri)).Images(deleteImage.dbId).Delete() 
                                                printer.out("Image deleted", printer.OK)
                                else:
                                        printer.out("Image not found", printer.ERROR)
                        
            
                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
                        self.help_delete()
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
                    
        def help_delete(self):
                doParser = self.arg_delete()
                doParser.print_help()
                
        
        def arg_cancel(self):
                doParser = ArgumentParser(prog=self.cmd_name+" cancel", add_help = True, description="Cancels a machine image build or publish")
                mandatory = doParser.add_argument_group("mandatory arguments")
                mandatory.add_argument('--id', dest='id', required=True, help="the ID of the machine image to cancel")
                return doParser  
                
        def do_cancel(self, args):
                try:
                        #add arguments
                        doParser = self.arg_cancel()
                        try:
                                doArgs = doParser.parse_args(args.split())
                        except SystemExit as e:
                                return
                        #call UForge API
                        printer.out("Searching image with id ["+doArgs.id+"] ...")
                        images = self.api.Users(self.login).Images.Get()
                        if images is None or not hasattr(images, 'get_image'):
                                printer.out("No images available")
                        else:
                                table = Texttable(800)
                                table.set_cols_dtype(["t","t","t","t","t","t","t","c","t"])
                                table.header(["Id", "Name", "Version", "Rev.", "Format", "Created", "Size", "Compressed", "Status"])  
                                cancelImage = None
                                for image in images.get_image():
                                        if str(image.dbId) == str(doArgs.id):
                                                imgStatus=self.get_image_status(image.status)
                                                table.add_row([image.dbId, image.name, image.version, image.revision, generate_utils.map_format(image.format.name), image.created.strftime("%Y-%m-%d %H:%M:%S"), size(image.size), "X" if image.compress else "", imgStatus])
                                                print table.draw() + "\n"
                                                cancelImage=image
                                if cancelImage is None or cancelImage.status.complete or cancelImage.status.cancelled:
                                        printer.out("Image not being generated, impossible to canceled", printer.ERROR)
                                        return
                                        
                                if cancelImage is not None:
                                        if generics_utils.query_yes_no("Do you really want to cancel image with id "+str(cancelImage.dbId)):
                                                self.api.Users(self.login).Appliances(generics_utils.extract_id(cancelImage.applianceUri)).Images(cancelImage.dbId).Status.Cancel()  
                                                printer.out("Image Canceled", printer.OK)
                                else:
                                        printer.out("Image not found", printer.ERROR)
                        
            
                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
                        self.help_delete()
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
                    
        def help_cancel(self):
                doParser = self.arg_cancel()
                doParser.print_help()
        
        
        def arg_download(self):
                doParser = ArgumentParser(prog=self.cmd_name+" download", add_help = True, description="Downloads a machine image to the local filesystem")
                mandatory = doParser.add_argument_group("mandatory arguments")
                mandatory.add_argument('--id', dest='id', required=True, help="the ID of the machine image to delete")   
                mandatory.add_argument('--file', dest='file', required=True, help="the pathname where to store the machine image")        
                return doParser   
        
        def do_download(self, args):
                try:
                        #add arguments
                        doParser = self.arg_download()
                        try:
                                doArgs = doParser.parse_args(args.split())
                        except SystemExit as e:
                                return
                        #call UForge API
                        printer.out("Searching image with id ["+doArgs.id+"] ...")
                        images = self.api.Users(self.login).Images.Get()
                        if images is None or not hasattr(images, 'get_image'):
                                printer.out("No images available")
                        else: 
                                dlImage = None
                                for image in images.get_image():
                                        if str(image.dbId) == str(doArgs.id):
                                                dlImage=image
                                if dlImage is not None and dlImage.status.complete and not dlImage.status.error and dlImage.compress:                                 
                                        download_url = self.api._url+"/"+dlImage.downloadUri
                                        dlUtils = download_utils.Download()
                                        try:
                                                urllib.urlretrieve(download_url, filename=doArgs.file, reporthook=dlUtils.progress_update)
                                        except Exception, e:
                                                printer.out("downloading "+download_url+": "+ str(e), printer.ERROR)
                                                return                                        
                                        dlUtils.progress_finish()
                                        printer.out("Image downloaded", printer.OK)
                                else:
                                        printer.out("Cannot download this image", printer.ERROR)
                        
            
                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
                        self.help_download()
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
                    
        def help_download(self):
                doParser = self.arg_download()
                doParser.print_help()
                
                
        def get_image_status(self, status):
                if (status.complete and not status.error):
                        imgStatus="Done"
                elif status.error:
                        imgStatus="Error"
                elif status.cancelled:
                        imgStatus="Canceled"
                else:
                        imgStatus="In progress ("+str(status.percentage)+"%)"
                return imgStatus


        def get_publish_status(self, status):
                if (status.complete and not status.error):
                        pubStatus="Done"
                elif status.error:
                        pubStatus="Error"
                elif status.cancelled:
                        pubStatus="Canceled"
                else:
                        pubStatus="In progress ("+str(status.percentage)+"%)"
                return pubStatus
            
        def publish_builder(self, builder, template, appliance, rInstallProfile, i, comliantImage):    
                try:
                        if comliantImage is None:
                                printer.out("Publishing '"+builder["type"]+"' image ("+str(i)+"/"+str(len(template["builders"]))+")")

                                #find image wich correspond to the template file
                                format=self.get_image_format(builder)

                                images = self.api.Users(self.login).Appliances(appliance.dbId).Images.Getall(Format=format)
                                if images is None or not hasattr(images, 'get_image'):
                                        printer.out("No images found for the template '"+template["stack"]["name"]+"' with type: "+builder["type"], printer.ERROR)
                                        return 2

                                compliantImages = []
                                for image in images.get_image():
                                        isOk = self.is_image_ready_to_publish(image, builder)
                                        if isOk:
                                                compliantImages.append(image) 

                                if(len(compliantImages)==0):
                                        printer.out("No images found for the template '"+template["stack"]["name"]+"' with type: "+builder["type"], printer.ERROR)
                                        return 2
                                elif(len(compliantImages)==1):
                                        comliantImage=compliantImages[0]
                                else:
                                        #TODO get the last created image
                                        comliantImage=compliantImages[0]

                        else:   #publishing image in param --id
                                printer.out("Publishing '"+builder["type"]+"' image ("+str(i)+"/"+str(1)+")")


                        mypImage = publishImage()
                        mypImage.imageUri = comliantImage.uri
                        mypImage.applianceUri = appliance.uri

                        if not "account" in builder:
                                printer.out("Missing account section on builder: ["+builder["type"]+"]", printer.ERROR)
                                return 2
                        #Get all cloud account on the plateform (for the user)
                        accounts = self.api.Users(self.login).Accounts.Getall()
                        if accounts is None or not accounts.get_credAccount():
                                printer.out("No accounts available on the plateform", printer.ERROR)
                                return 2
                        else:
                                for account in accounts.get_credAccount():
                                        if account.name == builder["account"]["name"]:
                                                mypImage.credAccount = account
                                                break

                                if mypImage.credAccount is None:
                                        printer.out("No accounts available with name " +builder["account"]["name"], printer.ERROR)
                                        return 2

                                format_type = builder["type"]   
                                func = getattr(publish_utils, "publish_"+generics_utils.remove_special_chars(format_type), None)
                                if func:
                                        mypImage = func(mypImage, builder)
                                else:
                                        printer.out("Builder type unknown: "+format_type, printer.ERROR)
                                        return 2

                                if mypImage is None:
                                        return 2

                                rpImage = self.api.Users(self.login).Appliances(appliance.dbId).Images(comliantImage.dbId).Pimages().Publish(mypImage)
                                status = rpImage.status
                                statusWidget = progressbar_widget.Status()
                                statusWidget.status = status
                                widgets = [Bar('>'), ' ', statusWidget, ' ', ReverseBar('<')]
                                progress = ProgressBar(widgets=widgets, maxval=100).start()
                                while not (status.complete or status.error or status.cancelled):
                                        statusWidget.status = status
                                        progress.update(status.percentage)
                                        status = self.api.Users(self.login).Appliances(appliance.dbId).Images(comliantImage.dbId).Pimages(rpImage.dbId).Status.Get()
                                        time.sleep(2)
                                statusWidget.status = status
                                progress.finish()
                                if status.error:
                                        printer.out("Publication to '"+builder["account"]["name"]+"' error: "+status.message+"\n"+status.errorMessage, printer.ERROR)
                                        if status.detailedError:
                                                printer.out(status.detailedErrorMsg)
                                elif status.cancelled:
                                        printer.out("\nPublication to '"+builder["account"]["name"]+"' canceled: "+status.message. printer.WARNING)
                                else:        
                                        printer.out("Publication to '"+builder["account"]["name"]+"' is ok", printer.OK)
                                        rpImage = self.api.Users(self.login).Appliances(appliance.dbId).Images(comliantImage.dbId).Pimages(rpImage.dbId).Get()
                                        if rpImage.cloudId is not None and rpImage.cloudId!="":
                                                printer.out("Cloud ID : "+rpImage.cloudId)
                        return 0            
                except KeyboardInterrupt:
                        printer.out("\n")
                        if generics_utils.query_yes_no("Do you want to cancel the job ?"):
                                if 'appliance' in locals() and 'comliantImage' in locals() and 'rpImage' in locals()\
                                and hasattr(appliance, 'dbId') and hasattr(comliantImage, 'dbId') and hasattr(rpImage, 'dbId'):
                                        self.api.Users(self.login).Appliances(appliance.dbId).Images(comliantImage.dbId).Pimages(rpImage.dbId).Cancel.Cancel()
                                else:
                                        printer.out("Impossible to cancel", printer.WARNING)
                        else:
                                printer.out("Exiting command")
                        raise KeyboardInterrupt
  
                                    
        def is_image_ready_to_publish(self, image, builder):
                if builder is not None:
                        if ("hardwareSettings" in builder) and ("memory" in builder["hardwareSettings"]) and (not image.installProfile.memorySize == builder["hardwareSettings"]["memory"]):
                                return False

                        if ("installation" in builder) and ("swapSize" in builder["installation"]) and (not image.installProfile.swapSize == builder["installation"]["swapSize"]):
                                return False
                                #print str(image.installProfile.swapSize)+"----"+ str(builder["installation"]["swapSize"])
                        #TODO 
                        #if ("diskSize" in builder["installation"]) and (not image.installProfile.diskSize == builder["installation"]["diskSize"]):
                        #        isOk = False
                        #        print str(image.installProfile.diskSize)+"----"+ str(builder["installation"]["diskSize"])

                if not image.status.complete or image.status.error or image.status.cancelled:
                        return False

                return True

        def get_image_format(self, builder):
                if not "type" in builder:
                        return 2
                if builder["type"] in generate_utils.CLOUD_FORMATS:
                        return generate_utils.CLOUD_FORMATS[builder["type"]]
                else:
                        if builder["type"] in generate_utils.VIRTUAL_FORMATS:
                                return generate_utils.VIRTUAL_FORMATS[builder["type"]]
                        else:
                                if builder["type"] in generate_utils.PHYSICAL_FORMATS:
                                        return generate_utils.PHYSICAL_FORMATS[builder["type"]]
                                else:
                                        printer.out("Format "+builder["type"]+" not found", printer.ERROR)
                                        return 2


        def find_builder(self, image, template):
                for builder in template["builders"]:
                        format= self.get_image_format(builder)
                        if format!=2:
                                if image.format.name == format:
                                        return builder
                return None

        