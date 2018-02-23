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
from hammr.utils import hammr_utils

__author__ = "UShareSoft"


class Credentials:
    def __init__(self, username=None, password=None, url=None, sslAutosigned=True):
        self.username = username
        self.password = password
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

    @property
    def credFile(self):
        return self.credFile

    def validate(self):
        if self.username is None:
            raise CredentialsException("No user provided.")
        if self.password is None:
            raise CredentialsException("No password provided.")
        if self.url is None:
            raise CredentialsException("No URL provided.")

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
