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
            printer.out("Getting all images and publications for [" + self.login + "] ...", printer.INFO)
            images = self.get_all_images()
            if len(images) == 0 :
                printer.out("No image available", printer.INFO)
            else :
                printer.out("Images:")
                table = self.initialize_text_table(800)
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
                printer.out("Found " + str(len(images)) + " images", printer.INFO)

            # get publications
            publish_images = self.api.Users(self.login).Pimages.Getall()
            publish_images = publish_images.publishImages.publishImage

            if publish_images is None or len(publish_images) == 0:
                printer.out("No publication available", printer.INFO)
                return 0

            printer.out("Publications:")
            table = self.initialize_text_table(800)
            table.set_cols_dtype(["t", "t", "t", "t", "t", "t", "t"])
            table.header(["Template name", "Image ID", "Publish ID", "Account name", "Format", "Cloud ID", "Status"])
            publish_images = generics_utils.order_list_object_by(publish_images, "name")
            for publish_image in publish_images:
                pubStatus = self.get_publish_status(publish_image.status)
                table.add_row([publish_image.name,
                               generics_utils.extract_id(publish_image.imageUri),
                               publish_image.dbId,
                               publish_image.credAccount.name if publish_image.credAccount is not None else "-",
                               publish_image.credAccount.targetPlatform.name,
                               publish_image.cloudId if publish_image.cloudId is not None else "-", pubStatus])
            print table.draw() + "\n"
            printer.out("Found " + str(len(publish_images)) + " publications", printer.INFO)

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
                    images = self.get_all_images()
                    image = self.get_image(images, str(doArgs.id))
                    if image is None:
                        printer.out("Image not found", printer.ERROR)
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
            do_parser = self.arg_deploy()
            do_args = do_parser.parse_args(shlex.split(args))

            # if the help command is called, parse_args returns None object
            if not do_args:
                return 2

            publish_image = self.get_publish_image_from_publish_id(do_args.pid)

            if not self.is_publish_image_ready_to_deploy(publish_image):
                raise ValueError("Published image with id '" + do_args.pid + " is not ready to be deployed")

            deploy_file = generics_utils.get_file(do_args.file)
            if deploy_file is None:
                raise TypeError("Deploy file not found")

            if publish_image.targetFormat is None:
                raise TypeError("Publish image target format not found")

            target_plateform_name = publish_image.targetFormat.name
            if "Amazon" in target_plateform_name:
                return self.deploy_aws(deploy_file, publish_image)

            elif "OpenStack" in target_plateform_name:
                return self.deploy_openstack(deploy_file, publish_image)

            elif "Azure" in target_plateform_name:
                return self.deploy_azure(deploy_file, publish_image)

            else:
                printer.out("Hammr only supports deployments for Amazon AWS, OpenStack and Microsoft Azure ARM.",
                            printer.ERROR)
                return 2

        except (TypeError, ValueError) as e:
            printer.out(str(e), printer.ERROR)
            return 2

        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_deploy()
        except KeyboardInterrupt:
            printer.out(
                "You have exited the command-line, however the deployment may still be in progress. Please go to the cloud's console for more information",
                printer.WARNING)
            pass
        except Exception as e:
            return handle_uforge_exception(e)

    def help_deploy(self):
        doParser = self.arg_deploy()
        doParser.print_help()

    def arg_delete(self):
        do_parser = ArgumentParser(prog=self.cmd_name + " delete", add_help=True,
                                  description="Deletes a machine image or publish information")
        mandatory = do_parser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--id', dest='id', required=True, help="the ID of the machine image to delete")
        return do_parser

    def do_delete(self, args):
        try:
            # add arguments
            do_parser = self.arg_delete()
            try:
                do_args = do_parser.parse_args(shlex.split(args))
            except SystemExit as e:
                return
            # call UForge API
            printer.out("Searching image with id [" + do_args.id + "] ...", printer.INFO)
            images = self.get_all_images()
            if len(images) == 0 :
                raise ValueError("No image found")

            table = self.initialize_text_table(800)
            table.set_cols_dtype(["t", "t", "t", "t", "t", "t", "t", "t", "t"])
            table.header(["Id", "Name", "Version", "Rev.", "Format", "Created", "Size", "Compressed", "Status"])
            delete_image = None
            for image in images:
                if str(image.dbId) == str(do_args.id):
                    img_status = self.get_image_status(image.status)
                    table.add_row([image.dbId, image.name, image.version, image.revision, image.targetFormat.name,
                                   image.created.strftime("%Y-%m-%d %H:%M:%S"), size(image.size),
                                   "X" if image.compress else "", img_status])
                    delete_image = image
            if delete_image is not None:
                print table.draw() + "\n"
                if generics_utils.query_yes_no(
                                "Do you really want to delete image with id " + str(delete_image.dbId)):
                    self.delete_image(delete_image)
                    printer.out("Image deleted", printer.OK)
                    return 0
            else:
                printer.out("Image not found", printer.ERROR)

        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_delete()
            return 2
        except ValueError as e:
            printer.out(str(e), printer.ERROR)
            return 2
        except Exception as e:
            return handle_uforge_exception(e)

    def help_delete(self):
        do_parser = self.arg_delete()
        do_parser.print_help()

    def arg_cancel(self):
        do_parser = ArgumentParser(prog=self.cmd_name + " cancel", add_help=True,
                                  description="Cancels a machine image build or publish")
        mandatory = do_parser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--id', dest='id', required=True, help="the ID of the machine image to cancel")
        return do_parser

    def do_cancel(self, args):
        try:
            # add arguments
            do_parser = self.arg_cancel()
            try:
                do_args = do_parser.parse_args(shlex.split(args))
            except SystemExit as e:
                return 2
            # call UForge API
            printer.out("Searching image with id [" + do_args.id + "] ...", printer.INFO)
            images = self.get_all_images()
            if len(images) == 0 :
                raise ValueError("No image found")

            table = self.initialize_text_table(800)
            table.set_cols_dtype(["t", "t", "t", "t", "t", "t", "t", "t", "t"])
            table.header(["Id", "Name", "Version", "Rev.", "Format", "Created", "Size", "Compressed", "Status"])
            cancel_image = None
            for image in images:
                if str(image.dbId) == str(do_args.id):
                    img_status = self.get_image_status(image.status)
                    table.add_row([image.dbId, image.name, image.version, image.revision, image.targetFormat.name,
                                   image.created.strftime("%Y-%m-%d %H:%M:%S"), size(image.size),
                                   "X" if image.compress else "", img_status])
                    print table.draw() + "\n"
                    cancel_image = image
            if cancel_image is None or cancel_image.status.complete or cancel_image.status.cancelled:
                raise ValueError("Image not being generated, impossible to canceled")

            if cancel_image is not None:
                if generics_utils.query_yes_no(
                                "Do you really want to cancel image with id " + str(cancel_image.dbId)):
                    self.cancel_image(cancel_image)
            else:
                printer.out("Image not found", printer.ERROR)

        except ArgumentParserError as e:
            printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
            self.help_delete()
            return 2
        except ValueError as e:
            printer.out(str(e), printer.ERROR)
            return 2

        except Exception as e:
            return handle_uforge_exception(e)

    def help_cancel(self):
        do_parser = self.arg_cancel()
        do_parser.print_help()

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
            printer.out("Searching image with id [" + doArgs.id + "] ...", printer.INFO)
            images = self.get_all_images()
            if len(images) == 0:
                raise ValueError("No image available")

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
            return 2
        except ValueError as e:
            printer.out(str(e), printer.ERROR)
            return 2
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

    def is_publish_image_ready_to_deploy(self, publishImage):
        if not publishImage.status.complete or publishImage.status.error or publishImage.status.cancelled:
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

    def get_publish_image_from_publish_id(self, publish_id):
        publish_images = self.api.Users(self.login).Pimages.Getall()
        publish_images = publish_images.publishImages.publishImage

        if publish_images is None or len(publish_images) == 0:
            raise TypeError("No published images available")

        publish_image = None
        for p in publish_images:
            if str(p.dbId) == str(publish_id):
                publish_image = p

        if publish_image is None:
            raise TypeError("Published image not found")
        else:
            return publish_image

    def deploy_aws(self, deploy_file, publish_image):
        attributes = check_and_get_attributes_from_file(deploy_file, ["name"])

        deployment = build_deployment_aws(attributes)

        deployed_instance = call_deploy(self, publish_image, deployment)

        deployed_instance_id = deployed_instance.applicationId
        status = show_deploy_progress_without_percentage(self, deployed_instance_id)
        return print_deploy_info(self, status, deployed_instance_id)

    def deploy_openstack(self, deploy_file, publish_image):
        attributes = check_and_get_attributes_from_file(deploy_file, ["name", "region", "network", "flavor"])

        bar_status = OpStatus()
        progress = create_progress_bar_openstack(bar_status)

        self.api.setTimeout(300)
        cred_account = retrieve_credaccount(self, publish_image.dbId, publish_image)
        self.api.setTimeout(constants.HTTP_TIMEOUT)
        deployment = build_deployment_openstack(attributes, publish_image, cred_account)

        bar_status.message = "Deploying instance"
        bar_status.percentage = 50
        progress.update(bar_status.percentage)

        deployed_instance = call_deploy(self, publish_image, deployment)

        deployed_instance_id = deployed_instance.applicationId
        status = show_deploy_progress_with_percentage(self, deployed_instance_id, bar_status, progress)
        return print_deploy_info(self, status, deployed_instance_id)

    def deploy_azure(self, deploy_file, publish_image):
        attributes = check_and_get_attributes_from_file(deploy_file, ["name", "userName"])

        deployment = build_deployment_azure(attributes)

        deployed_instance = call_deploy(self, publish_image, deployment)

        deployed_instance_id = deployed_instance.applicationId
        status = show_deploy_progress_without_percentage(self, deployed_instance_id)
        return print_deploy_info(self, status, deployed_instance_id)

    def get_all_images(self):
        images = self.api.Users(self.login).Images.Getall()
        images = images.images.image
        if images is None or len(images) == 0:
            return []
        else :
            return images

    def get_image(self, images, image_id):
        if images is None:
            return None
        for iimage in images:
            if str(iimage.dbId) == str(image_id):
                image = iimage
                return image
        return None

    def delete_image(self, image):
        if is_uri_based_on_appliance(image.uri):
            appliance_id = extract_appliance_id(image.uri)
            self.api.Users(self.login).Appliances(appliance_id).Images(image.dbId).Delete()

        elif is_uri_based_on_scan(image.uri):
            scanned_instance_id = extract_scannedinstance_id(image.uri)
            scan_id = extract_scan_id(image.uri)
            self.api.Users(self.login).Scannedinstances(scanned_instance_id).Scans(scan_id).Images(None, image.dbId).Delete()

        else:
            raise ValueError("Internal error: image cannot be deleted.")

    def cancel_image(self, image):
        if is_uri_based_on_appliance(image.uri):
            appliance_id = extract_appliance_id(image.uri)
            self.api.Users(self.login).Appliances(appliance_id).Images(image.dbId).Status.Cancel()

        elif is_uri_based_on_scan(image.uri):
            scanned_instance_id = extract_scannedinstance_id(image.uri)
            scan_id = extract_scan_id(image.uri)
            self.api.Users(self.login).Scannedinstances(scanned_instance_id).Scans(scan_id). \
                Images(None, image.dbId).Status.Cancel()

        printer.out("Image Canceled", printer.OK)

    def initialize_text_table(self, width):
        table = Texttable(width)
        return table
