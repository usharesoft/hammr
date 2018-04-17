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

from hammr.utils.publish_builders import *

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

    def test_publish_azure_should_return_publish_image_when_valid_entries_withResourceGroup(self):
        # given
        builder = self.build_azure_builder("myStorageAccount", "myContainer", "myBlob", "myDisplayName", "myResourceGroup")

        # when
        pimage = publish_azure(builder)

        # then
        self.assertNotEqual(pimage, None)
        self.assertEqual(pimage.storageAccount, builder["storageAccount"])
        self.assertEqual(pimage.container, builder["container"])
        self.assertEqual(pimage.blob, builder["blob"])
        self.assertEqual(pimage.displayName, builder["displayName"])
        self.assertEqual(pimage.resourceGroup, builder["resourceGroup"])

    def test_publish_azure_should_return_publish_image_when_valid_entries_withoutResourceGroup(self):
        # given
        builder = self.build_azure_builder("myStorageAccount", "myContainer", "myBlob", "myDisplayName", None)

        # when
        pimage = publish_azure(builder)

        # then
        self.assertNotEqual(pimage, None)
        self.assertEqual(pimage.storageAccount, builder["storageAccount"])
        self.assertEqual(pimage.container, builder["container"])
        self.assertEqual(pimage.blob, builder["blob"])
        self.assertEqual(pimage.displayName, builder["displayName"])
        self.assertEqual(pimage.resourceGroup, None)

    def test_publish_azure_should_return_none_when_missing_container(self):
        # given
        builder = self.build_azure_builder("myStorageAccount", None,"myBlob", "myDisplayName", "myResourceGroup")

        # when
        pimage = publish_azure(builder)

        # then
        self.assertEqual(pimage, None)

    def test_publish_azure_should_return_none_when_missing_blob(self):
        # given
        builder = self.build_azure_builder("myStorageAccount", "myContainer", None, "myDisplayName", "myResourceGroup")

        # when
        pimage = publish_azure(builder)

        # then
        self.assertEqual(pimage, None)

    def test_publish_azure_should_return_none_when_missing_displayName(self):
        # given
        builder = self.build_azure_builder("myStorageAccount", "myContainer", "myBlob", None, "myResourceGroup")

        # when
        pimage = publish_azure(builder)

        # then
        self.assertEqual(pimage, None)

    def build_azure_builder(self, storageAccount, container, blob, displayName, resourceGroup):
        builder = {}
        if storageAccount is not None: builder["storageAccount"] = storageAccount
        if container is not None: builder["container"] = container
        if blob is not None: builder["blob"] = blob
        if displayName is not None: builder["displayName"] = displayName
        if resourceGroup is not None: builder["resourceGroup"] = resourceGroup
        return builder

class TestPublishCloudStack(TestCase):

    def test_publish_cloudstack_should_return_publish_image_when_valid_entries(self):
        # given
        builder = self.build_cloudstack_builder("myImageName", "myZone", "myDescription")

        # when
        pimage = publish_cloudstack(builder)

        # then
        self.assertNotEqual(pimage, None)
        self.assertEqual(pimage.displayName, builder["imageName"])
        self.assertEqual(pimage.zoneName, builder["zone"])
        self.assertEqual(pimage.description, builder["description"])

    def test_publish_cloudstack_should_return_none_when_missing_image_name(self):
        # given
        builder = self.build_cloudstack_builder(None, "myZone", "myDescription")

        # when
        pimage = publish_cloudstack(builder)

        # then
        self.assertEqual(pimage, None)

    def test_publish_cloudstack_should_return_none_when_missing_zone(self):
        # given
        builder = self.build_cloudstack_builder("myImageName", None, "myDescription")

        # when
        pimage = publish_cloudstack(builder)

        # then
        self.assertEqual(pimage, None)

    def test_publish_cloudstack_should_return_none_when_missing_description(self):
        # give
        builder = self.build_cloudstack_builder("myImageName", "myZone", None)

        # when
        pimage = publish_cloudstack(builder)

        # then
        self.assertEqual(pimage, None)


    def build_cloudstack_builder(self, image_name, zone, description):
        builder = {}
        if image_name is not None: builder["imageName"] = image_name
        if zone is not None: builder["zone"] = zone
        if description is not None: builder["description"] = description
        return builder

class TestPublishOracle(TestCase):
    def test_publish_oracle_should_return_publish_image_when_valid_entries(self):
        # given
        builder = self.build_oracle_builder("displayName", "computeEndPoint")

        # when
        pimage = publish_oracleraw(builder)

        # then
        self.assertEqual(pimage.displayName, builder["displayName"])
        self.assertEqual(pimage.computeEndPoint, builder["computeEndPoint"])

    def test_publish_oracle_should_return_none_when_missing_display_name(self):
        # given
        builder = self.build_oracle_builder(None, "computeEndPoint")

        # when
        pimage = publish_oracleraw(builder)

        # then
        self.assertEqual(pimage, None)

    def test_publish_oracle_should_return_none_when_missing_compute_end_point(self):
        # given
        builder = self.build_oracle_builder("displayName", None)

        # when
        pimage = publish_oracleraw(builder)

        # then
        self.assertEqual(pimage, None)

    def build_oracle_builder(self, display_name, compute_end_point):
        builder = {}
        if display_name is not None: builder["displayName"] = display_name
        if compute_end_point is not None: builder["computeEndPoint"] = compute_end_point
        return builder


class TestPublishOutscale(TestCase):
    def test_publish_outscale_should_return_publish_image_when_valid_entries(self):
        # given
        builder = self.build_outscale_builder("myRegion")

        # when
        pimage = publish_outscale(builder)

        # then
        self.assertNotEqual(pimage, None)
        self.assertNotEqual(pimage.region, None)
        self.assertEqual(pimage.region, builder["region"])

    def test_publish_outscale_should_return_none_when_missing_region(self):
        # given
        builder = self.build_outscale_builder(None)

        # when
        pimage = publish_outscale(builder)

        # then
        self.assertEqual(pimage, None)

    def build_outscale_builder(self, region):
        builder = {}
        if region is not None:
            builder["region"] = region
        return builder

class TestPublishGoogle(TestCase):
    def test_publish_google_should_return_publish_image_when_valid_entries(self):
        # given
        builder = self.build_google_builder("computeZone", "bucketLocation", "bucket", "projectId", "storageClass", "diskNamePrefix")
        print(builder)

        # when
        pimage = publish_google(builder)

        # then
        self.assertEqual(pimage.zoneName, builder["computeZone"])
        self.assertEqual(pimage.bucketLocation, builder["bucketLocation"])
        self.assertEqual(pimage.bucket, builder["bucket"])
        self.assertEqual(pimage.projectId, builder["projectId"])
        self.assertEqual(pimage.storageClass, builder["storageClass"])
        self.assertEqual(pimage.diskNamePrefix, builder["diskNamePrefix"])

    def test_publish_google_should_return_none_when_missing_bucket(self):
        # given
        builder = self.build_google_builder("computeZone", "bucketLocation", None, "projectId", "storageClass", "diskNamePrefix")

        # when
        pimage = publish_google(builder)

        # then
        self.assertEqual(pimage, None)

    def test_publish_google_should_return_none_when_missing_project_id(self):
        # given
        builder = self.build_google_builder("computeZone", "bucketLocation", "bucket", None, "storageClass", "diskNamePrefix")

        # when
        pimage = publish_google(builder)

        # then
        self.assertEqual(pimage, None)

    def build_google_builder(self, compute_zone, bucket_location, bucket, project_id, storage_class, disk_name_prefix):
        builder = {}
        if compute_zone is not None: builder["computeZone"] = compute_zone
        if bucket_location is not None: builder["bucketLocation"] = bucket_location
        if bucket is not None: builder["bucket"] = bucket
        if project_id is not None: builder["projectId"] = project_id
        if storage_class is not None: builder["storageClass"] = storage_class
        if disk_name_prefix is not None: builder["diskNamePrefix"] = disk_name_prefix

        return builder
