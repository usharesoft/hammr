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
import shlex
from hurry.filesize import size

from texttable import Texttable
from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer, UnknownLength
from ussclicore.utils import generics_utils, printer, progressbar_widget, download_utils
from hammr.utils import *
from hammr.utils.hammr_utils import *
from hammr.utils.deployment_utils import *
from uforge.objects.uforge import *

#This import and configuration avoid pyxb warnings about xmls
import logging
logging.basicConfig()
logging.getLogger("pyxb").setLevel(logging.ERROR)

class Image(Cmd, CoreGlobal):
    """List, download or delete existing machine images. Publish new machine image to cloud account from configuration file"""

    cmd_name = "image"
    pbar = None

    def __init__(self):
        super(Image, self).__init__()

    def arg_list(self):
        doParser = ArgumentParser(prog=self.cmd_name + " list", add_help=True,
                                  description="Displays all the machine images built and publish information of those machine images to their respective target platforms")
        return doParser

    def do_list(self, args):
        try:
            # call UForge API
            # get images
            printer.out("Getting all images and publications for [" + self.login + "] ...")
            images = self.api.Users(self.login).Images.Getall()
            images = images.images.image
            # get publications
            pimages = self.api.Users(self.login).Pimages.Getall()
            pimages = pimages.publishImages.publishImage
            if images is None or len(images) == 0:
                printer.out("No images available")
            else:
                printer.out("Images:")
                table = Texttable(800)
                table.set_cols_dtype(["t", "t", "t", "t", "t", "t", "t", "t", "t"])
                table.header(
                    ["Id", "Name", "Version", "Rev.", "Format", "Created", "Size", "Compressed", "Generation Status"])
                images = generics_utils.order_list_object_by(images, "name")
                for image in images:
                    imgStatus = self.get_image_status(image.status)
                    table.add_row([image.dbId, image.name, image.version, image.revision, image.targetFormat.name,
                                   image.created.strftime("%Y-%m-%d %H:%M:%S"), size(image.fileSize),
                                   "X" if image.compress else "", imgStatus])
                print table.draw() + "\n"
                printer.out("Found " + str(len(images)) + " images")

            if pimages is None or len(pimages) == 0:
                printer.out("No publication available")
            else:
                printer.out("Publications:")
                table = Texttable(800)
                table.set_cols_dtype(["t", "t", "t", "t", "t", "t", "t"])
                table.header(["Template name", "Image ID", "Publish ID", "Account name", "Format", "Cloud ID", "Status"])
                pimages = generics_utils.order_list_object_by(pimages, "name")
                for pimage in pimages:
                    pubStatus = self.get_publish_status(pimage.status)
                    table.add_row([pimage.name,
                                   generics_utils.extract_id(pimage.imageUri),
                                   pimage.dbId,
                                   pimage.credAccount.name if pimage.credAccount is not None else "-",
                                   pimage.credAccount.targetPlatform.name,
                                   pimage.cloudId if pimage.cloudId is not None else "-", pubStatus])
                print table.draw() + "\n"
                printer.out("Found " + str(len(pimages)) + " publications")

            return 0
        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_list()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_list(self):
        doParser = self.arg_list()
        doParser.print_help()

    def arg_publish(self):
        doParser = ArgumentParser(prog=self.cmd_name + " publish", add_help=True,
                                  description="Publish (upload and register) a built machine image to a target environment")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--file', dest='file', required=True,
                               help="yaml/json file providing the cloud account parameters required for upload and registration")
        optional = doParser.add_argument_group("optional arguments")
        optional.add_argument('--id', dest='id', required=False, help="id of the image to publish")
        return doParser

    def do_publish(self, args):
        try:
            # add arguments
            doParser = self.arg_publish()
            doArgs = doParser.parse_args(shlex.split(args))

            #if the help command is called, parse_args returns None object
            if not doArgs:
                    return 2

            file = generics_utils.get_file(doArgs.file)
            if file is None:
                return 2
            template = validate(file)
            if template is None:
                return

            try:
                if doArgs.id:
                    images = self.api.Users(self.login).Images.Getall()
                    images = images.images.image
                    if images is None or len(images) == 0:
                        printer.out("No images available")
                    else:
                        for iimage in images:
                            if str(iimage.dbId) == str(doArgs.id):
                                image = iimage
                    if image is None:
                        printer.out("image not found", printer.ERROR)
                        return 2
                    if not self.is_image_ready_to_publish(image, None):
                        printer.out("Image with name '" + image.name + " can not be published", printer.ERROR)
                        return 2
                    appliance = self.api.Users(self.login).Appliances(
                        generics_utils.extract_id(image.applianceUri)).Get()
                    if appliance is None or not hasattr(appliance, 'dbId'):
                        printer.out("No template found for image", printer.ERROR)
                        return
                    rInstallProfile = self.api.Users(self.login).Appliances(appliance.dbId).Installprofile("").Get()
                    if rInstallProfile is None:
                        printer.out("No installation found on the template '" + template["stack"]["name"] + "'",
                                    printer.ERROR)
                        return
                    builder = self.find_builder(image, template)
                    if builder is None:
                        # TODO unmap image format
                        printer.out("No builder part found for image with format type: " + str(template["type"]),
                                    printer.ERROR)
                        return 2
                    self.publish_builder(builder, template, appliance, rInstallProfile, 1, image)
                else:
                    # Get template which correpond to the template file
                    appliances = self.api.Users(self.login).Appliances().Getall(
                        Query="name=='" + template["stack"]["name"] + "';version=='" + template["stack"][
                            "version"] + "'")
                    appliance = appliances.appliances.appliance
                    if appliance is None or len(appliance) != 1:
                        printer.out("No template found on the plateform", printer.ERROR)
                        return 0
                    appliance = appliance[0]
                    rInstallProfile = self.api.Users(self.login).Appliances(appliance.dbId).Installprofile("").Get()
                    if rInstallProfile is None:
                        printer.out("No installation found on the template '" + template["stack"]["name"] + "'",
                                    printer.ERROR)
                        return

                    i = 1
                    for builder in template["builders"]:
                        rCode = self.publish_builder(builder, template, appliance, rInstallProfile, i, None)
                        if rCode >= 2:
                            return
                        i += 1

            except KeyError as e:
                printer.out("unknown error template file, key: " + str(e), printer.ERROR)

        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_publish()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            return handle_uforge_exception(e)

    def help_publish(self):
        doParser = self.arg_publish()
        doParser.print_help()

    def arg_deploy(self):
        doParser = ArgumentParser(prog=self.cmd_name + " deploy", add_help=True,
                                  description="Deploy an instance of a published image on the targeted cloud.")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--file', dest='file', required=True,
                               help="yaml/json file providing the instance parameters required for deployment on targeted cloud")
        mandatory.add_argument('--publish-id', dest='pid', required=True,
                               help="the ID of the published image to deploy")
        return doParser

    def do_deploy(self, args):
        try:
            # add arguments
            doParser = self.arg_deploy()
            doArgs = doParser.parse_args(shlex.split(args))

            # if the help command is called, parse_args returns None object
            if not doArgs:
                return 2

            pimage = self.get_pimage_from_id(doArgs.pid)
            if pimage == 2:
                return 2

            target_platform = ""
            if pimage.targetFormat:
                target_platform = pimage.targetFormat.name

            if not self.is_pimage_ready_to_deploy(pimage):
                printer.out("Published image with name '" + pimage.name + " cannot be deployed", printer.ERROR)
                return 2

            file = generics_utils.get_file(doArgs.file)
            if file is None:
                return 2

            image_id = generics_utils.extract_id(pimage.imageUri)
            if image_id is None or image_id == "":
                printer.out("Image not found", printer.ERROR)
                return 2

            if "Amazon" in target_platform:
                return self.deploy_aws(file, pimage)

            if "OpenStack" in target_platform:
                return self.deploy_openstack(file, pimage)

            if "Azure" in target_platform:
                return self.deploy_azure(file, pimage)

            printer.out("Hammr only supports deployments for Amazon AWS, OpenStack and Microsoft Azure ARM.", printer.ERROR)

            return 2

        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_deploy()
        except KeyboardInterrupt:
            printer.out("You have exited the command-line, however the deployment may still be in progress. Please go to the cloud's console for more information", printer.WARNING)
            pass
        except Exception as e:
            return handle_uforge_exception(e)

    def help_deploy(self):
        doParser = self.arg_deploy()
        doParser.print_help()

    def arg_delete(self):
        doParser = ArgumentParser(prog=self.cmd_name + " delete", add_help=True,
                                  description="Deletes a machine image or publish information")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--id', dest='id', required=True, help="the ID of the machine image to delete")
        return doParser

    def do_delete(self, args):
        try:
            # add arguments
            doParser = self.arg_delete()
            try:
                doArgs = doParser.parse_args(shlex.split(args))
            except SystemExit as e:
                return
            # call UForge API
            printer.out("Searching image with id [" + doArgs.id + "] ...")
            images = self.api.Users(self.login).Images.Getall()
            images = images.images.image
            if images is None or len(images) == 0:
                printer.out("No images available")
            else:
                table = Texttable(800)
                table.set_cols_dtype(["t", "t", "t", "t", "t", "t", "t", "t", "t"])
                table.header(["Id", "Name", "Version", "Rev.", "Format", "Created", "Size", "Compressed", "Status"])
                deleteImage = None
                for image in images:
                    if str(image.dbId) == str(doArgs.id):
                        imgStatus = self.get_image_status(image.status)
                        table.add_row([image.dbId, image.name, image.version, image.revision, image.targetFormat.name,
                                       image.created.strftime("%Y-%m-%d %H:%M:%S"), size(image.size),
                                       "X" if image.compress else "", imgStatus])
                        deleteImage = image
                if deleteImage is not None:
                    print table.draw() + "\n"
                    if generics_utils.query_yes_no(
                                    "Do you really want to delete image with id " + str(deleteImage.dbId)):
                        self.api.Users(self.login).Appliances(
                            generics_utils.extract_id(deleteImage.applianceUri)).Images(deleteImage.dbId).Delete()
                        printer.out("Image deleted", printer.OK)
                else:
                    printer.out("Image not found", printer.ERROR)


        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_delete()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_delete(self):
        doParser = self.arg_delete()
        doParser.print_help()

    def arg_cancel(self):
        doParser = ArgumentParser(prog=self.cmd_name + " cancel", add_help=True,
                                  description="Cancels a machine image build or publish")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--id', dest='id', required=True, help="the ID of the machine image to cancel")
        return doParser

    def do_cancel(self, args):
        try:
            # add arguments
            doParser = self.arg_cancel()
            try:
                doArgs = doParser.parse_args(shlex.split(args))
            except SystemExit as e:
                return
            # call UForge API
            printer.out("Searching image with id [" + doArgs.id + "] ...")
            images = self.api.Users(self.login).Images.Getall()
            images = images.images.image
            if images is None or len(images) == 0:
                printer.out("No images available")
            else:
                table = Texttable(800)
                table.set_cols_dtype(["t", "t", "t", "t", "t", "t", "t", "t", "t"])
                table.header(["Id", "Name", "Version", "Rev.", "Format", "Created", "Size", "Compressed", "Status"])
                cancelImage = None
                for image in images:
                    if str(image.dbId) == str(doArgs.id):
                        imgStatus = self.get_image_status(image.status)
                        table.add_row([image.dbId, image.name, image.version, image.revision, image.targetFormat.name,
                                       image.created.strftime("%Y-%m-%d %H:%M:%S"), size(image.size),
                                       "X" if image.compress else "", imgStatus])
                        print table.draw() + "\n"
                        cancelImage = image
                if cancelImage is None or cancelImage.status.complete or cancelImage.status.cancelled:
                    printer.out("Image not being generated, impossible to canceled", printer.ERROR)
                    return

                if cancelImage is not None:
                    if generics_utils.query_yes_no(
                                    "Do you really want to cancel image with id " + str(cancelImage.dbId)):
                        self.api.Users(self.login).Appliances(
                            generics_utils.extract_id(cancelImage.applianceUri)).Images(
                            cancelImage.dbId).Status.Cancel()
                        printer.out("Image Canceled", printer.OK)
                else:
                    printer.out("Image not found", printer.ERROR)


        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_delete()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_cancel(self):
        doParser = self.arg_cancel()
        doParser.print_help()

    def arg_download(self):
        doParser = ArgumentParser(prog=self.cmd_name + " download", add_help=True,
                                  description="Downloads a machine image to the local filesystem")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--id', dest='id', required=True, help="the ID of the machine image to download")
        mandatory.add_argument('--file', dest='file', required=True,
                               help="the pathname where to store the machine image")
        return doParser

    def do_download(self, args):
        try:
            # add arguments
            doParser = self.arg_download()
            try:
                doArgs = doParser.parse_args(shlex.split(args))
            except SystemExit as e:
                return
            # call UForge API
            printer.out("Searching image with id [" + doArgs.id + "] ...")
            images = self.api.Users(self.login).Images.Getall()
            images = images.images.image
            if images is None or len(images) == 0:
                printer.out("No images available")
            else:
                dlImage = None
                for image in images:
                    if str(image.dbId) == str(doArgs.id):
                        dlImage = image
                if dlImage is not None and dlImage.status.complete and not dlImage.status.error and dlImage.compress:
                    download_url = self.api.getUrl() + "/" + dlImage.downloadUri
                    dlUtils = download_utils.Download(download_url, doArgs.file, not self.api.getDisableSslCertificateValidation())
                    try:
                        dlUtils.start()
                    except Exception, e:
                        return
                    printer.out("Image downloaded", printer.OK)
                elif dlImage is None:
                    printer.out("Unable to find the image to download in your library", printer.ERROR)
                elif not dlImage.status.complete:
                    printer.out("The image is being generated. Unable to download. Please retry later", printer.ERROR)
                elif not dlImage.compress:
                    printer.out("The image has been prepared to be published (not compressed). Cannot download.",
                                printer.ERROR)
                else:
                    printer.out("Cannot download this image", printer.ERROR)


        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_download()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_download(self):
        doParser = self.arg_download()
        doParser.print_help()

    def get_image_status(self, status):
        if (status.complete and not status.error):
            imgStatus = "Done"
        elif status.error:
            imgStatus = "Error"
        elif status.cancelled:
            imgStatus = "Canceled"
        else:
            imgStatus = "In progress (" + str(status.percentage) + "%)"
        return imgStatus

    def get_publish_status(self, status):
        if (status.complete and not status.error):
            pubStatus = "Done"
        elif status.error:
            pubStatus = "Error"
        elif status.cancelled:
            pubStatus = "Canceled"
        else:
            pubStatus = "In progress (" + str(status.percentage) + "%)"
        return pubStatus

    def publish_builder(self, builder, template, appliance, rInstallProfile, i, comliantImage):
        try:
            if comliantImage is None:
                comliantImage = self.get_image_to_publish(builder, template, appliance, i)

            # get target format to define publish method
            format_type = comliantImage.targetFormat.format.name
            publishMethod = getattr(publish_utils, "publish_" + generics_utils.remove_special_chars(format_type), None)
            if publishMethod:
                mypImage = publishMethod(builder)
                if mypImage is None:
                    return 2
            else:
                printer.out("Builder type unknown: " + format_type, printer.ERROR)
                return 2

            mypImage.imageUri = comliantImage.uri
            mypImage.applianceUri = appliance.uri
            mypImage.credAccount = self.get_account_to_publish(builder)
            account_name = mypImage.credAccount.name

            rpImage = self.api.Users(self.login).Appliances(appliance.dbId).Images(
                comliantImage.dbId).Pimages().Publish(body=mypImage, element_name="ns1:publishImage")

            status = rpImage.status
            statusWidget = progressbar_widget.Status()
            statusWidget.status = status
            widgets = [Bar('>'), ' ', statusWidget, ' ', ReverseBar('<')]
            progress = ProgressBar(widgets=widgets, maxval=100).start()
            while not (status.complete or status.error or status.cancelled):
                statusWidget.status = status
                progress.update(status.percentage)
                status = self.api.Users(self.login).Appliances(appliance.dbId).Images(comliantImage.dbId).Pimages(
                    rpImage.dbId).Status.Get()
                time.sleep(2)
            statusWidget.status = status
            progress.finish()
            if status.error:
                printer.out("Publication to '" + builder["account"][
                    "name"] + "' error: " + status.message + "\n" + status.errorMessage, printer.ERROR)
                if status.detailedError:
                    printer.out(status.detailedErrorMsg)
            elif status.cancelled:
                printer.out("\nPublication to '" + builder["account"][
                    "name"] + "' canceled: " + status.message.printer.WARNING)
            else:
                printer.out("Publication to " + account_name + " is ok", printer.OK)
                rpImage = self.api.Users(self.login).Appliances(appliance.dbId).Images(comliantImage.dbId).Pimages(
                    rpImage.dbId).Get()
                if rpImage.cloudId is not None and rpImage.cloudId != "":
                    printer.out("Cloud ID : " + rpImage.cloudId)
            return 0
        except KeyboardInterrupt:
            printer.out("\n")
            if generics_utils.query_yes_no("Do you want to cancel the job ?"):
                if 'appliance' in locals() and 'comliantImage' in locals() and 'rpImage' in locals() \
                        and hasattr(appliance, 'dbId') and hasattr(comliantImage, 'dbId') and hasattr(rpImage, 'dbId'):
                    self.api.Users(self.login).Appliances(appliance.dbId).Images(comliantImage.dbId).Pimages(
                        rpImage.dbId).Cancel.Cancel()
                else:
                    printer.out("Impossible to cancel", printer.WARNING)
            else:
                printer.out("Exiting command")
            raise KeyboardInterrupt

    def is_image_ready_to_publish(self, image, builder):
        if builder is not None:
            if ("hardwareSettings" in builder) and ("memory" in builder["hardwareSettings"]) and (
                    not image.installProfile.memorySize == builder["hardwareSettings"]["memory"]):
                return False

            if ("installation" in builder) and ("swapSize" in builder["installation"]) and (
                    not image.installProfile.swapSize == builder["installation"]["swapSize"]):
                return False
                # print str(image.installProfile.swapSize)+"----"+ str(builder["installation"]["swapSize"])
                # TODO
                # if ("diskSize" in builder["installation"]) and (not image.installProfile.diskSize == builder["installation"]["diskSize"]):
                #        isOk = False
                #        print str(image.installProfile.diskSize)+"----"+ str(builder["installation"]["diskSize"])

        if not image.status.complete or image.status.error or image.status.cancelled:
            return False

        return True

    def is_pimage_ready_to_deploy(self, pimage):
        if not pimage.status.complete or pimage.status.error or pimage.status.cancelled:
            return False

        return True


    def find_builder(self, image, template):
        for builder in template["builders"]:
            if image.targetFormat.name == builder["type"]:
                return builder

        return None

    def get_image_to_publish(self, builder, template, appliance, i):
        printer.out(
            "Publishing '" + builder["type"] + "' image (" + str(i) + "/" + str(len(template["builders"])) + ")")
        images = self.api.Users(self.login).Appliances(appliance.dbId).Images.Getall(
            Query="targetFormat.name=='" + builder["type"] + "'")
        images = images.images.image
        if images is None or len(images) == 0:
            printer.out(
                "No images found for the template '" + template["stack"]["name"] + "' with type: " + builder[
                    "type"], printer.ERROR)
            return 2

        compliantImages = []
        for image in images:
            isOk = self.is_image_ready_to_publish(image, builder)
            if isOk:
                compliantImages.append(image)

        if (len(compliantImages) == 0):
            printer.out(
                "No images found for the template '" + template["stack"]["name"] + "' with type: " + builder[
                    "type"], printer.ERROR)
            return 2
        elif (len(compliantImages) == 1):
            comliantImage = compliantImages[0]
        else:
            # TODO get the last created image
            comliantImage = compliantImages[0]

        return comliantImage

    def get_account_to_publish(self, builder):
        if not "account" in builder:
            printer.out("Missing account section on builder: [" + builder["type"] + "]", printer.ERROR)
            return 2
        # Get all cloud account on the plateform (for the user)
        accounts = self.api.Users(self.login).Accounts.Getall()
        accounts = accounts.credAccounts.credAccount
        if accounts is None or len(accounts) == 0:
            printer.out("No accounts available on the plateform.\n You can use the command 'hammr account create' to create an account.", printer.ERROR)
            return 2
        else:
            for account in accounts:

                builder_name = self.get_account_name_for_publish(builder, account)
                if builder_name == "":
                    printer.out("No account name given", printer.ERROR)
                    return 2

                if account.name == builder_name:
                    # A hack to avoid a toDOM, toXML bug
                    account.targetPlatform.type._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'string')
                    if hasattr(account, 'certificates'):
                        account.certificates._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Certificates')
                        for c in account.certificates.certificate:
                            c.type._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'string')

                    return account
                    break

            printer.out("No accounts available with name " + builder["account"]["name"] + ".\nYou can use the command 'hammr account create' to create an account.", printer.ERROR)
            return 2

    # get the account name from field or from the credential file given in the builder
    def get_account_name_for_publish(self, builder, account):
        builder_name = ""
        if builder["account"].has_key("name"):
            builder_name = builder["account"]["name"]

        elif builder["account"].has_key("file"):

            file = generics_utils.get_file(builder["account"]["file"])
            if file is None:
                return ""
            template = validate(file)
            if template is None:
                return ""

            builder_name = self.get_account_name_from_template(template, builder)

        return builder_name

    def get_account_name_from_template(self, template, builder):
        account_name = ""
        if not template.has_key("accounts"):
            return ""

        for account in template["accounts"]:
            if account.has_key("type") and account["type"] == builder["type"] and account.has_key("name"):
                account_name = account["name"]
        return account_name

    def get_pimage_from_id(self, id):
        pimages = self.api.Users(self.login).Pimages.Getall()
        pimages = pimages.publishImages.publishImage
        pimage = None
        if pimages is None or len(pimages) == 0:
            printer.out("No published images available")
        else:
            for piimage in pimages:
                if str(piimage.dbId) == str(id):
                    pimage = piimage
        if pimage is None:
            printer.out("published image not found", printer.ERROR)
            return 2
        return pimage

    def deploy_aws(self, file, pimage):
        image_id = generics_utils.extract_id(pimage.imageUri)
        deployment = build_deployment_amazon(file)
        if deployment is None:
            return

        deployed_instance = call_deploy(self, pimage, deployment, image_id)
        if deployed_instance == 2:
            return 2
        deployed_instance_id = deployed_instance.applicationId

        print("Deployment in progress")

        status = show_deploy_progress_without_percentage(self, deployed_instance_id)
        return print_deploy_info(self, status, deployed_instance_id)

    def deploy_openstack(self, file, pimage):
        image_id = generics_utils.extract_id(pimage.imageUri)
        pid = pimage.dbId
        bar_status = OpStatus()
        progress = create_progress_bar_openstack(bar_status)
        deployment = build_deployment_openstack(file, pimage, pid, retrieve_credaccount(self, pid, pimage))
        if deployment is None:
            return

        bar_status.percentage = 50
        bar_status.message = "Deploying instance"
        progress.update(bar_status.percentage)

        deployed_instance = call_deploy(self, pimage, deployment, image_id)
        if deployed_instance == 2:
            return 2
        deployed_instance_id = deployed_instance.applicationId

        status = show_deploy_progress_with_percentage(self, deployed_instance_id, bar_status, progress)
        return print_deploy_info(self, status, deployed_instance_id)

    def deploy_azure(self, file, pimage):
        image_id = generics_utils.extract_id(pimage.imageUri)
        deployment = build_deployment_azure(file)
        if deployment is None:
            return

        deployed_instance = call_deploy(self, pimage, deployment, image_id)
        if deployed_instance == 2:
            return 2
        deployed_instance_id = deployed_instance.applicationId

        print("Deployment in progress")

        status = show_deploy_progress_without_percentage(self, deployed_instance_id)
        return print_deploy_info(self, status, deployed_instance_id)