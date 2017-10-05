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
from hammr.utils.deployment_utils import *


class TestDeployUtils(TestCase):

    def test_build_deployment_openstack_returns_None_when_file_incomplete(self):
        # Given
        file = "tests/integration/data/deploy_openstack_incomplete.yml"

        # When
        return_value = build_deployment_openstack(file, None, None, None)

        #Then
        self.assertEquals(return_value, None)

    def testbuild_deployment_amazon_returns_None_when_file_incomplete(self):
        # Given
        file = "tests/integration/data/deploy_aws_incomplete.yml"

        # When
        return_value = build_deployment_amazon(file)

        #Then
        self.assertEquals(return_value, None)

    def testbuild_deployment_azure_returns_None_when_file_incomplete(self):
        # Given
        file = "tests/integration/data/deploy_azure_incomplete.yml"

        # When
        return_value = build_deployment_azure(file)

        #Then
        self.assertEquals(return_value, None)


