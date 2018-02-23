from unittest import TestCase

import re
from mock import patch

from hammr.utils import credentials
from hammr.utils.credentials import CredentialsException


class TestCredentials(TestCase):
    def test_validate_not_throw_when_credential_is_correct(self):
        # given
        cred = credentials.Credentials("my_user", "my_password", "url")

        # when / then
        cred.validate()

    def test_validate_throw_when_credential_miss_username(self):
        # given
        cred = credentials.Credentials(password="my_password", url="my_url")

        # when / then
        self.assertRaisesRegexp(CredentialsException, re.compile("user"), cred.validate)

    def test_validate_throw_when_credential_miss_password(self):
        # given
        cred = credentials.Credentials(username="my_user", url="my_url")

        # when / then
        self.assertRaisesRegexp(CredentialsException, re.compile("password"), cred.validate)

    def test_validate_throw_when_credential_miss_url(self):
        # given
        cred = credentials.Credentials(username="my_user", password="my_password")

        # when / then
        self.assertRaisesRegexp(CredentialsException, re.compile("URL"), cred.validate)

    @patch("hammr.utils.hammr_utils.load_data")
    def test_from_file_fill_fields_when_credential_is_correct(self, load_data):
        # given
        user = "my_user"
        password = "my_password"
        url = "my_url"
        sslAutosigned = "False"
        load_data.return_value = {"user": user, "password": password, "url": url, "acceptAutoSigned": sslAutosigned}

        # when
        cred = credentials.Credentials.from_file("credentials.yml")

        # then
        self.assertEqual(user, cred.username)
        self.assertEqual(password, cred.password)
        self.assertEqual(url, cred.url)
        self.assertEqual(sslAutosigned, cred.sslAutosigned)

    @patch("hammr.utils.hammr_utils.load_data")
    def test_from_file_throw_when_credential_is_empty(self, load_data):
        # given
        load_data.return_value = None

        # when / then
        self.assertRaises(CredentialsException, credentials.Credentials.from_file, "credentials.yml")
