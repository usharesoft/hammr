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

import json
import yaml
import sys
import re
import traceback
from os.path import expanduser
import os
import urllib
import pyxb

from uforge.objects.uforge import *
import ussclicore.utils.download_utils
from ussclicore.utils import printer
from ussclicore.utils import generics_utils
from hammr.utils.bundle_utils import *
from hammr_utils import *
from hammr.utils import constants
from progressbar import Bar, ProgressBar, ReverseBar
from ussclicore.utils import progressbar_widget

#TODO: key word provisioner in the builder file for deployment
def validate_deployment(file):
    try:
        isJson = check_extension_is_json(file)
        if isJson:
            data = generics_utils.check_json_syntax(file)
        else:
            data = generics_utils.check_yaml_syntax(file)

        if data is None:
            return
        return data

    except ValueError as e:
        printer.out("JSON parsing error: " + str(e), printer.ERROR)
        printer.out("Syntax of deployment file [" + file + "]: FAILED")
    except IOError as e:
        printer.out("unknown error deployment json file", printer.ERROR)

# TODO handle scan case
def build_deployment_openstack(file, pimage, pimageId, cred_account_ressources):
    file = validate_deployment(file)
    deployment = Deployment()
    myinstance = InstanceOpenStack()

    if not "name" in file:
        printer.out("There is no attribute [name] for the provisioner", printer.ERROR)
        return None
    deployment.name = file["name"]

    if not "region" in file:
        printer.out("There is no attribute [region] for the provisioner", printer.ERROR)
        return None
    myinstance.region = file["region"]

    if not "network" in file:
        printer.out("There is no attribute [network] for the provisioner", printer.ERROR)
        return None
    network_name = file["network"]

    if not "flavor" in file:
        printer.out("There is no attribute [flavor] for the provisioner", printer.ERROR)
        return None
    flavor_name = file["flavor"]

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
    # TODO handle when region not found
    regionsEntities = tenant.regionsEntities
    for regionEntities in regionsEntities:
        regions = regionEntities.regionEntities
        for region in regions:
            if region.regionName == region_name:
                break;

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

def build_deployment_amazon(file):
    file = validate_deployment(file)
    deployment = Deployment()
    myinstance = InstanceAmazon()

    if not "name" in file:
        printer.out("There is no attribute [name] for the provisioner", printer.ERROR)
        return None
    deployment.name = file["name"]

    if not "cores" in file:
        myinstance.cores = "1"
    else:
        myinstance.cores = file["cores"]
    if not "memory" in file:
        myinstance.memory = "1024"
    else:
        myinstance.memory = file["memory"]

    deployment.instances = pyxb.BIND()
    deployment.instances._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Instances')
    deployment.instances.append(myinstance)

    return deployment

def create_progress_bar_openstack(bar_status):
    bar_status.message = "Retrieving information from OpenStack"
    bar_status.percentage = 0
    statusWidget = progressbar_widget.Status()
    statusWidget.status = bar_status
    widgets = [Bar('>'), ' ', statusWidget, ' ', ReverseBar('<')]
    progress = ProgressBar(widgets=widgets, maxval=100).start()
    progress.start()
    return progress
