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

import unittest
import sys
import os

import hammr.commands
from uforge.application import Api

if not "TEST_USER" in os.environ or not "TEST_PASSWORD" in os.environ or not "TEST_URL" in os.environ:
        print "Set env varaible [TEST_USER], [TEST_PASSWORD], and [TEST_URL]"
        sys.exit(1)

login=os.environ['TEST_USER']
password=os.environ['TEST_PASSWORD']
url=os.environ['TEST_URL']



def get_template_id(template, name):
        stdout = sys.stdout
        sys.stdout = open('stdout_file', 'w')
        template.do_list(None)
        sys.stdout = stdout
        cmd = os.popen("cat stdout_file | grep "+name+" | grep -v Getting | cut -d '|' -f2")
        id = cmd.read().rstrip()
        os.remove("stdout_file")
        return id
    
def get_account_id(account, name):
        stdout = sys.stdout
        sys.stdout = open('stdout_file', 'w')
        account.do_list(None)
        sys.stdout = stdout
        cmd = os.popen("cat stdout_file | grep "+name+" | grep -v Getting | cut -d '|' -f2")
        id = cmd.read().rstrip()
        os.remove("stdout_file")
        return id
    
def get_image_id(image, name):
        stdout = sys.stdout
        sys.stdout = open('stdout_file', 'w')
        image.do_list(None)
        sys.stdout = stdout
        cmd = os.popen("cat stdout_file | grep "+name+" | grep -v Getting | cut -d '|' -f2")
        id = cmd.read().rstrip()
        os.remove("stdout_file")
        return id

def get_bundle_id(bundle, name):
        stdout = sys.stdout
        sys.stdout = open('stdout_file', 'w')
        bundle.do_list(None)
        sys.stdout = stdout
        cmd = os.popen("cat stdout_file | grep "+name+" | grep -v Getting | cut -d '|' -f2")
        id = cmd.read().rstrip()
        os.remove("stdout_file")
        return id

class TestCLI(unittest.TestCase):

        global api
        api = Api(url, username = login, password = password, headers = None, disable_ssl_certificate_validation = True)

        def test_01_help_list(self):
                image = hammr.commands.image.Image()
                image.set_globals(api, login, password)
                r = image.help_list()
                self.assertEqual(r, None)


class TestTemplate(unittest.TestCase):

        global api
        api = Api(url, username = login, password = password, headers = None, disable_ssl_certificate_validation = True)

        def test_01_list(self):
                template = hammr.commands.template.Template()
                template.set_globals(api, login, password)
                r = template.do_list(None)
                self.assertEqual(r, 0)

        def test_02_validate(self):
                template = hammr.commands.template.Template()
                template.set_globals(api, login, password)
                r = template.do_validate("--file data/template.json")
                self.assertEqual(r, 0)

        def test_03_delete(self):
                template = hammr.commands.template.Template()
                template.set_globals(api, login, password)
                id = get_template_id(template, "unittest")
                if id is not None and id !="":
                        r = template.do_delete("--id "+id+" --no-confirm")
                        self.assertEqual(r, 0)
                else:
                        raise unittest.SkipTest("No template to delete")

        def test_04_create(self):
                template = hammr.commands.template.Template()
                template.set_globals(api, login, password)
                r = template.do_create("--file data/template.json")
                self.assertNotEqual(r, None)

        def test_04_create_bundle_with_directory(self):
                template = hammr.commands.template.Template()
                template.set_globals(api, login, password)
                r = template.do_create("--file data/templateForBundleDirectoryTest.json")
                self.assertEqual(r, 0)

        def test_05_build(self):
                template = hammr.commands.template.Template()
                template.set_globals(api, login, password)
                r = template.do_build("--file data/template.json")
                self.assertEqual(r, 0)

        def test_06_export(self):
                template = hammr.commands.template.Template()
                template.set_globals(api, login, password)
                id = get_template_id(template, "unittest")
                r = template.do_export("--id "+id)
                self.assertEqual(r, 0)

        def test_07_import(self):
                template = hammr.commands.template.Template()
                template.set_globals(api, login, password)
                id = get_template_id(template, "unittest")
                template.do_delete("--id "+id+" --no-confirm")
                r = template.do_import("--file archive.tar.gz")
                os.remove("archive.tar.gz")
                self.assertEqual(r, 0)

        def test_08_0_templateFull(self):
                #template centOS 6 - name="templateFull"
                template = hammr.commands.template.Template()
                template.set_globals(api, login, password)
                r = template.do_create("--file data/templateFull.json --force")
                self.assertNotEqual(r, None)

        def test_08_1_exportCentOS6(self):
                template = hammr.commands.template.Template()
                template.set_globals(api, login, password)
                id = get_template_id(template, "templateFull")
                r = template.do_export("--id "+id)
                os.remove("archive.tar.gz")
                self.assertEqual(r, 0)

        def test_09_buildPXE(self):
                template = hammr.commands.template.Template()
                template.set_globals(api, login, password)
                r = template.do_build("--file data/templatePXE.json")
                self.assertEqual(r, 0)






class TestOs(unittest.TestCase):

        global api
        api = Api(url, username = login, password = password, headers = None, disable_ssl_certificate_validation = True)

        def test_01_list(self):
                os_ = hammr.commands.os.Os()
                os_.set_globals(api, login, password)
                r = os_.do_list(None)
                self.assertEqual(r, 0)


class TestQuota(unittest.TestCase):

        global api
        api = Api(url, username = login, password = password, headers = None, disable_ssl_certificate_validation = True)

        def test_01_list(self):
                quota = hammr.commands.quota.Quota()
                quota.set_globals(api, login, password)
                r = quota.do_list(None)
                self.assertEqual(r, 0)



class TestUser(unittest.TestCase):

        global api
        api = Api(url, username = login, password = password, headers = None, disable_ssl_certificate_validation = True)

        def test_01_info(self):
                user = hammr.commands.user.User()
                user.set_globals(api, login, password)
                r = user.do_info(None)
                self.assertEqual(r, 0)


class TestAccount(unittest.TestCase):

        global api
        api = Api(url, username = login, password = password, headers = None, disable_ssl_certificate_validation = True)
                
        def test_01_list(self):
                account = hammr.commands.account.Account()
                account.set_globals(api, login, password)
                r = account.do_list(None)
                self.assertEqual(r, 0)
                
        def test_02_delete_account_1(self):
                account = hammr.commands.account.Account()
                account.set_globals(api, login, password)
                id = get_account_id(account, "unittest1")
                if id is not None and id !="":
                        r = account.do_delete("--id "+id+" --no-confirm")
                        self.assertEqual(r, 0)
                else:
                        raise unittest.SkipTest("No account to delete")

        def test_02_delete_account_2(self):
                account = hammr.commands.account.Account()
                account.set_globals(api, login, password)
                id = get_account_id(account, "unittest2")
                if id is not None and id !="":
                        r = account.do_delete("--id "+id+" --no-confirm")
                        self.assertEqual(r, 0)
                else:
                        raise unittest.SkipTest("No account to delete")

        def test_02_delete_account_3(self):
                account = hammr.commands.account.Account()
                account.set_globals(api, login, password)
                id = get_account_id(account, "unittest3")
                if id is not None and id !="":
                        r = account.do_delete("--id "+id+" --no-confirm")
                        self.assertEqual(r, 0)
                else:
                        raise unittest.SkipTest("No account to delete")

        def test_02_delete_account_4(self):
                account = hammr.commands.account.Account()
                account.set_globals(api, login, password)
                id = get_account_id(account, "これはhammrを使って作成したテンプレートです。")
                if id is not None and id !="":
                        r = account.do_delete("--id "+id+" --no-confirm")
                        self.assertEqual(r, 0)
                else:
                        raise unittest.SkipTest("No account to delete")

        def test_03_create(self):
                account = hammr.commands.account.Account()
                account.set_globals(api, login, password)
                r = account.do_create("--file data/create-account.json")
                self.assertEqual(r, 0)

        def test_04_japanese_char(self):
                # ref issue #35
                account = hammr.commands.account.Account()
                account.set_globals(api, login, password)
                r = account.do_create("--file data/create-account-japan-char.json")
                self.assertEqual(r, 0)


class TestFormat(unittest.TestCase):

        global api
        api = Api(url, username = login, password = password, headers = None, disable_ssl_certificate_validation = True)

        def test_01_list(self):
                format = hammr.commands.format.Format()
                format.set_globals(api, login, password)
                r = format.do_list(None)
                self.assertEqual(r, 0)

class TestBundle(unittest.TestCase):

        global api
        api = Api(url, username = login, password = password, headers = None, disable_ssl_certificate_validation = True)

        def test_01_list(self):
                bundle = hammr.commands.bundle.Bundle()
                bundle.set_globals(api, login, password)
                r = bundle.do_list(None)
                self.assertEqual(r, 0)

        def test_02_validate(self):
                bundle = hammr.commands.bundle.Bundle()
                bundle.set_globals(api, login, password)
                r = bundle.do_validate("--file data/bundleFull.json")
                self.assertEqual(r, 0)

        def test_03_delete(self):
                bundle = hammr.commands.bundle.Bundle()
                bundle.set_globals(api, login, password)
                id = get_bundle_id(bundle, "Bundle")
                if id is not None and id !="":
                        r = bundle.do_delete("--id "+id)
                        self.assertEqual(r, 0)
                else:
                        raise unittest.SkipTest("No bundle to delete")

        def test_04_create(self):
                bundle = hammr.commands.bundle.Bundle()
                bundle.set_globals(api, login, password)
                r = bundle.do_create("--file data/bundleFull.json")
                self.assertNotEqual(r, None)

        def test_05_export(self):
                bundle = hammr.commands.bundle.Bundle()
                bundle.set_globals(api, login, password)
                id = get_bundle_id(bundle, "Bundle")
                r = bundle.do_export("--id "+id)
                self.assertEqual(r, 0)

        def test_06_import(self):
                bundle = hammr.commands.bundle.Bundle()
                bundle.set_globals(api, login, password)
                id = get_bundle_id(bundle, "Bundle")
                bundle.do_delete("--id "+id)
                r = bundle.do_import("--file Bundle.tar.gz")
                os.remove("Bundle.tar.gz")
                self.assertEqual(r, 0)


class TestImage(unittest.TestCase):

        global api
        api = Api(url, username = login, password = password, headers = None, disable_ssl_certificate_validation = True)

        def test_01_list(self):
                image = hammr.commands.image.Image()
                image.set_globals(api, login, password)
                r = image.do_list(None)
                self.assertEqual(r, 0)


class TestFilesYam(unittest.TestCase):
        global api
        api = Api(url, username = login, password = password, headers = None, disable_ssl_certificate_validation = True)

        def test_template_create_with_yaml(self):
                template = hammr.commands.template.Template()
                template.set_globals(api, login, password)
                r = template.do_create("--file data/test-parsing.yml --force")
                self.assertEqual(r, 0)


if __name__ == '__main__':
        v=sys.version_info
	if v>=(2,7):
                import xmlrunner
                unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
        else:
                unittest.main()


