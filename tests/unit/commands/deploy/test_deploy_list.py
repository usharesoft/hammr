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
from uforge.objects import uforge
from uforge.objects.uforge import *

from hammr.commands.deploy import deploy
from hammr.utils import constants

class TestDeployList(TestCase):
    # URL: users/{uid}/deployments/{did}/status
    @patch('uforge.application.Api._Users._Deployments.Getall')
    @patch('texttable.Texttable.add_row')
    def test_do_list_gives_correct_number_of_deployments(self, mock_table_add_row, mock_api_deployments_getall):
        # given
        i = deploy.Deploy()
        i.api = Api("url", username="username", password="password", headers=None,
                    disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        i.login = "login"
        i.password = "password"
        self.create_deployments(mock_api_deployments_getall)

        # when
        i.do_list(None)

        # then
        self.assertEquals(mock_table_add_row.call_count, 1)

    def create_deployments(self,mock_api_deployments_getall):
        new_deployments = uforge.deployments()
        new_deployments.deployments = pyxb.BIND()

        newdeployment = self.create_deployment()
        new_deployments.deployments.append(newdeployment)

        mock_api_deployments_getall.return_value = new_deployments

    def create_deployment(self):
        deployment = Deployment()
        deployment.name = "DeploymentName"
        deployment.applicationId = "id123456789"
        deployment.state = "running"

        myinstance = Instance()
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
