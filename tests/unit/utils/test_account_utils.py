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

from hammr.utils.account_utils import *

from fileUtils import *

class TestK5(TestCase):
    def test_k5_should_return_cred_account_when_valid_entries(self):
        # given
        account_given = self.build_account("testName", "testLogin", "testPassword")

        # when
        account = k5(account_given)

        # then
        self.assertEqual(account.name, account_given["name"])
        self.assertEqual(account.login, account_given["login"])
        self.assertEqual(account.password, account_given["password"])


    def test_k5_should_return_none_when_missing_name(self):
        # given
        account_given = self.build_account(None, "testLogin", "testPassword")

        # when
        account = k5(account_given)

        # then
        self.assertEqual(None, account)


    def test_k5_should_return_none_when_missing_login(self):
        # given
        account_given = self.build_account("testName", None, "testPassword")

        # when
        account = k5(account_given)

        # then
        self.assertEqual(None, account)


    def test_k5_should_return_none_when_missing_password(self):
        # given
        account_given = self.build_account("testName", "testLogin", None)

        # when
        account = k5(account_given)

        # then
        self.assertEqual(None, account)


    def build_account(self, name, login, password):
        account = {}
        if name is not None: account["name"] = name
        if login is not None: account["login"] = login
        if password is not None: account["password"] = password
        return account


class TestDocker(TestCase):
    def test_docker_should_return_cred_account_when_valid_entries(self):
        # given
        account_given = self.build_account("testName", "testUrl", "testLogin", "testPassword")

        # when
        account = docker(account_given)

        # then
        self.assertEqual(account.name, account_given["name"])
        self.assertEqual(account.endpointUrl, account_given["endpointUrl"])
        self.assertEqual(account.login, account_given["login"])
        self.assertEqual(account.password, account_given["password"])


    def test_docker_should_return_none_when_missing_name(self):
        # given
        accountMocked = self.build_account(None, "testUrl", "testLogin", "testPassword")

        # when
        account = docker(accountMocked)

        # then
        self.assertEqual(None, account)


    def test_docker_should_return_none_when_missing_url(self):
        # given
        accountMocked = self.build_account("testName", None, "testLogin", "testPassword")

        # when
        account = docker(accountMocked)

        # then
        self.assertEqual(None, account)


    def test_docker_should_return_none_when_missing_login(self):
        # given
        accountMocked = self.build_account("testName", "testUrl", None, "testPassword")

        # when
        account = docker(accountMocked)

        # then
        self.assertEqual(account, None)


    def test_docker_should_return_none_when_missing_password(self):
        # given
        accountMocked = self.build_account("testName", "testUrl", "testLogin", None)

        # when
        account = docker(accountMocked)

        # then
        self.assertEqual(account, None)


    def build_account(self, name, endpoint_url, login, password):
        account = {}
        if name is not None: account["name"] = name
        if endpoint_url is not None: account["endpointUrl"] = endpoint_url
        if login is not None: account["login"] = login
        if password is not None: account["password"] = password
        return account


class TestAzureManager(TestCase):

    def test_azure_should_return_cred_account_when_valid_arm_entries(self):
        # given
        account_given = self.build_arm_account("MyAccount", "MyTenantId", "MySubscriptionId", "MyApplicationId", "MyApplicationKey")

        # when
        account = azure(account_given)

        # then
        self.assertNotEqual(account, None)
        self.assertEqual(account.name, account_given["name"])
        self.assertEqual(account.tenantId, account_given["tenantId"])
        self.assertEqual(account.subscriptionId, account_given["subscriptionId"])
        self.assertEqual(account.applicationId, account_given["applicationId"])
        self.assertEqual(account.applicationKey, account_given["applicationKey"])

    def test_azure_should_return_none_when_missing_arm_name(self):
        # given
        accountMocked = self.build_arm_account(None, "MyTenantId", "MySubscriptionId", "MyApplicationId", "MyApplicationKey")

        # when
        account = azure(accountMocked)

        # then
        self.assertEqual(account, None)

    def test_azure_should_return_none_when_missing_arm_tenantId(self):
        # given
        accountMocked = self.build_arm_account("MyAccount", None, "MySubscriptionId", "MyApplicationId", "MyApplicationKey")

        # when
        account = azure(accountMocked)

        # then
        self.assertEqual(account, None)

    def test_azure_should_return_none_when_missing_arm_subscriptionId(self):
        # given
        accountMocked = self.build_arm_account("MyAccount", "MyTenantId", None, "MyApplicationId", "MyApplicationKey")

        # when
        account = azure(accountMocked)

        # then
        self.assertEqual(account, None)

    def test_azure_should_return_none_when_missing_arm_applicationId(self):
        # given
        accountMocked = self.build_arm_account("MyAccount", "MyTenantId", "MySubscriptionId", None, "MyApplicationKey")

        # when
        account = azure(accountMocked)

        # then
        self.assertEqual(account, None)

    def test_azure_should_return_none_when_missing_arm_applicationKey(self):
        # given
        accountMocked = self.build_arm_account("MyAccount", "MyTenantId", "MySubscriptionId",  "MyApplicationId", None)

        # when
        account = azure(accountMocked)

        # then
        self.assertEqual(account, None)

    def build_arm_account(self, name, tenantId, subscriptionId, applicationID, applicationKey):
        account = {}
        if name is not None: account["name"] = name
        if tenantId is not None: account["tenantId"] = tenantId
        if subscriptionId is not None: account["subscriptionId"] = subscriptionId
        if applicationID is not None: account["applicationId"] = applicationID
        if applicationKey is not None: account["applicationKey"] = applicationKey
        return account

    def test_azure_should_return_cred_account_when_valid_azure_classic_entries(self):
        # given
        publishSettingsFileRelativePath = findRelativePathFor("tests/integration/data/pk.pem")
        account_given = self.build_azure_classic_account("MyAccount", publishSettingsFileRelativePath)

        # when
        account = azure(account_given)

        # then
        self.assertNotEqual(account, None)
        self.assertEqual(account.name, account_given["name"])
        self.assertEqual(account.publishsettings, account_given["publishsettings"])

    def test_azure_should_return_none_when_missing_azure_classic_name(self):
        # given
        accountMocked = self.build_azure_classic_account(None, "publishsettings")

        # when
        account = azure(accountMocked)

        # then
        self.assertEqual(account, None)

    def test_azure_should_return_none_when_missing_azure_classic_publishsettings(self):
        # given
        accountMocked = self.build_azure_classic_account("MyAccount", None)

        # when
        account = azure(accountMocked)

        # then
        self.assertEqual(account, None)

    def test_azure_should_return_none_when_azure_classic_publishsettings_file_not_found(self):
        # given
        accountMocked = self.build_azure_classic_account("MyAccount", 'tests/myNonExistingFile.publishsettings')

        # when
        account = azure(accountMocked)

        # then
        self.assertEqual(account, None)

    def build_azure_classic_account(self, name, publishsettings):
        account = {}
        if name is not None: account["name"] = name
        if publishsettings is not None: account["publishsettings"] = publishsettings
        return account