# Copyright 2007-2015 UShareSoft SAS, All rights reserved
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
import sys
import re
import traceback
from os.path import expanduser
import os
import urllib

from uforge.objects.uforge import *
import ussclicore.utils.download_utils
from ussclicore.utils import printer
from ussclicore.utils import generics_utils


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
                    data = generics_utils.check_json_syntax(file)
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

def validate_json_file(file):
    try:
        data = generics_utils.check_json_syntax(file)
        if data is None:
            return
        #check manadatory fields
        if "stack" in data:
            stack=check_mandatory_stack(data["stack"])
            if stack is None:
                return
        #else:
        #        print "No stack section find in the template file"
        #        return

        if "builders" in data:
            check_mandatory_builders(data["builders"])

        return data
    except ValueError as e:
        printer.out("JSON parsing error: "+str(e), printer.ERROR)
        printer.out("Syntax of template file ["+file+"]: FAILED")
    except IOError as e:
        printer.out("unknown error template json file", printer.ERROR)



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
