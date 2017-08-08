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

import os
import os.path
import ntpath
from ussclicore.utils import generics_utils, printer
from hammr.utils import constants
from uforge.objects.uforge import *

def check_deployment(file, target_platform):
    if target_platform == "Amazon AWS":
        return build_deployment_amazon(file)
    if "OpenStack" in target_platform:
        return build_deployment_openstack(file)
    return None

def build_deployment_amazon(file):
    deployment = Deployment()
    myinstance = InstanceAmazon()

    if not "name" in file:
        printer.out("There is no attribute [name] for a [file]", printer.ERROR)
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

def build_deployment_openstack(file):
    deployment = Deployment()
    myinstance = InstanceOpenStack()

    if not "name" in file:
        printer.out("There is no attribute [name] for a [file]", printer.ERROR)
        return None
    deployment.name = file["name"]

    if not "region" in file:
        printer.out("There is no attribute [region] for a [file]", printer.ERROR)
        return None
    myinstance.region = file["region"]

    if not "network" in file:
        printer.out("There is no attribute [network] for a [file]", printer.ERROR)
        return None
    myinstance.networkId = file["network"]

    if not "flavor" in file:
        printer.out("There is no attribute [flavor] for a [file]", printer.ERROR)
        return None
    myinstance.flavorId = file["flavor"]

    deployment.instances = pyxb.BIND()
    deployment.instances._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Instances')
    deployment.instances.append(myinstance)

    return deployment
