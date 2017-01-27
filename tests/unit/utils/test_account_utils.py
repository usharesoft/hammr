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
        self.assertIsNone(account)


    def test_k5_should_return_none_when_missing_login(self):
        # given
        account_given = self.build_account("testName", None, "testPassword")

        # when
        account = k5(account_given)

        # then
        self.assertIsNone(account)


    def test_k5_should_return_none_when_missing_password(self):
        # given
        account_given = self.build_account("testName", "testLogin", None)

        # when
        account = k5(account_given)

        # then
        self.assertIsNone(account)


    def build_account(self, name, login, password):
        account = {}
        if name is not None: account["name"] = name
        if login is not None: account["login"] = login
        if password is not None: account["password"] = password
        return account
