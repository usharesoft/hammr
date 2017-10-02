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

def build_deployment_amazon(data):
    data = validate_deployment(data)
    deployment = Deployment()
    myinstance = InstanceAmazon()
    if not "name" in data:
        printer.out("There is no attribute [name] for the provisioner", printer.ERROR)
        return None
    deployment.name = data["name"]
    if not "cores" in data:
        myinstance.cores = "1"
    else:
        myinstance.cores = data["cores"]
    if not "memory" in data:
        myinstance.memory = "1024"
    else:
        myinstance.memory = data["memory"]
    deployment.instances = pyxb.BIND()
    deployment.instances._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Instances')
    deployment.instances.append(myinstance)
    return deployment

def build_deployment_azure(data):
    data = validate_deployment(data)
    deployment = Deployment()
    myinstance = InstanceAzureResourceManager()
    if not "name" in data:
        printer.out("There is no attribute [name] for the provisioner", printer.ERROR)
        return None
    deployment.name = data["name"]
    if "userName" in data:
        myinstance.userName = data["userName"]
    else:
        printer.out("There is no attribute [userName] for the provisioner", printer.ERROR)
        return None
    if "userSshKey" in data:
        myinstance.userSshKey = data["userSshKey"]
    elif "userSshKeyFile" in data:
        try:
            myinstance.userSshKey = open(data["userSshKeyFile"], "r").read()
        except IOError as e:
                printer.out("File error: "+str(e), printer.ERROR)
                return
    else:
        myinstance.userPassword = query_password_azure("Please enter the password to connect to the instance: ")

    if not "cores" in data:
        myinstance.cores = "1"
    else:
        myinstance.cores = data["cores"]
    if not "memory" in data:
        myinstance.memory = "1024"
    else:
        myinstance.memory = data["memory"]

    deployment.instances = pyxb.BIND()
    deployment.instances._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Instances')
    deployment.instances.append(myinstance)
    return deployment

def build_deployment_openstack(data, pimage, pimageId, cred_account_ressources):
    data = validate_deployment(data)
    deployment = Deployment()
    myinstance = InstanceOpenStack()

    if not "name" in data:
        printer.out("There is no attribute [name] for the provisioner", printer.ERROR)
        return None
    deployment.name = data["name"]

    if not "region" in data:
        printer.out("There is no attribute [region] for the provisioner", printer.ERROR)
        return None
    myinstance.region = data["region"]

    if not "network" in data:
        printer.out("There is no attribute [network] for the provisioner", printer.ERROR)
        return None
    network_name = data["network"]

    if not "flavor" in data:
        printer.out("There is no attribute [flavor] for the provisioner", printer.ERROR)
        return None
    flavor_name = data["flavor"]

    myinstance.networkId, myinstance.flavorId = retrieve_openstack_resources(myinstance.region, network_name,
                                                                flavor_name, pimage, pimageId, cred_account_ressources)

    deployment.instances = pyxb.BIND()
    deployment.instances._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Instances')
    deployment.instances.append(myinstance)

    return deployment

def retrieve_openstack_resources(region_name, network_name, flavor_name, pimage, pimageId, cred_account_ressources):
    flavor_id = None
    network_id = None
    tenants = cred_account_ressources.cloudResources.tenants.tenant
    tenant_name = pimage.tenantName
    for tenant in tenants:
        if tenant.name == tenant_name:
            break;

    region_retrieved = None
    regionsEntities = tenant.regionsEntities
    for regionEntities in regionsEntities:
        regions = regionEntities.regionEntities
        for region in regions:
            if region.regionName == region_name:
                region_retrieved = region
                break;

    if region_retrieved == None:
        printer.out("Region of the published image not found", printer.ERROR)
        return None, None

    flavors = region.flavors.flavor
    for flavor in flavors:
        if flavor.name == flavor_name:
            flavor_id = flavor.id
            break;

    networks = region.networks.network
    for network in networks:
        if network.name == network_name:
            network_id = network.id
            break;

    return network_id[0].encode('ascii', 'ignore'), flavor_id.encode('ascii', 'ignore')

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

def call_deploy(image_object, pimage, deployment, image_id):
    if is_uri_based_on_appliance(pimage.imageUri):
        source = image_object.api.Users(image_object.login).Appliances(generics_utils.extract_id(pimage.applianceUri)).Get()
        if source is None or not hasattr(source, 'dbId'):
            printer.out("No template found for this image", printer.ERROR)
            return 2
        deployed_instance = image_object.api.Users(image_object.login).Appliances(source.dbId).Images(image_id).Pimages(
            pimage.dbId).Deploys.Deploy(body=deployment, element_name="ns1:deployment")
    elif is_uri_based_on_scan(pimage.imageUri):
        ScannedInstanceId = extract_scannedinstance_id(pimage.imageUri)
        ScanId = extract_scan_id(pimage.imageUri)
        source = image_object.api.Users(image_object.login).Scannedinstances(ScannedInstanceId).Scans(ScanId).Get()
        if source is None or not hasattr(source, 'dbId'):
            printer.out("No scan found for this image", printer.ERROR)
            return 2
        deployed_instance = image_object.api.Users(image_object.login).Scannedinstances(ScannedInstanceId).Scans(
            ScanId).Images(Itid=image_id).Pimages(pimage.dbId).Deploys.Deploy(body=deployment, element_name="ns1:deployment")
    else:
        printer.out("No source found for this image", printer.ERROR)
        return 2
    return deployed_instance

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