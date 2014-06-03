# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import json
import sys
import re
import traceback
from os.path import expanduser
import os
import urllib

from uforge.objects.xsd0 import *
import download_utils
import printer

__author__="UShareSoft"


def extract_id(uri):
        elements = uri.split("/");
        return elements[len(elements) - 1];                
    
    
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
                                        data = check_json_syntax(file)
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

def check_json_syntax(file):
        try:
                printer.out("Validating the template file ["+file+"] ...")
                json_data=open(file)
                data = json.load(json_data)
                json_data.close()
                printer.out("Syntax of template file ["+file+"] is ok", printer.OK)
                return data
        except ValueError as e:
                printer.out("Syntax of template file ["+file+"] FAILED", printer.ERROR)
                printer.out("JSON parsing error: "+str(e))
                return
        except IOError as e:
                printer.out("File error: "+e.strerror, printer.ERROR)
                return
    
def validate_json_file(file):
        try:
                data = check_json_syntax(file)
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
                
                
def query_yes_no(question, default="yes"):
        """Ask a yes/no question via raw_input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is one of "yes" or "no".
        """
        valid = {"yes":True,   "y":True,  "ye":True,
                 "no":False,     "n":False}
        if default == None:
                prompt = " [y/n] "
        elif default == "yes":
                prompt = " [Y/n] "
        elif default == "no":
                prompt = " [y/N] "
        else:
                raise ValueError("invalid default answer: '%s'" % default)

        while True:
                printer.out(question + prompt)
                choice = raw_input().lower()
                if default is not None and choice == '':
                        return valid[default]
                elif choice in valid:
                        return valid[choice]
                else:
                        printer.out("Please respond with 'yes' or 'no' "\
                                     "(or 'y' or 'n').\n")
                             
                             
def remove_special_chars(string):
        return (re.sub('[-]', '_', string)).lower()

def is_uforge_exception(e):
        if len(e.args)>=1 and type(e.args[0]) is uForgeError:
                return True

def print_uforge_exception(e):
        if len(e.args)>=1 and type(e.args[0]) is uForgeError:
                return "UForge Error '"+str(e.args[0].statusCode)+"' with method: "+e.args[0].requestMethod+" "+e.args[0].requestUri+"\n"+"Message:\n\t"+e.args[0].errorMsg
        else:
                traceback.print_exc()
                
def oder_list_object_by(objects, attribute):
        if type(attribute) is str:
                return sorted(objects, key=lambda x: getattr(x, attribute).lower(), reverse=False)
                
        return objects
    
def get_uforge_url_from_ws_url(ws_url):
        if ws_url[-1:]!='/':
                return ws_url.rpartition('/')[0]
        else:
                return ws_url[:-1].rpartition('/')[0]
            
def get_home_dir():
        return expanduser("~")
    
def get_hammr_dir():
        dir = get_home_dir()+os.sep+".hammr"
        if not os.path.isdir(dir):
                os.mkdir(dir)
        return dir
    
def get_remote_regex():
        return 'http|ftp|svn'
    
def get_file(uri):
        try:
                regexp = re.compile(get_remote_regex())
                if regexp.search(uri) is not None:
                        print "Downloadling file "+os.path.basename(uri)+": "
                        dlUtils = download_utils.Download()
                        file, headers = urllib.urlretrieve(uri, reporthook=dlUtils.progress_update)
                        dlUtils.progress_finish()
                else:
                        file, headers = urllib.urlretrieve(uri)
                return file
        except Exception, e:
                print("error downloading "+uri+": "+ str(e))
                return
            
def remove_URI_forbidden_char(string):
        chars= ' '
        return re.sub(chars, '_', string)
    
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