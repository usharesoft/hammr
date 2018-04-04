from unittest import TestCase

import re
from hammr.utils import credentials
from hammr.utils.credentials import CredentialsException
from mock import patch


class TestCredentials(TestCase):
    @patch("hammr.utils.credentials.Credentials.is_basic_auth_valid")
    def test_validate_not_throw_when_credential_basic(self, is_basic_auth_valid):
        # given
        cred = credentials.Credentials(url="my_url")
        is_basic_auth_valid.return_value = True

        # when / then
        cred.validate()

    @patch("hammr.utils.credentials.Credentials.is_api_auth_valid")
    def test_validate_not_throw_when_credential_api(self, is_api_auth_valid):
        # given
        cred = credentials.Credentials(url="url")
        is_api_auth_valid.return_value = True

        # when / then
        cred.validate()

    @patch("hammr.utils.credentials.Credentials.is_basic_auth_valid")
    @patch("hammr.utils.credentials.Credentials.is_api_auth_valid")
    def test_validate_throw_when_credential_miss_url(self, is_basic_auth_valid, is_api_auth_valid):
        # given
        cred = credentials.Credentials()
        is_basic_auth_valid.return_value = True
        is_api_auth_valid.return_value = True

        # when / then
        self.assertRaisesRegexp(CredentialsException, re.compile("URL"), cred.validate)

    @patch("hammr.utils.credentials.Credentials.is_basic_auth_valid")
    @patch("hammr.utils.credentials.Credentials.is_api_auth_valid")
    def test_validate_throw_when_credential_wrong(self, is_basic_auth_valid, is_api_auth_valid):
        # given
        cred = credentials.Credentials(url="my_url")
        is_basic_auth_valid.return_value = False
        is_api_auth_valid.return_value = False

        # when / then
        self.assertRaises(CredentialsException, cred.validate)

    def test_is_basic_auth_valid_return_true_when_no_conflict(self):
        # given
        cred = credentials.Credentials(username="my_user", password="my_password", publicKey=None, secretKey=None)

        # when
        valid = cred.is_basic_auth_valid()

        # then
        self.assertTrue(valid)

    def test_is_basic_auth_valid_return_false_when_conflict(self):
        # given
        cred = credentials.Credentials(username="my_user", password="my_password", publicKey="my_pub", secretKey="my_secret")

        # when
        valid = cred.is_basic_auth_valid()

        # then
        self.assertFalse(valid)

    def test_is_basic_auth_valid_return_false_when_no_username(self):
        # given
        cred = credentials.Credentials(username=None, password="my_password", publicKey=None, secretKey=None)

        # when
        valid = cred.is_basic_auth_valid()

        # then
        self.assertFalse(valid)

    def test_is_basic_auth_valid_return_false_when_no_password(self):
        # given
        cred = credentials.Credentials(username="my_user", password=None, publicKey=None, secretKey=None)

        # when
        valid = cred.is_basic_auth_valid()

        # then
        self.assertFalse(valid)

    def test_is_api_auth_valid_return_true_when_no_conflict(self):
        # given
        cred = credentials.Credentials(username="my_user", password=None, publicKey="my_pub", secretKey="my_secret")

        # when
        valid = cred.is_api_auth_valid()

        # then
        self.assertTrue(valid)

    def test_is_api_auth_valid_return_false_when_conflict(self):
        # given
        cred = credentials.Credentials(username="my_user", password="my_password", publicKey="my_pub", secretKey="my_secret")

        # when
        valid = cred.is_api_auth_valid()

        # then
        self.assertFalse(valid)

    def test_is_api_auth_valid_return_false_when_no_username(self):
        # given
        cred = credentials.Credentials(username=None, password=None, publicKey="my_pub", secretKey="my_secret")

        # when
        valid = cred.is_api_auth_valid()

        # then
        self.assertFalse(valid)

    def test_is_api_auth_valid_return_false_when_no_public_key(self):
        # given
        cred = credentials.Credentials(username="my_user", password=None, publicKey=None, secretKey="my_secret")

        # when
        valid = cred.is_api_auth_valid()

        # then
        self.assertFalse(valid)

    def test_is_api_auth_valid_return_false_when_no_secret_key(self):
        # given
        cred = credentials.Credentials(username="my_user", password=None, publicKey="my_pub", secretKey=None)

        # when
        valid = cred.is_api_auth_valid()

        # then
        self.assertFalse(valid)

    @patch("hammr.utils.hammr_utils.load_data")
    def test_from_file_fill_fields_when_credential_is_correct(self, load_data):
        # given
        user = "my_user"
        password = "my_password"
        publicKey = "my_pub"
        secretKey = "my_secret"
        url = "my_url"
        sslAutosigned = "False"
        load_data.return_value = {"user": user, "password": password, "publickey": publicKey, "secretkey": secretKey,
                                  "url": url, "acceptAutoSigned": sslAutosigned}

        # when
        cred = credentials.Credentials.from_file("credentials.yml")

        # then
        self.assertEqual(user, cred.username)
        self.assertEqual(password, cred.password)
        self.assertEqual(publicKey, cred.publicKey)
        self.assertEqual(secretKey, cred.secretKey)
        self.assertEqual(url, cred.url)
        self.assertEqual(sslAutosigned, cred.sslAutosigned)

    @patch("hammr.utils.hammr_utils.load_data")
    def test_from_file_throw_when_credential_is_empty(self, load_data):
        # given
        load_data.return_value = None

        # when / then
        self.assertRaises(CredentialsException, credentials.Credentials.from_file, "credentials.yml")
