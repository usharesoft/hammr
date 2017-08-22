# -*- coding: utf-8 -*-
# Copyright 2007-2016 UShareSoft SAS, All rights reserved
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
import datetime
from hammr.commands.image import image

class TestDeployAws(TestCase):

    @patch('uforge.application.Api._Users._Appliances._Images._Pimages._Deploys.Deploy')
    def test_do_deploy_return_2_when_imageId_is_None(self, mock_api_deploy):
        # given
        i = self.prepare_image()
        deployment = self.get_deployment()
        mock_api_deploy.return_value = deployment
        args = self.prepare_image_deploy_command(None)

        # when
        deploy_return = i.do_deploy(args)

        # then
        self.assertEquals(deploy_return, 2)

    @patch('uforge.application.Api._Users._Pimages.Getall')
    @patch('uforge.application.Api._Users._Deployments._Status.Getdeploystatus')
    @patch('uforge.application.Api._Users._Appliances._Images._Pimages._Deploys.Deploy')
    @patch('uforge.application.Api._Users._Appliances.Get')
    @patch('uforge.application.Api._Users._Deployments.Get')
    def test_do_deploy_return_0_when_status_is_running(self, mock_get_deployment, mock_app_get, mock_api_deploy,
                                                        mock_get_deploy_status, mock_api_pimg_getall_for_app):
        # given
        i = self.prepare_image()
        args = self.prepare_image_deploy_command(1234)

        self.prepare_mock_deploy(mock_get_deployment, mock_api_deploy)
        self.prepare_mock_app_get(mock_app_get)
        self.prepare_mock_api_pimg_getall_for_app(mock_api_pimg_getall_for_app)
        self.prepare_mock_deploy_status_running(mock_get_deploy_status)

        # when
        deploy_return = i.do_deploy(args)

        # then
        self.assertEquals(deploy_return, 0)


    @patch('uforge.application.Api._Users._Pimages.Getall')
    @patch('uforge.application.Api._Users._Deployments._Status.Getdeploystatus')
    @patch('uforge.application.Api._Users._Scannedinstances._Scans._Images._Pimages._Deploys.Deploy')
    @patch('uforge.application.Api._Users._Scannedinstances._Scans.Get')
    @patch('uforge.application.Api._Users._Deployments.Get')
    def test_do_deploy_a_scan_return_0_when_status_is_running(self, mock_get_deployment, mock_scan_get, mock_scan_deploy,
                                                        mock_get_deploy_status, prepare_mock_api_pimg_getall_for_scan):
        # given
        i = self.prepare_image()
        args = self.prepare_image_deploy_command(1234)

        self.prepare_mock_deploy(mock_get_deployment, mock_scan_deploy)
        self.prepare_mock_scan_get(mock_scan_get)
        self.prepare_mock_api_pimg_getall_for_scan(prepare_mock_api_pimg_getall_for_scan)
        self.prepare_mock_deploy_status_running(mock_get_deploy_status)

        # when
        deploy_return = i.do_deploy(args)

        # then
        self.assertEquals(deploy_return, 0)

    @patch('uforge.application.Api._Users._Pimages.Getall')
    @patch('uforge.application.Api._Users._Deployments._Status.Getdeploystatus')
    @patch('uforge.application.Api._Users._Appliances._Images._Pimages._Deploys.Deploy')
    @patch('uforge.application.Api._Users._Appliances.Get')
    @patch('uforge.application.Api._Users._Deployments.Get')
    def test_do_deploy_return_1_when_status_is_onfire(self, mock_get_deployment, mock_app_get, mock_api_deploy,
                                                        mock_get_deploy_status, mock_api_pimg_getall_for_app):
        # given
        i = self.prepare_image()
        args = self.prepare_image_deploy_command(1234)

        self.prepare_mock_deploy(mock_get_deployment, mock_api_deploy)
        self.prepare_mock_app_get(mock_app_get)
        self.prepare_mock_api_pimg_getall_for_app(mock_api_pimg_getall_for_app)
        self.prepare_mock_deploy_status_onfire(mock_get_deploy_status)

        # when
        deploy_return = i.do_deploy(args)

        # then
        self.assertEquals(deploy_return, 1)


    def get_deployment(self):
        deployment = Deployment()
        deployment.name = "DeploymentName"
        deployment.applicationId = "id123456789"

        myinstance = InstanceAmazon()
        myinstance.cores = "1"
        myinstance.memory = "1024"
        myinstance.hostname = "example.com"

        myLocation = Location()
        myLocation.provider = "myprovider"
        myinstance.location = myLocation

        deployment.instances = pyxb.BIND()
        deployment.instances._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Instances')
        deployment.instances.append(myinstance)

        return deployment

    def prepare_image_deploy_command(self, id):
         args = "--file tests/integration/data/deploy_aws.yml --publish-id %s" % (id)
         return args

    def prepare_image(self):
        i = image.Image()
        i.api = Api("url", username="username", password="password", headers=None,
                    disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        i.login = "login"
        i.password = "password"
        return i

    def prepare_pimages_from_app(self):
        new_pimages = uforge.publishImages()
        new_pimages.publishImages = pyxb.BIND()

        newImage = PublishImageAws()
        newImage.dbId = 1234
        newImage.imageUri = 'users/guest/appliances/5/images/1234'
        newImage.applianceUri = 'users/guest/appliances/5'
        newImage.status = "complete"
        newImage.status.complete = True
        newImage.targetFormat = uforge.targetFormat()
        newImage.targetFormat.name = "Amazon AWS"

        new_pimages.publishImages.append(newImage)

        return new_pimages

    def prepare_pimages_from_scan(self):
        new_pimages = uforge.publishImages()
        new_pimages.publishImages = pyxb.BIND()

        newImage = PublishImageAws()
        newImage.dbId = 1234
        newImage.imageUri = 'users/guest/scannedinstances/5/scans/12/images/1234'
        newImage.status = "complete"
        newImage.status.complete = True
        newImage.targetFormat = uforge.targetFormat()
        newImage.targetFormat.name = "Amazon AWS"

        new_pimages.publishImages.append(newImage)

        return new_pimages

    def prepare_mock_deploy_status_running(self, mock_get_deploy_status):
        # The mock will return statusStarting on first and second calls, and statusRunning on third call
        statusStarting = OpStatus()
        statusStarting.message = "starting"
        statusRunning = OpStatus()
        statusRunning.message = "running"
        mock_get_deploy_status.side_effect = [statusStarting, statusStarting, statusRunning]

    def prepare_mock_deploy_status_onfire(self, mock_get_deploy_status):
        # The mock will return statusStarting on first and second calls, and statusRunning on third call
        statusStarting = OpStatus()
        statusStarting.message = "starting"
        statusRunning = OpStatus()
        statusRunning.message = "on-fire"
        mock_get_deploy_status.side_effect = [statusStarting, statusStarting, statusRunning]

    def prepare_mock_deploy(self, mock_get_deployment, mock_api_deploy):
        deployment = self.get_deployment()
        mock_api_deploy.return_value = deployment
        mock_get_deployment.return_value = deployment

    def prepare_mock_app_get(self, mock_app_get):
        newAppliance = Appliance()
        mock_app_get.return_value = newAppliance

    def prepare_mock_scan_get(self, mock_scan_get):
        newScan = Scan()
        mock_scan_get.return_value = newScan

    def prepare_mock_api_pimg_getall_for_app(self, mock_api_pimg_getall_for_app):
        new_pimages = self.prepare_pimages_from_app()
        mock_api_pimg_getall_for_app.return_value = new_pimages

    def prepare_mock_api_pimg_getall_for_scan(self, mock_api_pimg_getall_for_scan):
        new_pimages = self.prepare_pimages_from_scan()
        mock_api_pimg_getall_for_scan.return_value = new_pimages
