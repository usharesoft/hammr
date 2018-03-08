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

def publish_vcd(pimage, builder):
    # doing field verification
    if not "orgName" in builder:
        printer.out("orgName in vcd builder not found", printer.ERROR)
        return
    if not "catalogName" in builder:
        printer.out("catalogName in vcd builder not found", printer.ERROR)
        return
    if not "imageName" in builder:
        printer.out("imageName in vcd builder not found", printer.ERROR)
        return

    pimage.credAccount.organizationName = builder["orgName"]
    pimage.credAccount.catalogId = builder["catalogName"]
    pimage.credAccount.displayName = builder["imageName"]
    return pimage


def publish_vcenter(builder):
    pimage = PublishImageVSphere()

    # doing field verification

    if not "displayName" in builder:
        printer.out("displayName in vcenter builder not found", printer.ERROR)
        return

    if not "esxHost" in builder:
        printer.out("esxHost in vcenter builder not found", printer.ERROR)
        return

    if not "datastore" in builder:
        printer.out("datastore in vcenter builder not found", printer.ERROR)
        return

    if "network" in builder:
        pimage.network = builder["network"]

    pimage.displayName = builder["displayName"]
    pimage.esxHost = builder["esxHost"]
    pimage.datastore = builder["datastore"]
    return pimage


def publish_cloudstack(builder):
    pimage = PublishImageCloudStack()

    # doing field verification
    if not "imageName" in builder:
        printer.out("imageName in cloudstack builder not found", printer.ERROR)
        return
    if not "zone" in builder:
        printer.out("zone in cloudstack builder not found", printer.ERROR)
        return
    if not "description" in builder:
        printer.out("description in cloudstack builder not found", printer.ERROR)
        return

    if "publicImage" in builder:
        pimage.publicImage = True if (builder["publicImage"] == "true") else False
    if "featured" in builder:
        pimage.featuredEnabled = True if (builder["featured"] == "true") else False

    pimage.displayName = builder["imageName"]
    pimage.zoneName = builder["zone"]
    pimage.description = builder["description"]
    return pimage

def publish_cloudstackqcow2(builder):
    return publish_cloudstack(builder)

def publish_cloudstackvhd(builder):
    return publish_cloudstack(builder)

def publish_cloudstackova(builder):
    return publish_cloudstack(builder)


def publish_susecloud(pimage, builder):
    # doing field verification
    if not "imageName" in builder:
        printer.out("imageName in susecloud builder not found", printer.ERROR)
        return
    if not "tenant" in builder:
        printer.out("tenant in susecloud builder not found", printer.ERROR)
        return
    if "description" in builder:
        pimage.credAccount.description = builder["description"]

    pimage.credAccount.displayName = builder["imageName"]
    pimage.credAccount.tenantName = builder["tenant"]
    if "publicImage" in builder:
        pimage.credAccount.publicImage = True if (builder["publicImage"] == "true") else False
    # if "paraVirtualMode" in builder:
    #        pimage.credAccount. = True if (builder["paraVirtualMode"]=="true") else False
    return pimage


def publish_openstack(builder):
    pimage = PublishImageOpenStack()

    # doing field verification
    if not "displayName" in builder:
        printer.out("displayName in openstack builder not found", printer.ERROR)
        return
    if not "tenantName" in builder:
        printer.out("TenantName in openstack builder not found", printer.ERROR)
        return

    pimage.displayName = builder["displayName"]
    pimage.tenantName = builder["tenantName"]

    if "publicImage" in builder:
        pimage.credAccount.publicImage = True if (builder["publicImage"] == "true") else False
    if "keystoneDomain" in builder:
        pimage.keystoneDomain = builder["keystoneDomain"]
        return
    if "keystoneProject" in builder:
        pimage.keystoneProject = builder["keystoneProject"]
        return
    return pimage


def publish_openstackqcow2(builder):
    return publish_openstack(builder)


def publish_openstackvhd(builder):
    return publish_openstack(builder)


def publish_openstackvmdk(builder):
    return publish_openstack(builder)


def publish_openstackvdi(builder):
    return publish_openstack(builder)


def publish_aws(builder):
    pimage = PublishImageAws()

    # doing field verification
    if not "bucket" in builder:
        printer.out("bucket in AWS builder not found", printer.ERROR)
        return
    if not "region" in builder:
        printer.out("region in AMI builder not found", printer.ERROR)
        return

    pimage.bucket = builder["bucket"]
    pimage.region = builder["region"]
    return pimage


def publish_azure(builder):
    if "blob" in builder or "container" in builder:
        printer.out("Azure Resource Manager publish")
        return publish_azure_arm(builder)
    else:
        printer.out("Azure classic publish")
        return publish_azure_classic(builder)


def publish_azure_classic(builder):
    pimage = PublishImageAzure()

    # doing field verification
    if not "storageAccount" in builder:
        printer.out("storageAccount in Microsoft Azure not found", printer.ERROR)
        return
    if not "region" in builder:
        printer.out("region in Microsoft Azure not found", printer.ERROR)
        return

    pimage.storageAccount = builder["storageAccount"]
    pimage.region = builder["region"]

    return pimage


def publish_azure_arm(builder):
    pimage = PublishImageAzureResourceManager()

    if not "storageAccount" in builder:
        printer.out("storageAccount not found", printer.ERROR)
        return
    if not "container" in builder:
        printer.out("container not found", printer.ERROR)
        return
    if not "blob" in builder:
        printer.out("blob not found", printer.ERROR)
        return
    if not "displayName" in builder:
        printer.out("displayName not found", printer.ERROR)
        return

    if "resourceGroup" in builder:
        pimage.resourceGroup = builder["resourceGroup"]

    pimage.storageAccount = builder["storageAccount"]
    pimage.container = builder["container"]
    pimage.blob = builder["blob"]
    pimage.displayName = builder["displayName"]

    return pimage


def publish_flexiant(builder):
    pimage = PublishImageFlexiant()

    # doing field verification
    if not "diskOffering" in builder:
        printer.out("diskOffering in flexiant builder not found", printer.ERROR)
        return
    if not "virtualDatacenterName" in builder:
        printer.out("virtualDatacenterName in flexiant builder not found", printer.ERROR)
        return
    if not "machineImageName" in builder:
        printer.out("machineImageName in flexiant builder not found", printer.ERROR)
        return

    pimage.diskOffering = builder["diskOffering"]
    pimage.virtualDatacenterName = builder["virtualDatacenterName"]
    pimage.machineImageName = builder["machineImageName"]

    return pimage


def publish_flexiant_kvm(builder):
    return publish_flexiant(builder)


def publish_flexiant_ova(builder):
    return publish_flexiant(builder)


def publish_flexiantraw(builder):
    return publish_flexiant(builder)


def publish_abiquo(pimage, builder):
    # doing field verification
    if not "enterprise" in builder:
        printer.out("enterprise in abiquo builder not found", printer.ERROR)
        return
    if not "datacenter" in builder:
        printer.out("datacenter in abiquo builder not found", printer.ERROR)
        return
    if not "productName" in builder:
        printer.out("productName in abiquo builder not found", printer.ERROR)
        return
    if not "category" in builder:
        printer.out("category in abiquo builder not found", printer.ERROR)
        return
    if not "description" in builder:
        printer.out("description in abiquo builder not found", printer.ERROR)
        return

    pimage.credAccount.datacenterName = builder["datacenter"]
    pimage.credAccount.displayName = builder["productName"]
    pimage.credAccount.category = builder["category"]
    pimage.credAccount.organizationName = builder["enterprise"]
    pimage.credAccount.description = builder["description"]

    return pimage


def publish_nimbula(pimage, builder):
    # doing field verification
    if not "imageListName" in builder:
        printer.out("imageListName in nimbula builder not found", printer.ERROR)
        return
    if not "imageVersion" in builder:
        printer.out("imageVersion in nimbula builder not found", printer.ERROR)
        return
    if not "description" in builder:
        printer.out("description in nimbula builder not found", printer.ERROR)
        return

    pimage.credAccount.imageVersion = builder["imageVersion"]
    pimage.credAccount.description = builder["description"]
    pimage.credAccount.listName = builder["imageListName"]

    return pimage


def publish_nimbula_kvm(pimage, builder):
    return publish_nimbula(pimage, builder)


def publish_nimbula_esx(pimage, builder):
    return publish_nimbula(pimage, builder)


def publish_eucalyptus(pimage, builder):
    # doing field verification
    if not "imageName" in builder:
        printer.out("imageName in Eucalyptus builder not found", printer.ERROR)
        return
    if not "description" in builder:
        printer.out("description in Eucalyptus builder not found", printer.ERROR)
        return
    if not "bucket" in builder:
        printer.out("bucket in Eucalyptus builder not found", printer.ERROR)
        return

    pimage.credAccount.displayName = builder["imageName"]
    pimage.credAccount.bucket = builder["bucket"]
    pimage.credAccount.description = builder["description"]
    if "ramdisk" in builder and "kernelId" in builder:
        pimage.credAccount.ramdiskId = builder["ramdisk"]
        pimage.credAccount.kernelId = builder["kernelId"]

    return pimage


def publish_eucalyptus_kvm(pimage, builder):
    return publish_eucalyptus(pimage, builder)


def publish_eucalyptus_xen(pimage, builder):
    return publish_eucalyptus(pimage, builder)


def publish_gce(pimage, builder):
    # doing field verification
    if not "computeZone" in builder:
        printer.out("computeZone in GCE builder not found", printer.ERROR)
        return
    if not "bucketLocation" in builder:
        printer.out("bucketLocation in GCE builder not found", printer.ERROR)
        return
    if not "bucket" in builder:
        printer.out("bucket in GCE builder not found", printer.ERROR)
        return
    if not "projectId" in builder:
        printer.out("projectId in GCE builder not found", printer.ERROR)
        return
    if not "storageClass" in builder:
        printer.out("storageClass in GCE builder not found", printer.ERROR)
        return
    if not "diskNamePrefix" in builder:
        printer.out("diskNamePrefix in AMI builder not found", printer.ERROR)
        return

    if "description" in builder:
        pimage.credAccount.description = builder["description"]

    pimage.credAccount.bucket = builder["bucket"]
    pimage.credAccount.tenantName = builder["projectId"]
    pimage.credAccount.category = builder["storageClass"]
    pimage.credAccount.displayName = builder["diskNamePrefix"]
    pimage.credAccount.zoneName = builder["computeZone"]
    pimage.publishLocation = builder["bucketLocation"]
    return pimage


def publish_outscale(builder):
    pimage = PublishImageOutscale()

    # doing field verification
    if not "region" in builder:
        printer.out("region in cloudstack builder not found", printer.ERROR)
        return

    pimage.region = builder["region"]
    return pimage


def publish_k5vmdk(builder):
    pimage = PublishImageK5()

    # doing field verification
    if not "displayName" in builder:
        printer.out("displayName in k5 builder not found", printer.ERROR)
        return
    if not "domain" in builder:
        printer.out("domain in k5 builder not found", printer.ERROR)
        return
    if not "project" in builder:
        printer.out("project in k5 builder not found", printer.ERROR)
        return
    if not "region" in builder:
        printer.out("region in k5 builder not found", printer.ERROR)
        return

    pimage.displayName = builder["displayName"]
    pimage.keystoneDomain = builder["domain"]
    pimage.keystoneProject = builder["project"]
    pimage.publishLocation = builder["region"]

    return pimage


def publish_docker(builder):
    pimage = PublishImageDocker()

    if not "namespace" in builder:
        printer.out("namespace in Docker builder is missing", printer.ERROR)
        return
    if not "repositoryName" in builder:
        printer.out("repositoryName in Docker builder is missing", printer.ERROR)
        return
    if not "tagName" in builder:
        printer.out("tagName in Docker builder is missing", printer.ERROR)
        return

    pimage.namespace = builder["namespace"]
    pimage.repositoryName = builder["repositoryName"]
    pimage.tagName = builder["tagName"]
    return pimage


def publish_oracleraw(builder):
    pimage = PublishImageOracle()

    if not "displayName" in builder:
        printer.out("displayName in Oracle builder is missing", printer.ERROR)
        return
    if not "computeEndPoint" in builder:
        printer.out("computeEndPoint in Oracle builder is missing", printer.ERROR)
        return

    pimage.displayName = builder["displayName"]
    pimage.computeEndPoint = builder["computeEndPoint"]
    return pimage


def retrieve_source_from_image(image_object, image):
    if is_uri_based_on_appliance(image.uri):
        source = image_object.api.Users(image_object.login).Appliances(
            generics_utils.extract_id(image.applianceUri)).Get()

    elif is_uri_based_on_scan(image.uri):
        scanned_instance_id = extract_scannedinstance_id(image.uri)
        scan_id = extract_scan_id(image.uri)
        source = image_object.api.Users(image_object.login).Scannedinstances(scanned_instance_id).Scans(scan_id).Get()

    return source

# def retrieve_install_profile_from_source(image_object, source):
#     if source is None or not hasattr(source, 'dbId'):
#         raise ValueError("No template or scan found for image")
#
#     install_profile = None
#     if is_uri_based_on_appliance(source.uri):
#         install_profile = image_object.api.Users(image_object.login).Appliances(source.dbId).Installprofile("").Get()
#     elif is_uri_based_on_scan(source.uri):
#         install_profile = source.installProfile
#
#     if install_profile is None:
#         raise ValueError("No installation found on the template or scan")
#     return install_profile

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