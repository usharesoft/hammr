# Copyright (c) 2007-2019 UShareSoft, All rights reserved
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
from hammr.utils.publish_utils import *
from hammr.utils.publish_builders import *
from hammr.utils import image_utils

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
                pubStatus = get_publish_status(publish_image.status)
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
            printer.out("In Arguments: " + str(e), printer.ERROR)
            self.help_list()
        except Exception as e:
            return handle_uforge_exception(e)

    def help_list(self):
        doParser = self.arg_list()
        doParser.print_help()

    def arg_info(self):
        do_parser = ArgumentParser(prog=self.cmd_name + " info", add_help=True,
                                   description="Displays detailed information about a machine image")
        mandatory = do_parser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--id', dest='id', type=str, required=True,
                               help="the ID of the machine image to retrieve")
        return do_parser

    def do_info(self, args):
        try:
            do_parser = self.arg_info()
            do_args = do_parser.parse_args(shlex.split(args))
            if not do_args:
                return 2

            image_list = self.get_all_images()

            info_image = self.get_image(image_list, do_args.id)
            if info_image is None:
                printer.out("The image with id \"" + do_args.id + "\" doesn't exist.", printer.ERROR)
                return 2

            printer.out("Information about [" + info_image.name + "]:")

            self.do_info_draw_general(info_image)
            self.do_info_draw_publication(info_image)
            return 0

        except ArgumentParserError as error:
            printer.out("In Arguments: " + str(error), printer.ERROR)
            self.help_info()
        except Exception as exception:
            return handle_uforge_exception(exception)

    def do_info_draw_general(self, info_image):
        table = Texttable(0)
        table.set_cols_dtype(["a", "t"])
        table.set_cols_align(["l", "l"])

        table.add_row(["Name", info_image.name])
        table.add_row(["Format", info_image.targetFormat.name])
        table.add_row(["Id", info_image.dbId])
        table.add_row(["Version", info_image.version])
        table.add_row(["Revision", info_image.revision])
        table.add_row(["Uri", info_image.uri])

        self.do_info_draw_source(info_image.parentUri, table)

        table.add_row(["Created", info_image.created.strftime("%Y-%m-%d %H:%M:%S")])
        table.add_row(["Size", size(info_image.fileSize)])
        table.add_row(["Compressed", "Yes" if info_image.compress else "No"])

        if self.is_docker_based(info_image.targetFormat.format.name):
            registring_name = None
            if info_image.status.complete:
                registring_name = info_image.registeringName
            table.add_row(["RegisteringName",registring_name])
            table.add_row(["Entrypoint", info_image.entrypoint.replace("\\", "")])

        self.do_info_draw_generation(info_image, table)

        print table.draw() + "\n"

    def do_info_draw_source(self, parent_uri, table):
        appliance_id = image_utils.get_uid_from_uri(parent_uri, "appliances")
        if appliance_id:
            app = self.api.Users(self.login).Appliances(appliance_id).Get()
            table.add_row(["OS", app.distributionName + " " + app.archName])
            table.add_row(["Template Id", app.dbId])
            table.add_row(["Description", app.description])
            return

        scanned_instance_id = image_utils.get_uid_from_uri(parent_uri, "scannedinstances")
        if scanned_instance_id:
            scanned_instance = self.api.Users(self.login).Scannedinstances(scanned_instance_id).Get()
            distro = scanned_instance.distribution
            table.add_row(["OS", distro.name + " " + distro.version + " " + distro.arch])
            table.add_row(["Scan Id", scanned_instance.dbId])
            return

        my_software_id = image_utils.get_uid_from_uri(parent_uri, "mysoftware")
        template_id = image_utils.get_uid_from_uri(parent_uri, "templates")
        if my_software_id and template_id:
            my_software = self.api.Users(self.login).Mysoftware(my_software_id).Get()
            container_template = self.api.Users(self.login).Mysoftware(my_software_id).Templates(template_id).Get()
            distro = container_template.distribution
            table.add_row(["OS", distro.name + " " + distro.version + " " + distro.arch])
            table.add_row(["MySoftware Id", my_software.dbId])
            table.add_row(["Description", my_software.description])
            return

    def do_info_draw_generation(self, info_image, table):
        generation_status = image_utils.get_message_from_status(info_image.status)
        if not generation_status:
            generation_status = "Generating"
        table.add_row(["Generation Status", generation_status])
        table.add_row(["Generation Message", info_image.status.message])
        if info_image.status.error:
            table.add_row(["Detailed Error Message", info_image.status.errorMessage])

    def do_info_draw_publication(self, info_image):
        printer.out("Information about publications:")
        pimages = self.api.Users(self.login).Pimages.Getall()
        table = Texttable(0)
        table.set_cols_align(["l", "l"])

        has_pimage = False
        for pimage in pimages.publishImages.publishImage:
            if pimage.imageUri == info_image.uri:
                has_pimage = True
                cloud_id = None
                publish_status = image_utils.get_message_from_status(pimage.status)
                if not publish_status:
                    publish_status = "Publishing"

                if publish_status == "Done":
                    cloud_id = pimage.cloudId
                    format_name = info_image.targetFormat.format.name
                    if format_name == "docker" or format_name == "openshift":
                        cloud_id = pimage.namespace + "/" + pimage.repositoryName + ":" + pimage.tagName

                table.add_row([publish_status, cloud_id])

        if has_pimage:
            table.header(["Status", "Cloud Id"])
            print table.draw() + "\n"
        else:
            printer.out("No publication")

    def help_info(self):
        do_parser = self.arg_info()
        do_parser.print_help()

    def arg_publish(self):
        do_parser = ArgumentParser(prog=self.cmd_name + " publish", add_help=True,
                                  description="Publish (upload and register) a built machine image to a target environment")
        mandatory = do_parser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--file', dest='file', required=True,
                               help="yaml/json file providing the cloud account parameters required for upload and registration")
        optional = do_parser.add_argument_group("optional arguments")
        optional.add_argument('--id', dest='id', required=False, help="id of the image to publish")
        return do_parser

    def do_publish(self, args):
        try:
            do_args = self.parse_args(args)
            template = retrieve_template_from_file(do_args.file)
            if do_args.id:
                self.do_publish_with_id(do_args.id, template)
            else:
                self.do_publish_without_id(template)

        except KeyError as e:
            printer.out("unknown error template file, key: " + str(e), printer.ERROR)
            return 2
        except ArgumentParserError as e:
            printer.out("In Arguments: " + str(e), printer.ERROR)
            return 2
            self.help_publish()
        except ValueError as e:
            printer.out(str(e), printer.ERROR)
            return 2
        except KeyboardInterrupt:
            return 2
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
            printer.out("In Arguments: " + str(e), printer.ERROR)
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
            printer.out("In Arguments: " + str(e), printer.ERROR)
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
            printer.out("In Arguments: " + str(e), printer.ERROR)
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
        optional = doParser.add_argument_group("optional arguments")
        optional.add_argument('--file', dest='file', required=False,
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
                if self.is_docker_based(dlImage.targetFormat.format.name):
                    printer.out("In order to download the image, please run:", printer.OK)
                    printer.out("docker pull " + dlImage.registeringName)
                else:
                    if doArgs.file is None:
                        printer.out("argument --file is required for this image", printer.ERROR)
                        return 2
                    download_url = self.api.getUrl() + "/" + dlImage.downloadUri
                    dlUtils = download_utils.Download(download_url, doArgs.file, not self.api.getDisableSslCertificateValidation())
                    try:
                        dlUtils.start()
                    except Exception, e:
                        return 2
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
            printer.out("In Arguments: " + str(e), printer.ERROR)
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

    def parse_args(self, args):
        do_parser = self.arg_publish()
        do_args = do_parser.parse_args(shlex.split(args))
        if not do_args:
            raise ArgumentParserError("No arguments")
        return do_args

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

    def do_publish_with_id(self, id, template):
        images = self.get_all_images()
        image = self.get_image(images, str(id))
        if image is None:
            raise ValueError("Image not found")
        if not is_image_ready_to_publish(image, None):
            raise ValueError("Image with name '" + image.name + "' can not be published")

        source = retrieve_source_from_image(self, image)
        builder = self.find_builder(image, template)
        publish_image_from_builder(self, builder, template, source, 1, image)

    def do_publish_without_id(self, template):
        if template.has_key("stack") and template["stack"].has_key("name") and template["stack"].has_key("version"):
            query_string = "name=='" + template["stack"]["name"] + "';version=='" + template["stack"]["version"] + "'"
            appliance = self.retrieve_appliances_from_name_and_version(query_string)
            appliance = appliance[0]
            publish_all_builders(self, template, appliance)

    def build_publish_image(self, image, builder, cred_account):
        format_type = image.targetFormat.format.name
        publish_method = getattr(publish_builders, "publish_" + generics_utils.remove_special_chars(format_type), None)
        if publish_method:
            publish_image = publish_method(builder, cred_account)
            if publish_image is None:
                raise ValueError("Could not find the builder")
        else:
            raise ValueError("Builder type unknown: " + format_type)
        publish_image.credAccount = cred_account
        return publish_image

    def retrieve_appliances_from_name_and_version(self, query_string):
        appliances = self.api.Users(self.login).Appliances().Getall(Query=query_string)
        appliance = appliances.appliances.appliance
        if appliance is None or len(appliance) != 1:
            raise ValueError("No template found on the platform")
        return appliance

    def is_publish_image_ready_to_deploy(self, publishImage):
        if not publishImage.status.complete or publishImage.status.error or publishImage.status.cancelled:
            return False

        return True

    def find_builder(self, image, template):
        for builder in template["builders"]:
            if image.targetFormat.name == builder["type"]:
                return builder
        raise ValueError("No builder part found for image with this format type")

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

    def is_docker_based(self, format_name):
        return format_name == "docker" or format_name == "openshift"
