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
from hammr.utils import hammr_utils

__author__ = "UShareSoft"


class Credentials:
    def __init__(self, username=None, password=None, publicKey=None, secretKey=None, url=None, sslAutosigned=True):
        self.username = username
        self.password = password
        self.publicKey = publicKey
        self.secretKey = secretKey
        self.url = url
        self.sslAutosigned = sslAutosigned

    @property
    def username(self):
        return self.username

    @username.setter
    def username(self, username):
        self.username = username

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, password):
        self.password = password

    @property
    def publicKey(self):
        return self.publicKey

    @publicKey.setter
    def publicKey(self, publicKey):
        self.publicKey = publicKey

    @property
    def secretKey(self):
        return self.secretKey

    @secretKey.setter
    def secretKey(self, secretKey):
        self.secretKey = secretKey

    @property
    def url(self):
        return self.url

    @url.setter
    def url(self, url):
        self.url = url

    @property
    def sslAutosigned(self):
        return self.sslAutosigned

    @sslAutosigned.setter
    def sslAutosigned(self, sslAutosigned):
        self.sslAutosigned = sslAutosigned

    def get_api_keys(self):
        if self.publicKey is not None and self.secretKey is not None:
            return {"publickey": self.publicKey, "secretkey": self.secretKey}
        else:
            return None

    def validate(self):
        if not self.is_basic_auth_valid() and not self.is_api_auth_valid():
            raise CredentialsException("""Please provide authentication information. There are two ways to do this, either:
provide a user and password: -u|--user <username> -p|--password <password>
or
provide a user and an API key pair: -u|--user <username> -k|--publickey <value> -s|--secretkey <value>""")
        if self.url is None:
            raise CredentialsException("Please provide an URL.")

    def is_basic_auth_valid(self):
        return self.username is not None and self.password is not None and self.publicKey is None and self.secretKey is None

    def is_api_auth_valid(self):
        return self.username is not None and self.password is None and self.publicKey is not None and self.secretKey is not None

    @staticmethod
    def from_file(path):
        credentials = Credentials()
        data = hammr_utils.load_data(path)
        if data is None:
            raise CredentialsException("Parsing error in credentials file: " + path)
        if "user" in data:
            credentials.username = data["user"]
        if "password" in data:
            credentials.password = data["password"]
        if "publickey" in data:
            credentials.publicKey = data["publickey"]
        if "secretkey" in data:
            credentials.secretKey = data["secretkey"]
        if "url" in data:
            credentials.url = data["url"]
        if "acceptAutoSigned" in data:
            credentials.sslAutosigned = data["acceptAutoSigned"]
        return credentials


class CredentialsException(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return self.reason
