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

import json
import shutil
import paramiko
import yaml
import sys
import re
import traceback
from os.path import expanduser
import os
import urllib
import pyxb

from uforge.objects.uforge import *
import ussclicore.utils.download_utils
from ussclicore.utils import download_utils
from ussclicore.argumentParser import ArgumentParserError
from ussclicore.utils import printer
from ussclicore.utils import generics_utils
from hammr.utils.bundle_utils import *
from hammr.utils import constants

def check_mandatory_stack(stack):
    if not "name" in stack:
        printer.out("no attribute [name] for [stack]", printer.ERROR)
        return
    if not "version" in stack:
        printer.out("no attribute [version] for [stack]", printer.ERROR)
        return
    if not "os" in stack:
        printer.out("no attribute [os] for [stack]", printer.ERROR)
        return
    else:
        if not "name" in stack["os"]:
            printer.out("no attribute [name] for [os]", printer.ERROR)
            return
        if not "version" in stack["os"]:
            printer.out("no attribute [version] for [os]", printer.ERROR)
            return
        if not "arch" in stack["os"]:
            printer.out("no attribute [arch] for [os]", printer.ERROR)
            return

    return stack

def check_mandatory_builders(builders):
    return builders
    #TODO

def check_mandatory_generate_scan(builders):
    for builder in builders:
        if not "installation" in builder:
            printer.out("no attribute installation in builder", printer.ERROR)
            return
        if not "diskSize" in builder["installation"]:
            printer.out("no attribute diskSize in the installation part of builder", printer.ERROR)
            return
        if not "hardwareSettings" in builder:
            printer.out("no attribute hardwareSettings in builder", printer.ERROR)
            return
        if not "memory" in builder["hardwareSettings"]:
            printer.out("no attribute diskSize in the memory part of hardwareSettings", printer.ERROR)
            return
    return builders

def check_mandatory_create_account(iterables, type):
    #iterables can be builders or accounts
    for iterable in iterables:
        if type=="builders":
            if  "account" in iterable:
                if not "type" in iterable and not "type" in iterable["account"]:
                    printer.out("no attribute type in builder", printer.ERROR)
                    return
                if "file" in iterable["account"]:
                    file = get_file(iterable["account"]["file"])
                    if file is None:
                        return 2
                    data = load_data(file)
                    if data is None:
                        return 2
                    if "accounts" in data:
                        return check_mandatory_create_account(data["accounts"], "accounts")
        if type=="accounts":
            if not "type" in iterable:
                printer.out("no attribute type in accounts", printer.ERROR)
                return

                #TODO

    return iterables


def check_extension_is_json(file_path):
    file_extension = os.path.splitext(file_path)[1]
    if file_extension == ".yml" or file_extension == ".yaml":
        return False
    elif file_extension == ".json":
        return True
    else:
        printer.out("please provide a json or yaml file \n", printer.ERROR)
        raise Exception("File '" + file_path + "' is not allowed. Please provide a json or yaml file.")

def load_data(file):
    isJson = check_extension_is_json(file)
    if isJson:
        print "you provided a json file, checking the syntax..."
        data = generics_utils.check_json_syntax(file)
    else:
        print "you provided a yaml file, checking the syntax..."
        data = generics_utils.check_yaml_syntax(file)
    return data


def validate(file_path):
    is_json = check_extension_is_json(file_path)
    if is_json:
        printer.out("You provided a json file, checking...", printer.INFO)
        template = validate_configurations_file(file_path, isJson=True)
    else:
        printer.out("You provided a yaml file, checking...", printer.INFO)
        template = validate_configurations_file(file_path, isJson=False)
    return template

def validate_configurations_file(file, isJson):
    if isJson:
        data = generics_utils.check_json_syntax(file)
    else:
        data = generics_utils.check_yaml_syntax(file)
    if data is None:
        return
    #check manadatory fields
    if "stack" in data:
        stack=check_mandatory_stack(data["stack"])
        if stack is None:
            return
        if "bundles" in data["stack"]:
            for bundle in data["stack"]["bundles"]:
                bundle = check_bundle(bundle)
                if bundle is None:
                    return

    if "builders" in data:
        check_mandatory_builders(data["builders"])
    return data

def validate_builder_file_with_no_template_id(file_path):
    data = validate(file_path)
    if data is None:
        return None
    if "stack" in data and "builders" in data:
        return data
    elif "stack" not in data:
        printer.out("missing stack section in file " + file_path, printer.ERROR)
        return None
    else:
        printer.out("missing builder section in file "+file_path, printer.ERROR)
        return None

def validate_bundle(file):
    try:
        isJson = check_extension_is_json(file)
        if isJson:
            print "you provided a json file, checking..."
            data = generics_utils.check_json_syntax(file)
        else:
            print "you provided a yaml file, checking..."
            data = generics_utils.check_yaml_syntax(file)

        if data is None:
            return
        data = check_bundle(data)
        if data is None:
            return

        return data
    except ValueError as e:
        printer.out("JSON parsing error: "+str(e), printer.ERROR)
        printer.out("Syntax of bundle file ["+file+"]: FAILED")
    except IOError as e:
        printer.out("unknown error bundle json file", printer.ERROR)

def dump_data_in_file(data, archive_files, isJsonFile, fileName, newFileName):
    file = open(constants.TMP_WORKING_DIR + os.sep + newFileName, "w")

    if isJsonFile:
        json.dump(data, file, indent=4, separators=(',', ': '))
    else:
        yaml.safe_dump(data, file, default_flow_style=False, indent=2, explicit_start='---')

    file.close()
    archive_files.append([fileName, constants.TMP_WORKING_DIR + os.sep + newFileName])

    return archive_files

#manage uforge exception
def is_uforge_exception(e):
    if len(e.args)>=1 and type(e.args[0]) is UForgeError:
        return True

def get_uforge_exception(e):
    if len(e.args)>=1 and type(e.args[0]) is UForgeError:
        return "UForge Error '"+str(e.args[0].statusCode)+"' with method: "+e.args[0].requestMethod+" "+e.args[0].requestUri+"\n"+"Message:\n\t"+e.args[0].localizedErrorMsg.message


def print_uforge_exception(e):
    if len(e.args)>=1 and type(e.args[0]) is UForgeError:
        printer.out(get_uforge_exception(e), printer.ERROR)
    else:
        traceback.print_exc()

def handle_uforge_exception(e):
    print_uforge_exception(e)
    return 2





def get_uforge_url_from_ws_url(ws_url):
    if ws_url[-1:]!='/':
        return ws_url.rpartition('/')[0]
    else:
        return ws_url[:-1].rpartition('/')[0]


def get_hammr_dir():
    dir = ussclicore.utils.generics_utils.get_home_dir()+os.sep+".hammr"
    if not os.path.isdir(dir):
        os.mkdir(dir)
    return dir

def create_user_ssh_key(api, login, sshKey):
    if not "name" in sshKey:
        printer.out("sshKey name not found in builder", printer.ERROR)
        return 2
    if not "publicKey" in sshKey:
        printer.out("publicKey in sshKey not found in builder", printer.ERROR)
        return 2

    mySshKey = sshKey()
    mySshKey.name=sshKey["name"]
    mySshKey.publicKey=sshKey["publicKey"]
    key = self.api.Users(login).Sshkeys().Create(mySshKey)
    if key is None:
        printer.out("Impossible to create sshKey ["+mySshKey.name+"]", printer.ERROR)
        return 2
    return key

def is_uri_based_on_appliance(uri):
    match = re.match( r'users/[^/]+/appliances/[0-9]+($|/)', uri)
    if match:
        return True
    else:
        return False

def is_uri_based_on_scan(uri):
    match = re.match( r'users/[^/]+/scannedinstances/[0-9]+/scans/[0-9]+($|/)', uri)
    if match:
        return True
    else:
        return False

def extract_scannedinstance_id(image_uri):
    match = re.match( r'users/[^/]+/scannedinstances/([0-9]+)($|/)', image_uri)
    if match:
        return int(match.group(1))
    else:
        return None

def extract_scan_id(image_uri):
    match = re.match( r'users/[^/]+/scannedinstances/[0-9]+/scans/([0-9]+)($|/)', image_uri)
    if match:
        return int(match.group(1))
    else:
        return None

def extract_appliance_id(image_uri):
    match = re.match( r'users/[^/]+/appliances/([0-9]+)($|/)', image_uri)
    if match:
        return int(match.group(1))
    else:
        return None


def retrieve_template_from_file(file):
    file = generics_utils.get_file(file)
    if not file:
        raise ArgumentParserError("Wrong file argument")
    template = validate(file)
    if not template:
        raise ValueError("Could not extract information from file")
    return template

def download_binary_in_local_temp_dir(api, local_temp_dir, uri_binary, binary_name):
    uri = generics_utils.get_uforge_url_from_ws_url(api.getUrl())
    download_url = uri + uri_binary

    if os.path.isdir(local_temp_dir):
        shutil.rmtree(local_temp_dir)
    os.mkdir(local_temp_dir)
    local_uforge_binary_path = local_temp_dir + os.sep + binary_name

    dlUtils = download_utils.Download(download_url, local_uforge_binary_path,
                                      not api.getDisableSslCertificateValidation())
    try:
        dlUtils.start()
        return local_uforge_binary_path
    except Exception, e:
        raise Exception("Impossible to download binary [" + binary_name + "]: " + str(e))

def upload_binary_to_client(hostname, port, username, password, file_src_path, binary_path, id_file):
    try:
        t = paramiko.Transport((hostname, port))
        pkey = None
        if id_file:
            pkey = paramiko.RSAKey.from_private_key_file(id_file)
            t.connect(username=username, pkey=pkey)
        else:
            t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)

        # upload binary
        sftp.put(file_src_path, binary_path)
        t.close()

        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
        client.connect(hostname, port, username, password, pkey)

    except paramiko.AuthenticationException as e:
        raise Exception("Authentification error: " + e[0])
    except Exception, e:
        try:
            t.close()
            client.close()
        except:
            pass
        raise Exception("Caught exception when uploading binary [" + binary_path + "]: " + str(e))

    return client

def launch_binary(client, command):
    try:
        summary = ''
        stdin, stdout, stderr = client.exec_command(command)
        for line in stdout:
            summary = summary + "... " + line

    except Exception, e:
        try:
            client.close()
        except:
            pass
        raise Exception("Caught exception: " + str(e))

    return summary