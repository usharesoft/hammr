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
from ussclicore.utils import generics_utils
import hammr.commands.image
from hammr.utils import constants
from uforge.objects.uforge import *
import datetime

class TestDeploy(TestCase):

    @patch('uforge.application.Api._Users._Appliances._Images._Pimages._Deploys.Deploy')
    def test_do_deploy_return_2_when_imageId_is_None(self, mock_api_deploy):
        # given
        i = hammr.commands.image.Image()
        i.api = Api("url", username="username", password="password", headers=None,
                    disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
        i.login = "login"
        i.password = "password"
        deployment = self.get_deployment()
        mock_api_deploy.return_value = deployment
        args = self.prepare_image_deploy_command(None)

        # when
        deploy_return = i.do_deploy(args)

        # then
        self.assertEquals(deploy_return, 2)


    def get_deployment(self):
        deployment = Deployment()
        myinstance = Instance()
        deployment.name = "DeploymentName"
        myinstance.cores = "1"
        myinstance.memory = "1024"
        deployment.instances = pyxb.BIND()
        deployment.instances._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Instances')
        deployment.instances.append(myinstance)

        return deployment


    def prepare_image_deploy_command(self, id):
         args = "--id %s --name DeploymentName" % (id)
         return args
