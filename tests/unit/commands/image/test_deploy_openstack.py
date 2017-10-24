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
from tests.unit.commands.image.deploy_test_utils import prepare_image, prepare_mock_deploy
from tests.unit.utils.file_utils import findRelativePathFor
from tests.unit.utils.pyxb_utils import get_pyXB_anon_type_for_list_attrb, get_pyXB_anon_type_for_simple_attrb


class TestDeployOpenStack(TestCase):

    @patch('uforge.application.Api._Users._Pimages.Getall')
    @patch('uforge.application.Api._Users._Deployments._Status.Getdeploystatus')
    @patch('uforge.application.Api._Users._Appliances._Images._Pimages._Deploys.Deploy')
    @patch('uforge.application.Api._Users._Appliances.Get')
    @patch('uforge.application.Api._Users._Deployments.Get')
    @patch('uforge.application.Api._Users._Appliances._Images._Pimages._Accounts._Resources.Getaccountresources')
    def test_do_deploy_openstack_return_0_when_status_is_running(self, mock_app_get_account_resources, mock_get_deployment,
                                                                 mock_app_get, mock_api_deploy, mock_get_deploy_status,
                                                                 mock_api_pimg_getall_for_app):
        # given
        i = prepare_image()
        args = self.prepare_image_deploy_command_openstack(1234)

        deployment = self.get_deployment_openstack()
        pimages = self.prepare_openstack_pimages_from_app()

        prepare_mock_deploy(deployment, pimages, Appliance(), ["starting", "starting", "running"],
                        mock_get_deployment, mock_app_get, mock_api_deploy, mock_get_deploy_status,
                        mock_api_pimg_getall_for_app)

        self.mock_openstack_retrieval(mock_app_get_account_resources)

        # when
        deploy_return = i.do_deploy(args)

        # then
        self.assertEquals(deploy_return, 0)

    @patch('uforge.application.Api._Users._Pimages.Getall')
    @patch('uforge.application.Api._Users._Deployments._Status.Getdeploystatus')
    @patch('uforge.application.Api._Users._Scannedinstances._Scans._Images._Pimages._Deploys.Deploy')
    @patch('uforge.application.Api._Users._Scannedinstances._Scans.Get')
    @patch('uforge.application.Api._Users._Deployments.Get')
    @patch('uforge.application.Api._Users._Scannedinstances._Scans._Images._Pimages._Accounts._Resources.Getaccountresources')
    def test_do_deploy_openstack_a_scan_return_0_when_status_is_running(self, mock_scan_get_account_resources,
                                                        mock_get_deployment, mock_scan_get, mock_scan_deploy,
                                                        mock_get_deploy_status, prepare_mock_api_pimg_getall_for_scan):
        # given
        i = prepare_image()
        args = self.prepare_image_deploy_command_openstack(1234)

        deployment = self.get_deployment_openstack()
        pimages = self.prepare_openstack_pimages_from_scan()

        prepare_mock_deploy(deployment, pimages, Scan(), ["starting", "starting", "running"],
                        mock_get_deployment, mock_scan_get, mock_scan_deploy, mock_get_deploy_status,
                        prepare_mock_api_pimg_getall_for_scan)

        self.mock_openstack_retrieval(mock_scan_get_account_resources)

        # when
        deploy_return = i.do_deploy(args)

        # then
        self.assertEquals(deploy_return, 0)

    @patch('uforge.application.Api._Users._Pimages.Getall')
    @patch('uforge.application.Api._Users._Deployments._Status.Getdeploystatus')
    @patch('uforge.application.Api._Users._Appliances._Images._Pimages._Deploys.Deploy')
    @patch('uforge.application.Api._Users._Appliances.Get')
    @patch('uforge.application.Api._Users._Deployments.Get')
    @patch('uforge.application.Api._Users._Appliances._Images._Pimages._Accounts._Resources.Getaccountresources')
    def test_do_deploy_openstack_return_1_when_status_is_onfire(self, mock_app_get_account_resources, mock_get_deployment,
                                                                mock_app_get, mock_api_deploy, mock_get_deploy_status,
                                                                mock_api_pimg_getall_for_app):
        # given
        i = prepare_image()
        args = self.prepare_image_deploy_command_openstack(1234)

        deployment = self.get_deployment_openstack()
        pimages = self.prepare_openstack_pimages_from_app()

        prepare_mock_deploy(deployment, pimages, Appliance(), ["starting", "starting", "on-fire"],
                        mock_get_deployment, mock_app_get, mock_api_deploy, mock_get_deploy_status,
                        mock_api_pimg_getall_for_app)

        self.mock_openstack_retrieval(mock_app_get_account_resources)

        # when
        deploy_return = i.do_deploy(args)

        # then
        self.assertEquals(deploy_return, 1)

    def get_deployment_openstack(self):
        deployment = Deployment()
        deployment.name = "DeploymentName"
        deployment.applicationId = "id123456789"

        myinstance = InstanceOpenStack()
        myinstance.cores = "1"
        myinstance.memory = "1024"
        myinstance.hostname = "example.com"
        myinstance.userName = "myName"
        myinstance.userSshKey = "mySshKey"

        myLocation = Location()
        myLocation.provider = "myprovider"
        myinstance.location = myLocation
        myinstance.cloudProvider = "openstack"

        deployment.instances = pyxb.BIND()
        deployment.instances._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Instances')
        deployment.instances.append(myinstance)

        return deployment

    def prepare_image_deploy_command_openstack(self, id):
         args = "--file %s --publish-id %s" % (findRelativePathFor("tests/integration/data/deploy_openstack.yml"), id)
         return args

    def prepare_openstack_credaccount(self):
        credAccount = CredAccountOpenStack()
        credAccount.dbId = 2462
        credAccount.name = 'OpenStackCredAccount'
        credAccount.glanceUrl = ''
        credAccount.keystoneUrl = ''
        credAccount.keystoneVersion = ''
        credAccount.login = 'usharesoft'
        credAccount.password = 'somepassword'

        return credAccount

    def prepare_openstack_pimages_from_app(self):
        new_pimages = uforge.publishImages()
        new_pimages.publishImages = pyxb.BIND()

        newImage = PublishImageOpenStack()
        newImage.dbId = 1234
        newImage.imageUri = 'users/guest/appliances/5/images/116'
        newImage.applianceUri = 'users/guest/appliances/5'
        newImage.status = "complete"
        newImage.status.complete = True
        newImage.targetFormat = uforge.targetFormat()
        newImage.targetFormat.name = "OpenStack"
        newImage.uri = "users/guest/appliances/5/images/116/pimages/1234"
        newImage.credAccount = self.prepare_openstack_credaccount();

        new_pimages.publishImages.append(newImage)

        return new_pimages

    def prepare_openstack_pimages_from_scan(self):
        new_pimages = uforge.publishImages()
        new_pimages.publishImages = pyxb.BIND()

        newImage = PublishImageOpenStack()
        newImage.dbId = 1234
        newImage.imageUri = 'users/guest/scannedinstances/5/scans/12/images/116'
        newImage.status = "complete"
        newImage.status.complete = True
        newImage.targetFormat = uforge.targetFormat()
        newImage.targetFormat.name = "OpenStack"
        newImage.uri = "users/guest/scannedinstances/5/scans/12/images/116/pimages/1234"
        newImage.credAccount = self.prepare_openstack_credaccount();

        new_pimages.publishImages.append(newImage)

        return new_pimages

    def mock_openstack_retrieval(self, mock_get_account_resources):

        credAccountResources = CredAccountResources()
        mock_get_account_resources.return_value = credAccountResources

        openstackResources = OpenstackResources()
        credAccountResources.cloudResources = openstackResources
        openstackResources.tenants = pyxb.BIND()

        tenant_type = get_pyXB_anon_type_for_list_attrb(openstackResources.tenants.tenant)
        tenant = tenant_type()
        openstackResources.tenants.tenant.append(tenant)

        regions_type = get_pyXB_anon_type_for_list_attrb(tenant.regionsEntities)
        regions = regions_type()
        tenant.regionsEntities.append(regions)

        region_type = get_pyXB_anon_type_for_list_attrb(regions.regionEntities)
        region = region_type()
        regions.regionEntities.append(region)
        region.regionName = "GRA1"

        flavors_type = get_pyXB_anon_type_for_simple_attrb(region, "flavors")
        flavors = flavors_type()
        region.flavors = flavors

        networks_type = get_pyXB_anon_type_for_simple_attrb(region, "networks")
        networks = networks_type()
        region.networks = networks

        flavor_type = get_pyXB_anon_type_for_list_attrb(flavors.flavor)
        flavor = flavor_type()
        flavors.flavor.append(flavor)
        flavor.id = "98c1e679-5f2c-4069-b4ea-4a4f7179b758"
        flavor.name = "myFlavor"

        network_type = get_pyXB_anon_type_for_list_attrb(networks.network)
        network = network_type()
        networks.network.append(network)
        network.id = "8d3e91fd-c533-418f-8578-4252de201489"
        network.name = "myNetwork"