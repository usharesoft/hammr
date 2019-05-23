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
from ussclicore.utils import printer
from uforge.objects.uforge import *
from hammr.utils.hammr_utils import *
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer, UnknownLength
from ussclicore.utils import generics_utils, printer, progressbar_widget, download_utils

def retrieve_source_from_image(image_object, image):
    if is_uri_based_on_appliance(image.uri):
        source = image_object.api.Users(image_object.login).Appliances(
            generics_utils.extract_id(image.parentUri)).Get()

    elif is_uri_based_on_scan(image.uri):
        scanned_instance_id = extract_scannedinstance_id(image.uri)
        scan_id = extract_scan_id(image.uri)
        source = image_object.api.Users(image_object.login).Scannedinstances(scanned_instance_id).Scans(scan_id).Get()

    return source

def call_publish_webservice(image_object, image, source, publish_image):
    if is_uri_based_on_appliance(image.uri):
        published_image = image_object.api.Users(image_object.login).Appliances(source.dbId).Images(
            image.dbId).Pimages().Publish(body=publish_image, element_name="ns1:publishImage")

    elif is_uri_based_on_scan(image.uri):
        scanned_instance_id = extract_scannedinstance_id(source.uri)
        scan_id = extract_scan_id(source.uri)
        published_image = image_object.api.Users(image_object.login).Scannedinstances(scanned_instance_id).Scans(scan_id). \
            Images(Itid=image.dbId).Pimages().Publish(body=publish_image, element_name="ns1:publishImage")

    else:
        raise TypeError("No template or scan found for the image")

    if published_image is None:
        raise TypeError("No template or scan found for the image")
    else:
        return published_image

def call_status_publish_webservice(image_object, source, image, published_image):
    status = None
    if is_uri_based_on_appliance(image.uri):
        status = image_object.api.Users(image_object.login).Appliances(source.dbId).Images(image.dbId). \
            Pimages(published_image.dbId).Status.Get()
    if is_uri_based_on_scan(image.uri):
        scanned_instance_id = extract_scannedinstance_id(source.uri)
        scan_id = extract_scan_id(source.uri)
        status = image_object.api.Users(image_object.login).Scannedinstances(scanned_instance_id).Scans(scan_id). \
            Images(Itid=image.dbId).Pimages(published_image.dbId).Status.Get()
    return status

def print_publish_status(image_object, source, image, published_image, builder, account_name):
    status = published_image.status
    statusWidget = progressbar_widget.Status()
    statusWidget.status = status
    widgets = [Bar('>'), ' ', statusWidget, ' ', ReverseBar('<')]
    progress = ProgressBar(widgets=widgets, maxval=100).start()
    while not (status.complete or status.error or status.cancelled):
        statusWidget.status = status
        progress.update(status.percentage)
        status = call_status_publish_webservice(image_object, source, image, published_image)
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
        published_image = image_object.get_publish_image_from_publish_id(published_image.dbId)
        printer.out("Publish ID : " + str(published_image.dbId))
        if published_image.cloudId is not None and published_image.cloudId != "":
            printer.out("Cloud ID : " + published_image.cloudId)

def cancel_publish_in_progress(image_object, source, image, published_image):
    if hasattr(source, 'dbId') and hasattr(image, 'dbId') and hasattr(published_image, 'dbId'):

        if is_uri_based_on_appliance(image.uri):
            image_object.api.Users(image_object.login).Appliances(source.dbId).Images(image.dbId).Pimages(
                published_image.dbId).Cancel.Cancel()
        if is_uri_based_on_scan(image.uri):
            scanned_instance_id = extract_scannedinstance_id(source.uri)
            scan_id = extract_scan_id(source.uri)
            image_object.api.Users(image_object.login).Scannedinstances(scanned_instance_id).Scans(scan_id). \
                Images(Itid=image.dbId).Pimages(published_image.dbId).Cancel.Cancel()

    else:
        printer.out("Impossible to cancel", printer.WARNING)

def is_image_ready_to_publish(image, builder):
    if builder is not None:
        if ("hardwareSettings" in builder) and ("memory" in builder["hardwareSettings"]) and (
                not image.installProfile.memorySize == builder["hardwareSettings"]["memory"]):
            return False

        if ("installation" in builder) and ("swapSize" in builder["installation"]) and (
                not image.installProfile.swapSize == builder["installation"]["swapSize"]):
            return False

    if not image.status.complete or image.status.error or image.status.cancelled:
        return False

    return True

def get_publish_status(status):
    if (status.complete and not status.error):
        pubStatus = "Done"
    elif status.error:
        pubStatus = "Error"
    elif status.cancelled:
        pubStatus = "Canceled"
    else:
        pubStatus = "In progress (" + str(status.percentage) + "%)"
    return pubStatus

def get_image_to_publish(image_object, builder, template, appliance, counter):
    printer.out(
        "Publishing '" + builder["type"] + "' image (" + str(counter) + "/" + str(len(template["builders"])) + ")")
    images = image_object.api.Users(image_object.login).Appliances(appliance.dbId).Images.Getall(
        Query="targetFormat.name=='" + builder["type"] + "'")
    images = images.images.image
    if images is None or len(images) == 0:
        raise ValueError(
            "No images found for the template '" + template["stack"]["name"] + "' with type: " + builder["type"])

    images_ready = []
    for image in images:
        isOk = is_image_ready_to_publish(image, builder)
        if isOk:
            images_ready.append(image)

    if (len(images_ready) == 0):
        raise ValueError(
            "No images found for the template '" + template["stack"]["name"] + "' with type: " + builder["type"])
    elif (len(images_ready) == 1):
        image_ready = images_ready[0]
    else:
        image_ready = images_ready[0]

    return image_ready

def get_account_to_publish(image_object, builder):
    if not "account" in builder:
        raise ValueError("Missing account section on builder: [" + builder["type"] + "]")
    # Get all cloud account on the plateform (for the user)
    accounts = image_object.api.Users(image_object.login).Accounts.Getall()
    accounts = accounts.credAccounts.credAccount
    if accounts is None or len(accounts) == 0:
        raise ValueError("No accounts available on the plateform.\n You can use the command 'hammr account create' to create an account.")

    else:
        for account in accounts:
            builder_name = get_account_name_for_publish(image_object, builder)
            if builder_name == "":
                raise ValueError("No account name given")

            if account.name == builder_name:
                # A hack to avoid a toDOM, toXML bug
                account.targetPlatform.type._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'string')
                if hasattr(account, 'certificates'):
                    account.certificates._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Certificates')
                    for c in account.certificates.certificate:
                        c.type._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'string')

                return account
                break

        raise ValueError("No accounts available with name " + builder["account"]["name"] +
                         ".\nYou can use the command 'hammr account create' to create an account.")

# get the account name from field or from the credential file given in the builder
def get_account_name_for_publish(image_object, builder):
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

        builder_name = image_object.get_account_name_from_template(template, builder)

    return builder_name

def publish_image_from_builder(image_object, builder, template, source, counter, image):
    try:
        if image is None:
            image = get_image_to_publish(image_object, builder, template, source, counter)

        cred_account = get_account_to_publish(image_object, builder)
        publish_image = image_object.build_publish_image(image, builder, cred_account)
        publish_image.imageUri = image.uri
        publish_image.parentUri = source.uri
        account_name = publish_image.credAccount.name

        published_image = call_publish_webservice(image_object, image, source, publish_image)
        print_publish_status(image_object, source, image, published_image, builder, account_name)
        return 0

    except KeyboardInterrupt:
        printer.out("\n")
        if generics_utils.query_yes_no("Do you want to cancel the job ?"):
            cancel_publish_in_progress(image_object, source, image, published_image)
        else:
            printer.out("Exiting command")
        raise KeyboardInterrupt

def publish_all_builders(image_object, template, appliance):
    counter = 1
    for builder in template["builders"]:
        if publish_image_from_builder(image_object, builder, template, appliance, counter, None) == 0:
            counter += 1
        else:
            raise Exception("Unknown error")
