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

try:
    from termcolor import colored
except ImportError:
    def colored(string, a=None, b=None, attrs=None):
        return string
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import argparse
import getpass
import os
import sys
import shlex


from ussclicore.cmd import Cmd, CmdUtils
from ussclicore.argumentParser import CoreArgumentParser, ArgumentParser, ArgumentParserError
from ussclicore.utils import generics_utils
from ussclicore.utils import printer
import commands
from uforge.application import Api, checkUForgeCompatible
from utils import constants, hammr_utils

class CmdBuilder(object):
    @staticmethod
    def generateCommands(class_):
        # Create subCmds if not exist
        if not hasattr(class_, 'subCmds'):
            class_.subCmds = {}
            # Add commands
        user = commands.user.User()
        class_.subCmds[user.cmd_name] = user
        template = commands.template.Template()
        class_.subCmds[template.cmd_name] = template
        _os = commands.os.Os()
        class_.subCmds[_os.cmd_name] = _os
        format = commands.format.Format()
        class_.subCmds[format.cmd_name] = format
        image = commands.image.Image()
        class_.subCmds[image.cmd_name] = image
        account = commands.account.Account()
        class_.subCmds[account.cmd_name] = account
        bundle = commands.bundle.Bundle()
        class_.subCmds[bundle.cmd_name] = bundle
        scan = commands.scan.Scan()
        class_.subCmds[scan.cmd_name] = scan
        quota = commands.quota.Quota()
        class_.subCmds[quota.cmd_name] = quota
        platform = commands.platform.Platform()
        class_.subCmds[platform.cmd_name] = platform
        deploy = commands.deploy.Deploy()
        class_.subCmds[deploy.cmd_name] = deploy

## Main cmd
class Hammr(Cmd):
    #    subCmds = {
    #        'tools': CmdUtils
    #    }
    def __init__(self):
        super(Hammr, self).__init__()
        self.prompt = 'hammr> '

    def do_exit(self, args):
        return True

    def do_quit(self, args):
        return True

    def arg_batch(self):
        doParser = ArgumentParser("batch", add_help = True, description="Execute hammr batch command from a file (for scripting)")
        mandatory = doParser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--file', dest='file', required=True, help="hammr batch file commands")
        return doParser

    def do_batch(self, args):
        try:
            doParser = self.arg_batch()
            doArgs = doParser.parse_args(shlex.split(args))

            #if the help command is called, parse_args returns None object
            if not doArgs:
                    return 2

            with open(doArgs.file) as f:
                for line in f:
                    try:
                        self.run_commands_at_invocation([line])
                    except:
                        printer.out("bad command '"+line+"'", printer.ERROR)
                    print "\n"
        except IOError as e:
            printer.out("File error: "+str(e), printer.ERROR)
            return
        except ArgumentParserError as e:
            printer.out("In Arguments: "+str(e), printer.ERROR)
            self.help_batch()

    def help_batch(self):
        doParser = self.arg_batch()
        doParser.print_help()

    def compatibility_verbose(self):
        try:
            compatible, serviceStatusVersion = checkUForgeCompatible(api)
            if not compatible:
                printer.out("Sorry but this version of Hammr (version = '" + str(
                    constants.VERSION) + "') is not compatible with the version of UForge (version = '" + str(
                    serviceStatusVersion) + "').", printer.ERROR)
                printer.out(
                    "Please refer to 'Install Compatibility' section in the documentation to learn how to install a compatible version of Hammr.",
                    printer.ERROR)
                sys.exit(2)

        except Exception as e:
            hammr_utils.print_uforge_exception(e)
            sys.exit(2)

    def cmdloop(self, args):
        self.compatibility_verbose()
        if len(args):
            code = self.run_commands_at_invocation([str.join(' ', args)])
            sys.exit(code)
        else:
            self._cmdloop()

def generate_base_doc(app, hamm_help):
    myactions=[]
    cmds= sorted(app.subCmds)
    for cmd in cmds:
        myactions.append(argparse._StoreAction(
            option_strings=[],
            dest=str(cmd),
            nargs=None,
            const=None,
            default=None,
            type=str,
            choices=None,
            required=False,
            help=str(app.subCmds[cmd].__doc__),
            metavar=None))
    return myactions

def set_globals_cmds(subCmds):
    for cmd in subCmds:
        if hasattr(subCmds[cmd], 'set_globals'):
            subCmds[cmd].set_globals(api, login, password)
            if hasattr(subCmds[cmd], 'subCmds'):
                set_globals_cmds(subCmds[cmd].subCmds)

def check_credfile(credfile):
    printer.out("Checking given credentials file: " + credfile, printer.INFO)
    if os.path.isfile(credfile):
        return credfile
    return None

def check_default_credfile():
    printer.out("Checking default credentials file...", printer.INFO)
    credfile_yaml=hammr_utils.get_hammr_dir()+os.sep+"credentials.yml"
    if os.path.isfile(credfile_yaml):
        return credfile_yaml
    credfile_json=hammr_utils.get_hammr_dir()+os.sep+"credentials.json"
    if os.path.isfile(credfile_json):
        return credfile_json
    return None

#Generate hammr base command + help base command
CmdBuilder.generateCommands(Hammr)
app = Hammr()
myactions=generate_base_doc(app, hamm_help="")

# Args parsing
mainParser = CoreArgumentParser(add_help=False)
CoreArgumentParser.actions=myactions
mainParser.add_argument('-a', '--url', dest='url', type=str, help='the UForge server URL endpoint to use', required = False)
mainParser.add_argument('-u', '--user', dest='user', type=str, help='the user name used to authenticate to the UForge server', required = False)
mainParser.add_argument('-p', '--password', dest='password', type=str, help='the password used to authenticate to the UForge server', required = False)
mainParser.add_argument('-c', '--credentials', dest='credentials', type=str, help='the credential file used to authenticate to the UForge server (default to ~/.hammr/credentials.yml or ~/.hammr/credentials.json)', required = False)
mainParser.add_argument('-v', action='version', help='displays the current version of the hammr tool', version="%(prog)s version '"+constants.VERSION+"'")
mainParser.add_argument('-h', '--help', dest='help', action='store_true', help='show this help message and exit', required = False)
mainParser.set_defaults(help=False)
mainParser.add_argument('cmds', nargs='*', help='Hammr cmds')
mainArgs, unknown = mainParser.parse_known_args()

if mainArgs.help and not mainArgs.cmds:
    mainParser.print_help()
    exit(0)

if mainArgs.url is not None:
    url=mainArgs.url

if mainArgs.user is not None:
    if not mainArgs.password:
        mainArgs.password = getpass.getpass()
    username=mainArgs.user
    password=mainArgs.password
    sslAutosigned=True
else:
    if mainArgs.credentials is not None:
        credfile=mainArgs.credentials
        credpath=check_credfile(credfile)
        if credpath is None:
            printer.out("credentials file '" + credfile + "' not found\n", printer.ERROR)
            exit(1)
    else:
        credpath=check_default_credfile()
        if credpath is None:
            printer.out("credentials file 'credentials.yml' or 'credentials.json' not found\n", printer.ERROR)
            exit(1)

    printer.out("no username nor password provided on command line, trying credentials file", printer.INFO)

    printer.out("Using credentials file: " + credpath, printer.INFO)
    try:
        data = hammr_utils.load_data(credpath)
        if mainArgs.user:
            username=mainArgs.user
        elif "user" in data:
            username=data["user"]
        else:
            printer.out("username not found in credentials file", printer.ERROR)
        if mainArgs.password:
            password=mainArgs.password
        elif "password" in data:
            password=data["password"]
        else:
            printer.out("password not found in credentials file", printer.ERROR)
        if mainArgs.url:
            url=mainArgs.url
        elif "url" in data:
            url=data["url"]
        else:
            printer.out("url not found in credentials file", printer.ERROR)
        printer.out("Using url " + url, printer.INFO)
        if "acceptAutoSigned" in data:
            sslAutosigned=data["acceptAutoSigned"]
        else:
            sslAutosigned=True
    except ValueError as e:
        printer.out("parsing error in credentials file: "+str(e), printer.ERROR)
    except IOError as e:
        printer.out("File error in credentials file: "+str(e), printer.ERROR)
    except Exception as e:
        hammr_utils.print_uforge_exception(e)
        exit(1)

#UForge API instanciation
api = Api(url, username = username, password = password, headers = None, disable_ssl_certificate_validation = sslAutosigned, timeout = constants.HTTP_TIMEOUT)

if generics_utils.is_superviser_mode(username):
    login = generics_utils.get_target_username(username)
else:
    login = username

set_globals_cmds(app.subCmds)

if mainArgs.help and len(mainArgs.cmds)>=1:
    argList=mainArgs.cmds + unknown;
    argList.insert(len(mainArgs.cmds)-1, "help")
    app.cmdloop(argList)
elif mainArgs.help:
    app.cmdloop(mainArgs.cmds + unknown + ["-h"])
else:
    app.cmdloop(mainArgs.cmds + unknown)
