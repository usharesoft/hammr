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
from unittest import TestCase
from mock import patch

from uforge.objects import uforge

from hammr.utils.publish_builders import *

class TestPublishK5(TestCase):
    def test_publish_k5_should_return_publish_image_when_valid_entries(self):
        # given
        builder = self.build_builder("testName", "testDomain", "testProject", "testRegion")

        # when
        pimage = publish_k5vmdk(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage.displayName, builder["displayName"])
        self.assertEqual(pimage.keystoneDomain, builder["domain"])
        self.assertEqual(pimage.keystoneProject, builder["project"])
        self.assertEqual(pimage.publishLocation, builder["region"])


    def test_publish_k5_should_return_none_when_missing_name(self):
        # given
        builder = self.build_builder(None, "testDomain", "testProject", "testRegion")

        # when
        pimage = publish_k5vmdk(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage, None)


    def test_publish_k5_should_return_none_when_missing_domain(self):
        # given
        builder = self.build_builder("testName", None, "testProject", "testRegion")

        # when
        pimage = publish_k5vmdk(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage, None)


    def test_publish_k5_should_return_none_when_missing_project(self):
        # given
        builder = self.build_builder("testName", "testDomain", None, "testRegion")

        # when
        pimage = publish_k5vmdk(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage, None)


    def test_publish_k5_should_return_none_when_missing_region(self):
        # given
        builder = self.build_builder("testName", "testDomain", "testProject", None)

        # when
        pimage = publish_k5vmdk(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage, None)


    def build_builder(self, name, domain, project, region):
        builder = {}
        if name is not None: builder["displayName"] = name
        if domain is not None: builder["domain"] = domain
        if project is not None: builder["project"] = project
        if region is not None: builder["region"] = region
        return builder

    def build_cred_account(self):
        cred_accound = uforge.CredAccountK5()
        return cred_accound

class TestPublishDocker(TestCase):
    def test_publish_docker_should_return_publish_image_when_valid_entries(self):
        # given
        builder = self.build_builder("testNamespace", "testRepositoryName", "testTagName")

        # when
        pimage = publish_docker(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage.namespace, builder["namespace"])
        self.assertEqual(pimage.repositoryName, builder["repositoryName"])
        self.assertEqual(pimage.tagName, builder["tagName"])

    def test_publish_docker_should_return_none_when_missing_namespace(self):
        # given
        builder = self.build_builder(None, "testRepositoryName", "testTagName")

        # when
        pimage = publish_docker(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage, None)

    def test_publish_docker_should_return_none_when_missing_repository_name(self):
        # given
        builder = self.build_builder("testNamespace", None, "testTagName")

        # when
        pimage = publish_docker(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage, None)

    def test_publish_docker_should_return_none_when_missing_tag_name(self):
        # given
        builder = self.build_builder("testNamespace", "testRepositoryName", None)

        # when
        pimage = publish_docker(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage, None)

    def build_builder(self, namespace, repository_name, tag_name):
        builder = {}
        if namespace is not None: builder["namespace"] = namespace
        if repository_name is not None: builder["repositoryName"] = repository_name
        if tag_name is not None: builder["tagName"] = tag_name
        return builder

    def build_cred_account(self):
        cred_accound = uforge.CredAccountDocker()
        return cred_accound

class TestPublishOpenShift(TestCase):
    def test_publish_openshift_should_return_publish_image_when_valid_entries(self):
        # given
        builder = self.build_builder("testNamespace", "testRepositoryName", "testTagName")

        # when
        pimage = publish_openshift(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage.namespace, builder["namespace"])
        self.assertEqual(pimage.repositoryName, builder["repositoryName"])
        self.assertEqual(pimage.tagName, builder["tagName"])

    def test_publish_openshift_should_return_none_when_missing_namespace(self):
        # given
        builder = self.build_builder(None, "testRepositoryName", "testTagName")

        # when
        pimage = publish_openshift(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage, None)

    def test_publish_openshift_should_return_none_when_missing_repository_name(self):
        # given
        builder = self.build_builder("testNamespace", None, "testTagName")

        # when
        pimage = publish_openshift(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage, None)

    def test_publish_openshift_should_return_none_when_missing_tag_name(self):
        # given
        builder = self.build_builder("testNamespace", "testRepositoryName", None)

        # when
        pimage = publish_openshift(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage, None)

    def build_builder(self, namespace, repository_name, tag_name):
        builder = {}
        if namespace is not None: builder["namespace"] = namespace
        if repository_name is not None: builder["repositoryName"] = repository_name
        if tag_name is not None: builder["tagName"] = tag_name
        return builder

    def build_cred_account(self):
        cred_accound = uforge.CredAccountOpenShift()
        return cred_accound

class TestPublishAzure(TestCase):

    def test_publish_azure_should_return_publish_image_when_valid_entries_withResourceGroup(self):
        # given
        builder = self.build_azure_builder("myStorageAccount", "myContainer", "myBlob", "myDisplayName", "myResourceGroup")

        # when
        pimage = publish_azure(builder, self.build_cred_account())

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
        pimage = publish_azure(builder, self.build_cred_account())

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
        pimage = publish_azure(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage, None)

    def test_publish_azure_should_return_none_when_missing_blob(self):
        # given
        builder = self.build_azure_builder("myStorageAccount", "myContainer", None, "myDisplayName", "myResourceGroup")

        # when
        pimage = publish_azure(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage, None)

    def test_publish_azure_should_return_none_when_missing_displayName(self):
        # given
        builder = self.build_azure_builder("myStorageAccount", "myContainer", "myBlob", None, "myResourceGroup")

        # when
        pimage = publish_azure(builder, self.build_cred_account())

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

    def build_cred_account(self):
        cred_accound = uforge.CredAccountAzure()
        return cred_accound

class TestPublishCloudStack(TestCase):

    def test_publish_cloudstack_should_return_publish_image_when_valid_entries(self):
        # given
        builder = self.build_cloudstack_builder("myImageName", "myZone", "myDescription")

        # when
        pimage = publish_cloudstack(builder, self.build_cred_account())

        # then
        self.assertNotEqual(pimage, None)
        self.assertEqual(pimage.displayName, builder["imageName"])
        self.assertEqual(pimage.zoneName, builder["zone"])
        self.assertEqual(pimage.description, builder["description"])

    def test_publish_cloudstack_should_return_none_when_missing_image_name(self):
        # given
        builder = self.build_cloudstack_builder(None, "myZone", "myDescription")

        # when
        pimage = publish_cloudstack(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage, None)

    def test_publish_cloudstack_should_return_none_when_missing_zone(self):
        # given
        builder = self.build_cloudstack_builder("myImageName", None, "myDescription")

        # when
        pimage = publish_cloudstack(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage, None)

    def test_publish_cloudstack_should_return_none_when_missing_description(self):
        # give
        builder = self.build_cloudstack_builder("myImageName", "myZone", None)

        # when
        pimage = publish_cloudstack(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage, None)


    def build_cloudstack_builder(self, image_name, zone, description):
        builder = {}
        if image_name is not None: builder["imageName"] = image_name
        if zone is not None: builder["zone"] = zone
        if description is not None: builder["description"] = description
        return builder

    def build_cred_account(self):
        cred_accound = uforge.CredAccountCloudStack()
        return cred_accound

class TestPublishOracle(TestCase):
    def test_publish_oracle_should_return_publish_image_when_valid_entries(self):
        # given
        builder = self.build_oracle_builder("displayName", "computeEndPoint")

        # when
        pimage = publish_oracleraw(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage.displayName, builder["displayName"])
        self.assertEqual(pimage.computeEndPoint, builder["computeEndPoint"])

    def test_publish_oracle_should_return_none_when_missing_display_name(self):
        # given
        builder = self.build_oracle_builder(None, "computeEndPoint")

        # when
        pimage = publish_oracleraw(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage, None)

    def test_publish_oracle_should_return_none_when_missing_compute_end_point(self):
        # given
        builder = self.build_oracle_builder("displayName", None)

        # when
        pimage = publish_oracleraw(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage, None)

    def build_oracle_builder(self, display_name, compute_end_point):
        builder = {}
        if display_name is not None: builder["displayName"] = display_name
        if compute_end_point is not None: builder["computeEndPoint"] = compute_end_point
        return builder

    def build_cred_account(self):
        cred_accound = uforge.CredAccountOracle()
        return cred_accound


class TestPublishOutscale(TestCase):
    def test_publish_outscale_should_return_publish_image_when_valid_entries(self):
        # given
        builder = self.build_outscale_builder("myRegion")

        # when
        pimage = publish_outscale(builder, self.build_cred_account())

        # then
        self.assertNotEqual(pimage, None)
        self.assertNotEqual(pimage.region, None)
        self.assertEqual(pimage.region, builder["region"])

    def test_publish_outscale_should_return_none_when_missing_region(self):
        # given
        builder = self.build_outscale_builder(None)

        # when
        pimage = publish_outscale(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage, None)

    def build_outscale_builder(self, region):
        builder = {}
        if region is not None:
            builder["region"] = region
        return builder

    def build_cred_account(self):
        cred_accound = uforge.CredAccountOutscale()
        return cred_accound

class TestPublishGoogle(TestCase):
    def test_publish_google_should_return_publish_image_when_valid_entries(self):
        # given
        builder = self.build_google_builder("computeZone", "bucketLocation", "bucket", "projectId", "storageClass", "diskNamePrefix")
        print(builder)

        # when
        pimage = publish_google(builder, self.build_cred_account())

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
        pimage = publish_google(builder, self.build_cred_account())

        # then
        self.assertEqual(pimage, None)

    def test_publish_google_should_return_none_when_missing_project_id(self):
        # given
        builder = self.build_google_builder("computeZone", "bucketLocation", "bucket", None, "storageClass", "diskNamePrefix")

        # when
        pimage = publish_google(builder, self.build_cred_account())

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

    def build_cred_account(self):
        cred_accound = uforge.CredAccountGoogle()
        return cred_accound

class TestPublishOpenStack(TestCase):
    def test_publish_openstack_should_return_publish_image_when_valid_entries_for_v3(self):
        # given
        builder = self.build_builder_v3("testDisplayName", "testKeystoneDomain", "testKeystoneProject")

        # when
        pimage = publish_openstack(builder, self.build_cred_account_v3())

        # then
        self.assertEqual(pimage.displayName, builder["displayName"])
        self.assertEqual(pimage.keystoneDomain, builder["keystoneDomain"])
        self.assertEqual(pimage.keystoneProject, builder["keystoneProject"])

    def test_publish_openstack_should_return_none_when_missing_keystoneDomain_for_v3(self):
        # given
        builder = self.build_builder_v3("testDisplayName", None, "testKeystoneProject")

        # when
        pimage = publish_openstack(builder, self.build_cred_account_v3())

        # then
        self.assertEqual(pimage, None)

    def test_publish_openstack_should_return_none_when_missing_keystoneDomain_for_v3(self):
        # given
        builder = self.build_builder_v3("testDisplayName", "testKeystoneDomain", None)

        # when
        pimage = publish_openstack(builder, self.build_cred_account_v3())

        # then
        self.assertEqual(pimage, None)

    def test_publish_openstack_should_return_none_when_missing_displayName_for_v3(self):
        # given
        builder = self.build_builder_v3(None, "testKeystoneDomain", "testKeystoneProject")

        # when
        pimage = publish_openstack(builder, self.build_cred_account_v3())

        # then
        self.assertEqual(pimage, None)

    def test_publish_openstack_should_return_publish_image_when_valid_entries_for_v2(self):
        # given
        builder = self.build_builder_v2("testDisplayName", "testTenantName")

        # when
        pimage = publish_openstack(builder, self.build_cred_account_v2())

        # then
        self.assertEqual(pimage.displayName, builder["displayName"])
        self.assertEqual(pimage.tenantName, builder["tenantName"])

    def test_publish_openstack_should_return_none_when_missing_tenantName_for_v2(self):
        # given
        builder = self.build_builder_v2("testDisplayName", None)

        # when
        pimage = publish_openstack(builder, self.build_cred_account_v2())

        # then
        self.assertEqual(pimage, None)

    def test_publish_openstack_should_return_none_when_missing_displayName_for_v2(self):
        # given
        builder = self.build_builder_v2(None, "testTenantName")

        # when
        pimage = publish_openstack(builder, self.build_cred_account_v2())

        # then
        self.assertEqual(pimage, None)

    @patch("hammr.utils.publish_builders.publish_openstack")
    def test_publish_openstackqcow2_should_call_publish_openstack_with_same_parameters(self, mock_publish_openstack):
        # given
        builder = self.build_builder("testDisplayNameqcow2")
        cred_account = self.build_cred_account()

        # when
        publish_openstackqcow2(builder, cred_account)

        # then
        mock_publish_openstack.assert_called_with(builder, cred_account)

    @patch("hammr.utils.publish_builders.publish_openstack")
    def test_publish_openstackvhd_should_call_publish_openstack_with_same_parameters(self, mock_publish_openstack):
        # given
        builder = self.build_builder("testDisplayNamevhd")
        cred_account = self.build_cred_account()

        # when
        publish_openstackvhd(builder, cred_account)

        # then
        mock_publish_openstack.assert_called_with(builder, cred_account)

    @patch("hammr.utils.publish_builders.publish_openstack")
    def test_publish_openstackvmdk_should_call_publish_openstack_with_same_parameters(self, mock_publish_openstack):
        # given
        builder = self.build_builder("testDisplayNamevmdk")
        cred_account = self.build_cred_account()

        # when
        publish_openstackvmdk(builder, cred_account)

        # then
        mock_publish_openstack.assert_called_with(builder, cred_account)

    @patch("hammr.utils.publish_builders.publish_openstack")
    def test_publish_openstackvdi_should_call_publish_openstack_with_same_parameters(self, mock_publish_openstack):
        # given
        builder = self.build_builder("testDisplayNamevdi")
        cred_account = self.build_cred_account()

        # when
        publish_openstackvdi(builder, cred_account)

        # then
        mock_publish_openstack.assert_called_with(builder, cred_account)

    def build_builder(self, display_name):
        builder = {}
        if display_name is not None: builder["displayName"] = display_name
        return builder

    def build_builder_v2(self, display_name, tenant_name):
        builder = self.build_builder(display_name)
        if tenant_name is not None: builder["tenantName"] = tenant_name
        return builder

    def build_builder_v3(self, display_name, keystone_domain, keystone_project):
        builder = self.build_builder(display_name)
        if keystone_domain is not None: builder["keystoneDomain"] = keystone_domain
        if keystone_project is not None: builder["keystoneProject"] = keystone_project
        return builder

    def build_cred_account(self):
        cred_accound = uforge.CredAccountOpenStack()
        return cred_accound

    def build_cred_account_v2(self):
        cred_accound = self.build_cred_account()
        cred_accound.keystoneVersion = "v2.0"
        return cred_accound

    def build_cred_account_v3(self):
        cred_accound = self.build_cred_account()
        cred_accound.keystoneVersion = "v3"
        return cred_accound