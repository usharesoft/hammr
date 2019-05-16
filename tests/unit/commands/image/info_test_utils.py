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

import datetime
import pyxb
from uforge.objects import uforge

def create_image():
    image_format = uforge.ImageFormat()
    image_format.name = "aws"

    target_format = uforge.TargetFormat()
    target_format.name = "aws"
    target_format.format = image_format

    image = uforge.Image()
    image.targetFormat = target_format

    image.name = "test image"
    image.dbId = 1
    image.version = "1"
    image.revision = "2"
    image.uri = "users/14/appliances/102/images/1"
    image.fileSize = 1000
    image.compress = True
    image.created = datetime.datetime.now()

    status = uforge.OpStatus()
    status.message = "message"
    status.complete = True
    image.status = status

    return image


def create_image_format_docker():
    image = create_image()
    image.targetFormat.name = "docker"
    image.targetFormat.format.name = "docker"
    image.registeringName = "registry/1/qwerty"
    image.entrypoint = "['/usr/sbin/httpd','-DFOREGROUND']"

    return image


def create_image_status_error():
    image = create_image()
    image.status.complete = False
    image.status.error = True
    image.status.errorMessage = "error message"

    return image


def create_appliance():
    appliance = uforge.Appliance()
    appliance.distributionName = "CentOS 7"
    appliance.archName = "x86_64"
    appliance.dbId = 104
    appliance.uri = "users/guest/appliances/104"
    appliance.description = "Description"

    return appliance


def create_scanned_instance():
    scanned_instance = uforge.ScannedInstance()
    scanned_instance.uri = "users/guest/scannedinstances/10"
    scanned_instance.dbId = 104
    distribution = uforge.Distribution()
    distribution.name = "CentOS"
    distribution.version = "7"
    distribution.arch = "x86_64"
    scanned_instance.distribution = distribution

    return scanned_instance


def create_my_software():
    my_software = uforge.MySoftware()
    my_software.uri = "users/guest/mysoftware/518"
    my_software.dbId = 10
    my_software.description = "description"

    return my_software


def create_container_template():
    container_template = uforge.ContainerTemplate()
    container_template.uri = "users/guest/mysoftware/518/templates/1"
    distribution = uforge.Distribution()
    distribution.name = "CentOS"
    distribution.version = "7"
    distribution.arch = "x86_64"
    container_template.distribution = distribution

    return container_template


def create_pimage():
    pimage = uforge.PublishImageAws()
    pimage.cloudId = "Cloud ID"
    pimage.imageUri = "users/14/appliances/102/images/1"
    pimage.targetFormat = uforge.targetFormat()
    pimage.targetFormat.dbId = 1234

    status = uforge.OpStatus()
    status.complete = True
    pimage.status = status

    return pimage


def create_images(image):
    images = uforge.Images()
    images.images = pyxb.BIND()
    images.images.append(image)

    return images


def create_pimages(pimage=None):
    pimages = uforge.publishImages()
    pimages.publishImages = pyxb.BIND()
    if pimage:
        pimages.publishImages.append(pimage)

    return pimages
