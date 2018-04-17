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

from ussclicore.utils import printer
from uforge.objects.uforge import *


def publish_vcd(builder):
    pimage = PublishImageVCloudDirector()

    # doing field verification
    if not "displayName" in builder:
        printer.out("displayName in vcd builder not found", printer.ERROR)
        return
    if not "catalogName" in builder:
        printer.out("catalogName in vcd builder not found", printer.ERROR)
        return
    if not "vdcName" in builder:
        printer.out("vdcName in vcd builder not found", printer.ERROR)
        return

    pimage.displayName = builder["displayName"]
    pimage.catalogName = builder["catalogName"]
    pimage.vdcName = builder["vdcName"]
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


def publish_cloudstack(pimage, builder):
    # doing field verification
    if not "imageName" in builder:
        printer.out("imageName in cloudstack builder not found", printer.ERROR)
        return
    if not "zone" in builder:
        printer.out("zone in cloudstack builder not found", printer.ERROR)
        return
    if "publicImage" in builder:
        pimage.credAccount.publicImage = True if (builder["publicImage"] == "true") else False
    if "featured" in builder:
        pimage.credAccount.featuredEnabled = True if (builder["featured"] == "true") else False

    pimage.credAccount.displayName = builder["imageName"]
    pimage.credAccount.zoneName = builder["zone"]
    return pimage


def publish_cloudstack_qcow2(pimage, builder):
    return publish_cloudstack(pimage, builder)


def publish_cloudstack_vhd(pimage, builder):
    return publish_cloudstack(pimage, builder)


def publish_cloudstack_ova(pimage, builder):
    return publish_cloudstack(pimage, builder)


def publish_susecloud(builder):
    pimage = PublishImageSuseCloud()

    # doing field verification
    if not "keystoneDomain" in builder:
        printer.out("keystoneDomain in susecloud builder not found", printer.ERROR)
        return
    if not "keystoneProject" in builder:
        printer.out("keystoneProject in susecloud builder not found", printer.ERROR)
        return
    if not "displayName" in builder:
        printer.out("displayName in susecloud builder not found", printer.ERROR)
        return
    if not "tenantName" in builder:
        printer.out("tenantName in susecloud builder not found", printer.ERROR)
        return

    pimage.keystoneDomain = builder["keystoneDomain"]
    pimage.keystoneProject = builder["keystoneProject"]
    pimage.displayName = builder["displayName"]
    pimage.tenantName = builder["tenantName"]

    if "publicImage" in builder:
        pimage.publicImage = True if (builder["publicImage"] == "true") else False
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


def publish_openstackvhd(pimage, builder):
    return publish_openstack(pimage, builder)


def publish_openstackvmdk(pimage, builder):
    return publish_openstack(pimage, builder)


def publish_openstackvdi(pimage, builder):
    return publish_openstack(pimage, builder)


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

def publish_google(builder):
    pimage = PublishImageGoogle()

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
        pimage.description = builder["description"]

    pimage.bucket = builder["bucket"]
    pimage.bucketLocation = builder["bucketLocation"]
    pimage.projectId = builder["projectId"]
    pimage.storageClass = builder["storageClass"]
    pimage.diskNamePrefix = builder["diskNamePrefix"]
    pimage.zoneName = builder["computeZone"]
    return pimage


def publish_outscale(pimage, builder):
    # doing field verification
    if not "zone" in builder:
        printer.out("zone in outscale builder not found", printer.ERROR)
        return
    if not "description" in builder:
        pimage.credAccount.description = builder["description"]

    pimage.credAccount.zoneName = builder["zone"]
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
