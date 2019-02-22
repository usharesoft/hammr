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

from hammr.utils.account_utils import *

from file_utils import *

class TestK5(TestCase):

    @patch("hammr.utils.account_utils.k5")
    def test_fill_k5_should_return_cred_account_when_valid_entries(self, mock_k5):
        # given
        account_given = self.build_account("testName", "testLogin", "testPassword")

        # when
        account = fill_k5(account_given)

        # then
        self.assertEquals(mock_k5.call_count, 1)
        self.assertEqual(account.name, account_given["name"])
        self.assertEqual(account.login, account_given["login"])
        self.assertEqual(account.password, account_given["password"])


    def test_fill_k5_should_return_none_when_missing_name(self):
        # given
        account_given = self.build_account(None, "testLogin", "testPassword")

        # when
        account = fill_k5(account_given)

        # then
        self.assertEqual(None, account)


    def test_fill_k5_should_return_none_when_missing_login(self):
        # given
        account_given = self.build_account("testName", None, "testPassword")

        # when
        account = fill_k5(account_given)

        # then
        self.assertEqual(None, account)


    def test_fill_k5_should_return_none_when_missing_password(self):
        # given
        account_given = self.build_account("testName", "testLogin", None)

        # when
        account = fill_k5(account_given)

        # then
        self.assertEqual(None, account)


    def build_account(self, name, login, password):
        account = {}
        if name is not None: account["name"] = name
        if login is not None: account["login"] = login
        if password is not None: account["password"] = password
        return account


class TestDocker(TestCase):

    @patch("hammr.utils.account_utils.docker")
    def test_fill_docker_should_return_cred_account_when_valid_entries(self, mock_docker):
        # given
        account_given = self.build_account("testName", "testUrl", "testLogin", "testPassword")

        # when
        account = fill_docker(account_given)

        # then
        self.assertEquals(mock_docker.call_count, 1)
        self.assertEqual(account.name, account_given["name"])
        self.assertEqual(account.endpointUrl, account_given["endpointUrl"])
        self.assertEqual(account.login, account_given["login"])
        self.assertEqual(account.password, account_given["password"])


    def test_fill_docker_should_return_none_when_missing_name(self):
        # given
        accountMocked = self.build_account(None, "testUrl", "testLogin", "testPassword")

        # when
        account = fill_docker(accountMocked)

        # then
        self.assertEqual(None, account)


    def test_fill_docker_should_return_none_when_missing_url(self):
        # given
        accountMocked = self.build_account("testName", None, "testLogin", "testPassword")

        # when
        account = fill_docker(accountMocked)

        # then
        self.assertEqual(None, account)


    def test_fill_docker_should_return_none_when_missing_login(self):
        # given
        accountMocked = self.build_account("testName", "testUrl", None, "testPassword")

        # when
        account = fill_docker(accountMocked)

        # then
        self.assertEqual(account, None)


    def test_fill_docker_should_return_none_when_missing_password(self):
        # given
        accountMocked = self.build_account("testName", "testUrl", "testLogin", None)

        # when
        account = fill_docker(accountMocked)

        # then
        self.assertEqual(account, None)


    def build_account(self, name, endpoint_url, login, password):
        account = {}
        if name is not None: account["name"] = name
        if endpoint_url is not None: account["endpointUrl"] = endpoint_url
        if login is not None: account["login"] = login
        if password is not None: account["password"] = password
        return account

class TestOpenShift(TestCase):

    @patch("hammr.utils.account_utils.openshift")
    def test_fill_openshift_should_return_cred_account_when_valid_entries(self, mock_openshift):
        # given
        account_given = self.build_account("testName", "testUrl", "testToken")

        # when
        account = fill_openshift(account_given)

        # then
        self.assertEquals(mock_openshift.call_count, 1)
        self.assertEqual(account.name, account_given["name"])
        self.assertEqual(account.registryUrl, account_given["registryUrl"])
        self.assertEqual(account.token, account_given["token"])


    def test_fill_openshift_should_return_none_when_missing_name(self):
        # given
        accountMocked = self.build_account(None, "testUrl", "testToken")

        # when
        account = fill_openshift(accountMocked)

        # then
        self.assertEqual(None, account)


    def test_fill_openshift_should_return_none_when_missing_url(self):
        # given
        accountMocked = self.build_account("testName", None, "testToken")

        # when
        account = fill_openshift(accountMocked)

        # then
        self.assertEqual(None, account)


    def test_fill_openshift_should_return_none_when_missing_token(self):
        # given
        accountMocked = self.build_account("testName", "testUrl", None)

        # when
        account = fill_openshift(accountMocked)

        # then
        self.assertEqual(account, None)

    def build_account(self, name, registryUrl, token):
        account = {}
        if name is not None: account["name"] = name
        if registryUrl is not None: account["registryUrl"] = registryUrl
        if token is not None: account["token"] = token
        return account

class TestAzure(TestCase):

    @patch("hammr.utils.account_utils.azure")
    def test_fill_azure_should_return_cred_account_when_valid_entries(self, mock_azure):
        # given
        account_given = self.build_azure_account("MyAccount", "MyTenantId", "MySubscriptionId", "MyApplicationId", "MyApplicationKey")

        # when
        account = fill_azure(account_given)

        # then
        self.assertEquals(mock_azure.call_count, 1)
        self.assertNotEqual(account, None)
        self.assertEqual(account.name, account_given["name"])
        self.assertEqual(account.tenantId, account_given["tenantId"])
        self.assertEqual(account.subscriptionId, account_given["subscriptionId"])
        self.assertEqual(account.applicationId, account_given["applicationId"])
        self.assertEqual(account.applicationKey, account_given["applicationKey"])

    def test_fill_azure_should_return_none_when_missing_name(self):
        # given
        accountMocked = self.build_azure_account(None, "MyTenantId", "MySubscriptionId", "MyApplicationId", "MyApplicationKey")

        # when
        account = fill_azure(accountMocked)

        # then
        self.assertEqual(account, None)

    def test_fill_azure_should_return_none_when_missing_tenantId(self):
        # given
        accountMocked = self.build_azure_account("MyAccount", None, "MySubscriptionId", "MyApplicationId", "MyApplicationKey")

        # when
        account = fill_azure(accountMocked)

        # then
        self.assertEqual(account, None)

    def test_fill_azure_should_return_none_when_missing_subscriptionId(self):
        # given
        accountMocked = self.build_azure_account("MyAccount", "MyTenantId", None, "MyApplicationId", "MyApplicationKey")

        # when
        account = fill_azure(accountMocked)

        # then
        self.assertEqual(account, None)

    def test_fill_azure_should_return_none_when_missing_applicationId(self):
        # given
        accountMocked = self.build_azure_account("MyAccount", "MyTenantId", "MySubscriptionId", None, "MyApplicationKey")

        # when
        account = fill_azure(accountMocked)

        # then
        self.assertEqual(account, None)

    def test_fill_azure_should_return_none_when_missing_applicationKey(self):
        # given
        accountMocked = self.build_azure_account("MyAccount", "MyTenantId", "MySubscriptionId", "MyApplicationId", None)

        # when
        account = fill_azure(accountMocked)

        # then
        self.assertEqual(account, None)

    def build_azure_account(self, name, tenantId, subscriptionId, applicationID, applicationKey):
        account = {}
        if name is not None: account["name"] = name
        if tenantId is not None: account["tenantId"] = tenantId
        if subscriptionId is not None: account["subscriptionId"] = subscriptionId
        if applicationID is not None: account["applicationId"] = applicationID
        if applicationKey is not None: account["applicationKey"] = applicationKey
        return account

class TestOracle(TestCase):

    @patch("hammr.utils.account_utils.oracle")
    def test_fill_oracle_should_return_cred_account_when_valid_entries(self, mock_oracle):
        # given
        account_given = self.build_account("testName", "testDomainName", "testLogin", "testPassword")

        # when
        account = fill_oracle(account_given)

        # then
        self.assertEquals(mock_oracle.call_count, 1)
        self.assertEqual(account.name, account_given["name"])
        self.assertEqual(account.domainName, account_given["domainName"])
        self.assertEqual(account.login, account_given["login"])
        self.assertEqual(account.password, account_given["password"])

    def test_fill_oracle_should_return_none_when_missing_name(self):
        # given
        accountMocked = self.build_account(None, "testDomainName", "testLogin", "testPassword")

        # when
        account = fill_oracle(accountMocked)

        # then
        self.assertEqual(account, None)

    def test_fill_oracle_should_return_none_when_missing_domain_name(self):
        # given
        accountMocked = self.build_account("testName", None, "testLogin", "testPassword")

        # when
        account = fill_oracle(accountMocked)

        # then
        self.assertEqual(account, None)

    def test_fill_oracle_should_return_none_when_missing_login(self):
        # given
        accountMocked = self.build_account("testName", "testDomainName", None, "testPassword")

        # when
        account = fill_oracle(accountMocked)

        # then
        self.assertEqual(account, None)

    def test_fill_oracle_should_return_none_when_missing_password(self):
        # given
        accountMocked = self.build_account("testName", "testDomainName", "testLogin", None)

        # when
        account = fill_oracle(accountMocked)

        # then
        self.assertEqual(account, None)

    def build_account(self, name, domain_name, login, password):
        account = {}
        if name is not None: account["name"] = name
        if domain_name is not None: account["domainName"] = domain_name
        if login is not None: account["login"] = login
        if password is not None: account["password"] = password
        return account

class TestAWS(TestCase):

    @patch("hammr.utils.account_utils.aws")
    def test_fill_aws_should_return_cred_account_when_valid_entries(self, mock_aws):
        # given
        account_given = self.build_account("accountNumber", "name", "accessKeyId", "secretAccessKeyId")

        # when
        account = fill_aws(account_given)

        # then
        self.assertEquals(mock_aws.call_count, 1)
        self.assertEqual(account.accountNumber, account_given["accountNumber"])
        self.assertEqual(account.name, account_given["name"])
        self.assertEqual(account.accessKeyId, account_given["accessKeyId"])
        self.assertEqual(account.secretAccessKeyId, account_given["secretAccessKeyId"])

    def test_fill_aws_should_return_none_when_missing_accountNumber(self):
        # given
        accountMocked = self.build_account(None, "name", "accessKeyId", "secretAccessKeyId")

        # when
        account = fill_aws(accountMocked)

        # then
        self.assertEqual(None, account)

    def test_fill_aws_should_return_none_when_missing_name(self):
        # given
        accountMocked = self.build_account("accountNumber", None, "accessKeyId", "secretAccessKeyId")

        # when
        account = fill_aws(accountMocked)

        # then
        self.assertEqual(None, account)


    def test_fill_aws_should_return_none_when_missing_accessKeyId(self):
        # given
        accountMocked = self.build_account("accountNumber", "name", None, "secretAccessKeyId")

        # when
        account = fill_aws(accountMocked)

        # then
        self.assertEqual(None, account)


    def test_fill_aws_should_return_none_when_missing_secretAccessKeyId(self):
        # given
        accountMocked = self.build_account("accountNumber", "name", "accessKeyId", None)

        # when
        account = fill_aws(accountMocked)

        # then
        self.assertEqual(account, None)

    def build_account(self, accountNumber, name, accessKeyId, secretAccessKeyId):
        account = {}
        if accountNumber is not None: account["accountNumber"] = accountNumber
        if name is not None: account["name"] = name
        if accessKeyId is not None: account["accessKeyId"] = accessKeyId
        if secretAccessKeyId is not None: account["secretAccessKeyId"] = secretAccessKeyId
        return account


class TestGoogle(TestCase):

    def test_fill_google_should_return_none_when_missing_name(self):
        # given
        accountMocked = self.build_account(None, "testCert")

        # when
        account = fill_google(accountMocked)

        # then
        self.assertEqual(None, account)

    def test_fill_google_should_return_none_when_missing_cert(self):
        # given
        accountMocked = self.build_account("testName", None)

        # when
        account = fill_google(accountMocked)

        # then
        self.assertEqual(None, account)

    def test_fill_google_should_return_none_when_old(self):
        # given
        accountMocked = self.build_account("testName", "testCert")
        accountMocked["username"] = "testUsername"

        # when
        account = fill_google(accountMocked)

        # then
        self.assertEqual(account, None)

    def build_account(self, name, certificate):
        account = {}
        if name is not None: account["name"] = name
        if certificate is not None: account["cert"] = certificate
        return account