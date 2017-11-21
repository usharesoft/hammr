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
        self.assertEqual(pimage, None)


    def test_publish_k5_should_return_none_when_missing_domain(self):
        # given
        builder = self.build_builder("testName", None, "testProject", "testRegion")

        # when
        pimage = publish_k5vmdk(builder)

        # then
        self.assertEqual(pimage, None)


    def test_publish_k5_should_return_none_when_missing_project(self):
        # given
        builder = self.build_builder("testName", "testDomain", None, "testRegion")

        # when
        pimage = publish_k5vmdk(builder)

        # then
        self.assertEqual(pimage, None)


    def test_publish_k5_should_return_none_when_missing_region(self):
        # given
        builder = self.build_builder("testName", "testDomain", "testProject", None)

        # when
        pimage = publish_k5vmdk(builder)

        # then
        self.assertEqual(pimage, None)


    def build_builder(self, name, domain, project, region):
        builder = {}
        if name is not None: builder["displayName"] = name
        if domain is not None: builder["domain"] = domain
        if project is not None: builder["project"] = project
        if region is not None: builder["region"] = region
        return builder


class TestPublishDocker(TestCase):
    def test_publish_docker_should_return_publish_image_when_valid_entries(self):
        # given
        builder = self.build_builder("testNamespace", "testRepositoryName", "testTagName")

        # when
        pimage = publish_docker(builder)

        # then
        self.assertEqual(pimage.namespace, builder["namespace"])
        self.assertEqual(pimage.repositoryName, builder["repositoryName"])
        self.assertEqual(pimage.tagName, builder["tagName"])

    def test_publish_docker_should_return_none_when_missing_namespace(self):
        # given
        builder = self.build_builder(None, "testRepositoryName", "testTagName")

        # when
        pimage = publish_docker(builder)

        # then
        self.assertEqual(pimage, None)

    def test_publish_docker_should_return_none_when_missing_repository_name(self):
        # given
        builder = self.build_builder("testNamespace", None, "testTagName")

        # when
        pimage = publish_docker(builder)

        # then
        self.assertEqual(pimage, None)

    def test_publish_docker_should_return_none_when_missing_tag_name(self):
        # given
        builder = self.build_builder("testNamespace", "testRepositoryName", None)

        # when
        pimage = publish_docker(builder)

        # then
        self.assertEqual(pimage, None)

    def build_builder(self, namespace, repository_name, tag_name):
        builder = {}
        if namespace is not None: builder["namespace"] = namespace
        if repository_name is not None: builder["repositoryName"] = repository_name
        if tag_name is not None: builder["tagName"] = tag_name
        return builder



class TestPublishAzure(TestCase):

    def test_publish_azure_should_return_publish_image_when_valid_arm_entries_withResourceGroup(self):
        # given
        builder = self.build_arm_builder("myStorageAccount", "myContainer", "myBlob", "myDisplayName", "myResourceGroup")

        # when
        pimage = publish_azure(builder)

        # then
        self.assertNotEqual(pimage, None)
        self.assertEqual(pimage.storageAccount, builder["storageAccount"])
        self.assertEqual(pimage.container, builder["container"])
        self.assertEqual(pimage.blob, builder["blob"])
        self.assertEqual(pimage.displayName, builder["displayName"])
        self.assertEqual(pimage.resourceGroup, builder["resourceGroup"])

    def test_publish_azure_should_return_publish_image_when_valid_arm_entries_withoutResourceGroup(self):
        # given
        builder = self.build_arm_builder("myStorageAccount", "myContainer", "myBlob", "myDisplayName", None)

        # when
        pimage = publish_azure(builder)

        # then
        self.assertNotEqual(pimage, None)
        self.assertEqual(pimage.storageAccount, builder["storageAccount"])
        self.assertEqual(pimage.container, builder["container"])
        self.assertEqual(pimage.blob, builder["blob"])
        self.assertEqual(pimage.displayName, builder["displayName"])
        self.assertEqual(pimage.resourceGroup, None)

    def test_publish_azure_should_return_none_when_missing_arm_container(self):
        # given
        builder = self.build_arm_builder("myStorageAccount", None,"myBlob", "myDisplayName", "myResourceGroup")

        # when
        pimage = publish_azure(builder)

        # then
        self.assertEqual(pimage, None)

    def test_publish_azure_should_return_none_when_missing_arm_blob(self):
        # given
        builder = self.build_arm_builder("myStorageAccount", "myContainer", None, "myDisplayName", "myResourceGroup")

        # when
        pimage = publish_azure(builder)

        # then
        self.assertEqual(pimage, None)

    def test_publish_azure_should_return_none_when_missing_arm_displayName(self):
        # given
        builder = self.build_arm_builder("myStorageAccount", "myContainer", "myBlob", None, "myResourceGroup")

        # when
        pimage = publish_azure(builder)

        # then
        self.assertEqual(pimage, None)

    def build_arm_builder(self, storageAccount, container, blob, displayName, resourceGroup):
        builder = {}
        if storageAccount is not None: builder["storageAccount"] = storageAccount
        if container is not None: builder["container"] = container
        if blob is not None: builder["blob"] = blob
        if displayName is not None: builder["displayName"] = displayName
        if resourceGroup is not None: builder["resourceGroup"] = resourceGroup
        return builder

    def test_publish_azure_should_return_publish_image_when_valid_azure_classic_entries_witResourceGroup(self):
        # given
        builder = self.build_azure_classic_builder("myStorageAccount", "myRegion")

        # when
        pimage = publish_azure(builder)

        # then
        self.assertNotEqual(pimage, None)
        self.assertEqual(pimage.storageAccount, builder["storageAccount"])
        self.assertEqual(pimage.region, builder["region"])

    def test_publish_azure_should_return_none_when_missing_azure_classic_storageAccount(self):
        # given
        builder = self.build_azure_classic_builder(None, "myRegion")

        # when
        pimage = publish_azure(builder)

        # then
        self.assertEqual(pimage, None)

    def test_publish_azure_should_return_none_when_missing_azure_classic_region(self):
        # given
        builder = self.build_azure_classic_builder("myStorageAccount", None)

        # when
        pimage = publish_azure(builder)

        # then
        self.assertEqual(pimage, None)

    def build_azure_classic_builder(self, storageAccount, region):
        builder = {}
        if storageAccount is not None: builder["storageAccount"] = storageAccount
        if region is not None: builder["region"] = region
        return builder