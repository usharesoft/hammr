# Copyright (c) 2007-2018 UShareSoft, All rights reserved
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
            generics_utils.extract_id(image.applianceUri)).Get()

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