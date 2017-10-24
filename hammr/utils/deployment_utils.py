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
import pyxb
from uforge.objects.uforge import *
import ussclicore.utils.download_utils
from ussclicore.utils import printer
from ussclicore.utils import generics_utils
from hammr_utils import *
from progressbar import Bar, ProgressBar, ReverseBar, UnknownLength, BouncingBar
from ussclicore.utils import progressbar_widget
import pyxb.binding.content as pyxb_content
from texttable import Texttable
import getpass
import re


def retrieve_credaccount(image_object, pimageId, pimage):
    # Increases the limit for non determinist content: the xml used for openstack retrieval has a lot of
    # non determinist content that raises an exception if limit is low.
    # See https://stackoverflow.com/questions/1952931/how-to-rewrite-this-nondeterministic-xml-schema-to-deterministic
    pyxb_content.AutomatonConfiguration.PermittedNondeterminism = 10000
    if is_uri_based_on_appliance(pimage.uri):
        return retrieve_credaccount_from_app(image_object, pimageId, pimage)
    else:
        return retrieve_credaccount_from_scan(image_object, pimageId, pimage)


def retrieve_credaccount_from_app(image_object, pimageId, pimage):
    image_id = generics_utils.extract_id(pimage.imageUri)
    source_id = generics_utils.extract_id(pimage.applianceUri)
    account_id = pimage.credAccount.dbId
    return image_object.api.Users(image_object.login).Appliances(source_id).Images(image_id).Pimages(pimageId).\
        Accounts(account_id).Resources.Getaccountresources()


def retrieve_credaccount_from_scan(image_object, pimageId, pimage):
    image_id = generics_utils.extract_id(pimage.imageUri)
    scannedinstance_id = extract_scannedinstance_id(pimage.imageUri)
    scan_id = extract_scan_id(pimage.imageUri)
    account_id = pimage.credAccount.dbId
    return image_object.api.Users(image_object.login).Scannedinstances(scannedinstance_id).Scans(scan_id).\
        Images(image_id).Pimages(pimageId).Accounts(account_id).Resources.Getaccountresources()


def validate_deployment(file):
    try:
        isJson = check_extension_is_json(file)
        if isJson:
            data = generics_utils.check_json_syntax(file)
        else:
            data = generics_utils.check_yaml_syntax(file)

        if data is None:
            return
        if "provisioner" not in data:
            printer.out("There is no provisioner in the file", printer.ERROR)
        return data["provisioner"]

    except ValueError as e:
        printer.out("JSON parsing error: " + str(e), printer.ERROR)
        printer.out("Syntax of deployment file [" + file + "]: FAILED")
    except IOError as e:
        printer.out("unknown error deployment json file", printer.ERROR)


def check_and_get_attributes_from_file(deploy_file, expected_attributes):
    file_attributes = validate_deployment(deploy_file)
    for attribute in expected_attributes:
        if not attribute in file_attributes:
            raise ValueError("There is no attribute [" + attribute + "] for the provisioner")

    return file_attributes


def build_deployment_aws(attributes):
    deployment = Deployment()
    myInstance = InstanceAmazon()

    deployment.name = attributes["name"]
    get_instance_cores_and_memory(myInstance, attributes)

    deployment.instances = pyxb.BIND()
    deployment.instances._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Instances')
    deployment.instances.append(myInstance)
    return deployment


def build_deployment_azure(attributes):
    deployment = Deployment()
    myInstance = InstanceAzureResourceManager()

    deployment.name = attributes["name"]
    myInstance.userName = attributes["userName"]

    if "userSshKey" in attributes:
        myInstance.userSshKey = attributes["userSshKey"]
    elif "userSshKeyFile" in attributes:
        myInstance.userSshKey = open(attributes["userSshKeyFile"], "r").read()
    else:
        myInstance.userPassword = query_password_azure("Please enter the password to connect to the instance: ")

    get_instance_cores_and_memory(myInstance, attributes)

    deployment.instances = pyxb.BIND()
    deployment.instances._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Instances')
    deployment.instances.append(myInstance)
    return deployment


def get_instance_cores_and_memory(my_instance, attributes):
    if not "cores" in attributes:
        my_instance.cores = "1"
    else:
        my_instance.cores = attributes["cores"]
    if not "memory" in attributes:
        my_instance.memory = "1024"
    else:
        my_instance.memory = attributes["memory"]


def build_deployment_openstack(attributes, publishImage, credAccountRessources):
    deployment = Deployment()
    myInstance = InstanceOpenStack()

    deployment.name = attributes["name"]
    myInstance.region = attributes["region"]
    networkName = attributes["network"]
    flavorName = attributes["flavor"]

    myInstance.networkId, myInstance.flavorId = retrieve_openstack_resources(myInstance.region, networkName,
                                                                             flavorName, publishImage, credAccountRessources)

    deployment.instances = pyxb.BIND()
    deployment.instances._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Instances')
    deployment.instances.append(myInstance)
    return deployment


def retrieve_openstack_resources(regionName, networkName, flavorName, publishImage, credAccountRessources):
    tenant = retrieve_cred_account_ressources_tenant(credAccountRessources, publishImage)
    region = retrieve_openstack_resources_region(regionName, tenant)
    flavorId = retrieve_openstack_resources_flavor_id(flavorName, region)
    networkId = retrieve_openstack_resources_network_id(networkName, region)

    return networkId[0].encode('ascii', 'ignore'), flavorId.encode('ascii', 'ignore')


def retrieve_cred_account_ressources_tenant(credAccountRessources, publishImage):
    tenant = None
    for t in credAccountRessources.cloudResources.tenants.tenant:
        if t.name == publishImage.tenantName:
            tenant = t
            break

    if tenant is None:
        raise TypeError("Tenant not found")
    else:
        return tenant


def retrieve_openstack_resources_region(region_name, tenant):
    region = None
    for regionEntities in tenant.regionsEntities:
        for regionEntity in regionEntities.regionEntities:
            if regionEntity.regionName == region_name:
                region = regionEntity
                break

    if region is None:
        raise TypeError("Region " + region_name + " not found on OpenStack")
    else:
        return region


def retrieve_openstack_resources_flavor_id(flavor_name, region):
    flavorId = None
    for flavor in region.flavors.flavor:
        if flavor.name == flavor_name:
            flavorId = flavor.id
            break

    if flavorId is None:
        raise TypeError("Cannot find flavor " + flavor_name + " in region " + region.regionName)
    else:
        return flavorId


def retrieve_openstack_resources_network_id(network_name, region):
    networkId = None
    for network in region.networks.network:
        if network.name == network_name:
            networkId = network.id
            break

    if networkId is None:
        raise TypeError("Cannot find network " + network_name + " in region " + region.regionName)
    else:
        return networkId


def create_progress_bar_openstack(bar_status):
    bar_status.message = "Retrieving information from OpenStack"
    bar_status.percentage = 0
    statusWidget = progressbar_widget.Status()
    statusWidget.status = bar_status
    widgets = [Bar('>'), ' ', statusWidget, ' ', ReverseBar('<')]
    progress = ProgressBar(widgets=widgets, maxval=100).start()
    progress.start()
    bar_status.percentage = 10
    progress.update(bar_status.percentage)
    return progress


def call_deploy(imageObject, publishImage, deployment):
    image_id = generics_utils.extract_id(publishImage.imageUri)

    if is_uri_based_on_appliance(publishImage.imageUri):
        source = imageObject.api.Users(imageObject.login).Appliances(
            generics_utils.extract_id(publishImage.applianceUri)).Get()

        if source is None or not hasattr(source, 'dbId'):
            raise TypeError("No template found for this image")
        else:
            return imageObject.api.Users(imageObject.login).Appliances(source.dbId).Images(imageId).Pimages(
                publishImage.dbId).Deploys.Deploy(body=deployment, element_name="ns1:deployment")

    elif is_uri_based_on_scan(publishImage.imageUri):
        scannedInstanceId = extract_scannedinstance_id(publishImage.imageUri)
        scanId = extract_scan_id(publishImage.imageUri)
        source = imageObject.api.Users(imageObject.login).Scannedinstances(scannedInstanceId).Scans(scanId).Get()

        if source is None or not hasattr(source, 'dbId'):
            raise TypeError("No scan found for this image")
        else:
            return imageObject.api.Users(imageObject.login).Scannedinstances(scannedInstanceId).Scans(
                scanId).Images(Itid=imageId).Pimages(publishImage.dbId).Deploys.Deploy(body=deployment,
                                                                                       element_name="ns1:deployment")
    else:
        raise TypeError("No source found for this image")


def print_deploy_info(image_object, status, deployed_instance_id):
    if status.message == "on-fire":
        printer.out("Deployment failed", printer.ERROR)
        if status.detailedError:
            printer.out(status.detailedErrorMsg, printer.ERROR)
        return 1
    else:
        printer.out("Deployment is successful", printer.OK)

        deployment = image_object.api.Users(image_object.login).Deployments(deployed_instance_id).Get()
        instance = deployment.instances.instance[-1]

        deployment_name = deployment.name
        cloud_provider = format_cloud_provider(instance.cloudProvider)
        location = instance.location.provider
        hostname=instance.hostname
        deployment_status = deployment.state

        if instance.sourceSummary and type(instance.sourceSummary) == ScanSummaryLight:
            source_type = "Scan"
            source_id = str(extract_scannedinstance_id(instance.sourceSummary.uri))
            source_name = instance.sourceSummary.name
        elif instance.sourceSummary and type(instance.sourceSummary) == ApplianceSummary:
            source_type = "Template"
            source_id = str(generics_utils.extract_id(instance.sourceSummary.uri))
            source_name = instance.sourceSummary.name
        else:
            source_type = None
            source_id = None
            source_name = None

        table = print_deploy_info_line(deployment_name, deployed_instance_id, cloud_provider, location, hostname, source_type,
                               source_id, source_name, deployment_status)
        print table.draw() + "\n"
        return 0

def show_deploy_progress_without_percentage(image_object, deployed_instance_id):
    printer.out("Deployment in progress", printer.INFO)

    status = image_object.api.Users(image_object.login).Deployments(deployed_instance_id).Status.Getdeploystatus()
    bar = ProgressBar(widgets=[BouncingBar()], maxval=UnknownLength)
    bar.start()
    i = 1
    while not (status.message == "running" or status.message == "on-fire"):
        status = image_object.api.Users(image_object.login).Deployments(deployed_instance_id).Status.Getdeploystatus()
        time.sleep(1)
        bar.update(i)
        i += 2
    bar.finish()
    return status

def show_deploy_progress_with_percentage(image_object, deployed_instance_id, bar_status, progress):
    status = image_object.api.Users(image_object.login).Deployments(deployed_instance_id).Status.Getdeploystatus()
    while not (status.message == "running" or status.message == "on-fire"):
        status = image_object.api.Users(image_object.login).Deployments(deployed_instance_id).Status.Getdeploystatus()
        time.sleep(1)

    bar_status.percentage = 100
    bar_status.message = "Deployment complete"
    progress.update(bar_status.percentage)
    progress.finish()
    return status

def query_password_azure(question):
    pattern = "(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=*!])(?=\\S+$).{6,}"
    while(True):
        first_choice = getpass.getpass(prompt=question)
        if not re.match(pattern, first_choice):
            printer.out("""The user password must be between 6-72 characters long and must contains at least one uppercase character, one lowercase character, one numeric digit and one special character (@#$%^&+=*!)""", printer.WARNING)
            continue;
        second_choice = getpass.getpass(prompt="Please confirm your password: ")
        if second_choice == first_choice:
            break;
        printer.out("The two passwords are different, please try again.", printer.WARNING)
    return first_choice

def format_cloud_provider(cloudprovider):
    if "aws" in cloudprovider:
        return "Amazon"
    if "openstack" in cloudprovider:
        return "OpenStack"
    if "azure" in cloudprovider:
        return "Azure "
    return cloudprovider


def print_deploy_info_line(deployment_name, deployed_instance_id, cloud_provider, location, hostname, source_type,
                       source_id, source_name, deployment_status):
    table = print_deploy_header()
    table.add_row([deployment_name, deployed_instance_id, cloud_provider, location, hostname, source_type, source_id,
               source_name, deployment_status])
    return table

def print_deploy_header():
    table = Texttable(200)
    table.set_cols_dtype(["t", "t", "t", "t", "t", "t", "t", "t", "t"])
    table.header(
        ["Deployment name", "Deployment ID", "Cloud provider", "Region", "Hostname", "Source type", "Source ID",
         "Source name", "Status"])
    return table