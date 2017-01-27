# Copyright 2007-2017 UShareSoft SAS, All rights reserved
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

from hammr.utils.publish_utils import *


class TestPublishK5(TestCase):
    def test_publish_k5_should_return_publish_image_when_valid_entries(self):
        # given
        builder = self.build_builder("testName", "testDomain", "testProject", "testRegion")

        # when
        pimage = publish_k5vmdk(builder)

        # then
        self.assertEqual(pimage.displayName, builder["displayName"])
        self.assertEqual(pimage.keystoneDomain, builder["domain"])
        self.assertEqual(pimage.keystoneProject, builder["project"])
        self.assertEqual(pimage.publishLocation, builder["region"])


    def test_publish_k5_should_return_none_when_missing_name(self):
        # given
        builder = self.build_builder(None, "testDomain", "testProject", "testRegion")

        # when
        pimage = publish_k5vmdk(builder)

        # then
        self.assertIsNone(pimage)


    def test_publish_k5_should_return_none_when_missing_domain(self):
        # given
        builder = self.build_builder("testName", None, "testProject", "testRegion")

        # when
        pimage = publish_k5vmdk(builder)

        # then
        self.assertIsNone(pimage)


    def test_publish_k5_should_return_none_when_missing_project(self):
        # given
        builder = self.build_builder("testName", "testDomain", None, "testRegion")

        # when
        pimage = publish_k5vmdk(builder)

        # then
        self.assertIsNone(pimage)


    def test_publish_k5_should_return_none_when_missing_region(self):
        # given
        builder = self.build_builder("testName", "testDomain", "testProject", None)

        # when
        pimage = publish_k5vmdk(builder)

        # then
        self.assertIsNone(pimage)


    def build_builder(self, name, domain, project, region):
        builder = {}
        if name is not None: builder["displayName"] = name
        if domain is not None: builder["domain"] = domain
        if project is not None: builder["project"] = project
        if region is not None: builder["region"] = region
        return builder
