# -*- coding: utf-8 -*-
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
from unittest import TestCase

import pyxb
from mock import patch
from uforge.application import Api
from hammr.utils import constants
from uforge.objects.uforge import *
from uforge.objects import uforge
from tests.unit.commands.image.deploy_test_utils import prepare_image, prepare_mock_deploy
from tests.unit.utils.file_utils import findRelativePathFor


class TestDeployAzure(TestCase):
    @patch('uforge.application.Api._Users._Pimages.Getall')
    @patch('uforge.application.Api._Users._Deployments._Status.Getdeploystatus')
    @patch('uforge.application.Api._Users._Appliances._Images._Pimages._Deploys.Deploy')
    @patch('uforge.application.Api._Users._Appliances.Get')
    @patch('uforge.application.Api._Users._Deployments.Get')
    def test_do_deploy_azure_return_0_when_status_is_running(self, mock_get_deployment, mock_app_get, mock_api_deploy,
                                                        mock_get_deploy_status, mock_api_pimg_getall_for_app):
        # given
        i = prepare_image()
        args = self.prepare_image_deploy_command_azure(1234)

        deployment = self.get_deployment_azure()
        pimages = self.prepare_azure_pimages_from_app()

        prepare_mock_deploy(deployment, pimages, Appliance(), ["starting", "starting", "running"],
                        mock_get_deployment, mock_app_get, mock_api_deploy, mock_get_deploy_status,
                        mock_api_pimg_getall_for_app)

        # when
        deploy_return = i.do_deploy(args)

        # then
        self.assertEquals(deploy_return, 0)

    @patch('uforge.application.Api._Users._Pimages.Getall')
    @patch('uforge.application.Api._Users._Deployments._Status.Getdeploystatus')
    @patch('uforge.application.Api._Users._Scannedinstances._Scans._Images._Pimages._Deploys.Deploy')
    @patch('uforge.application.Api._Users._Scannedinstances._Scans.Get')
    @patch('uforge.application.Api._Users._Deployments.Get')
    def test_do_deploy_azure_a_scan_return_0_when_status_is_running(self, mock_get_deployment, mock_scan_get, mock_scan_deploy,
                                                        mock_get_deploy_status, prepare_mock_api_pimg_getall_for_scan):
        # given
        i = prepare_image()
        args = self.prepare_image_deploy_command_azure(1234)

        deployment = self.get_deployment_azure()
        publish_images = self.prepare_azure_pimages_from_scan()

        prepare_mock_deploy(deployment, publish_images, Scan(), ["starting", "starting", "running"],
                        mock_get_deployment, mock_scan_get, mock_scan_deploy, mock_get_deploy_status,
                            prepare_mock_api_pimg_getall_for_scan)

        # when
        deploy_return = i.do_deploy(args)

        # then
        self.assertEquals(deploy_return, 0)

    @patch('uforge.application.Api._Users._Pimages.Getall')
    @patch('uforge.application.Api._Users._Deployments._Status.Getdeploystatus')
    @patch('uforge.application.Api._Users._Appliances._Images._Pimages._Deploys.Deploy')
    @patch('uforge.application.Api._Users._Appliances.Get')
    @patch('uforge.application.Api._Users._Deployments.Get')
    def test_do_deploy_azure_return_1_when_status_is_onfire(self, mock_get_deployment, mock_app_get, mock_api_deploy,
                                                          mock_get_deploy_status, mock_api_pimg_getall_for_app):
        # given
        i = prepare_image()
        args = self.prepare_image_deploy_command_azure(1234)

        deployment = self.get_deployment_azure()
        publish_images = self.prepare_azure_pimages_from_app()

        prepare_mock_deploy(deployment, publish_images, Appliance(), ["starting", "starting", "on-fire"],
                        mock_get_deployment, mock_app_get, mock_api_deploy, mock_get_deploy_status,
                        mock_api_pimg_getall_for_app)

        # when
        deploy_return = i.do_deploy(args)

        # then
        self.assertEquals(deploy_return, 1)

    def get_deployment_azure(self):
        deployment = Deployment()
        deployment.name = "DeploymentName"
        deployment.applicationId = "id123456789"

        instance = InstanceAzureResourceManager()
        instance.cores = "1"
        instance.memory = "1024"
        instance.hostname = "example.com"
        instance.userName = "myName"
        instance.userSshKey = "mySshKey"

        location = Location()
        location.provider = "myprovider"
        instance.location = location
        instance.cloudProvider = "azurearm"

        deployment.instances = pyxb.BIND()
        deployment.instances._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Instances')
        deployment.instances.append(instance)

        return deployment

    def prepare_image_deploy_command_azure(self, id):
         args = "--file %s --publish-id %s" % (findRelativePathFor("tests/integration/data/deploy_azure.yml"), id)
         return args

    def prepare_azure_pimages_from_app(self):
        publish_images = uforge.publishImages()
        publish_images.publishImages = pyxb.BIND()

        publish_image = PublishImageAzureResourceManager()
        publish_image.dbId = 1234
        publish_image.imageUri = 'users/guest/appliances/5/images/1234'
        publish_image.applianceUri = 'users/guest/appliances/5'
        publish_image.status = "complete"
        publish_image.status.complete = True
        publish_image.targetFormat = uforge.targetFormat()
        publish_image.targetFormat.name = "Microsoft Azure"

        publish_images.publishImages.append(publish_image)

        return publish_images

    def prepare_azure_pimages_from_scan(self):
        publish_images = uforge.publishImages()
        publish_images.publishImages = pyxb.BIND()

        publish_image = PublishImageAzureResourceManager()
        publish_image.dbId = 1234
        publish_image.imageUri = 'users/guest/scannedinstances/5/scans/12/images/1234'
        publish_image.status = "complete"
        publish_image.status.complete = True
        publish_image.targetFormat = uforge.targetFormat()
        publish_image.targetFormat.name = "Microsoft Azure"

        publish_images.publishImages.append(publish_image)

        return publish_images

