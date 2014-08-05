'''
	hammr
'''

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
import base64
import httplib2
import os
import json
import sys


from lib.cmdHamr import Cmd, CmdUtils
from lib.argumentParser import HammrArgumentParser, ArgumentParser, ArgumentParserError
import commands
from uforge.application import Api
from utils import *


__author__ = "UShareSoft"
__license__ = "Apache License 2.0"





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
                

## Main cmd
class Hammr(Cmd):
#	subCmds = {
#		'tools': CmdUtils
#	}
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
                        try:
                                doArgs = doParser.parse_args(args.split())
                        except SystemExit as e:
                                return
                        with open(doArgs.file) as f:             
                                for line in f:
                                        try:
                                                self.run_commands_at_invocation([line])
                                        except:
                                                printer.out("bad command '"+line+"'", printer.ERROR)
                                        print "\n"
                                        
                except IOError as e:
                        printer.out("File error: "+e.strerror, printer.ERROR)
                        return
                except ArgumentParserError as e:
                        printer.out("In Arguments: "+str(e), printer.ERROR)
                        self.help_batch()
                
        def help_batch(self):
                doParser = self.arg_batch()
                doParser.print_help()
                

	def cmdloop(self, args):
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
                        subCmds[cmd].set_globals(api, username, password)
                        if hasattr(subCmds[cmd], 'subCmds'):
                                set_globals_cmds(subCmds[cmd].subCmds)


#Generate hammr base command + help base command
CmdBuilder.generateCommands(Hammr)
app = Hammr()
myactions=generate_base_doc(app, hamm_help="")


# Args parsing
mainParser = HammrArgumentParser(add_help=False)
HammrArgumentParser.hammr_actions=myactions
mainParser.add_argument('-a', '--url', dest='url', type=str, help='the UForge server URL endpoint to use', required = False)
mainParser.add_argument('-u', '--user', dest='user', type=str, help='the user name used to authenticate to the UForge server', required = False)
mainParser.add_argument('-p', '--password', dest='password', type=str, help='the password used to authenticate to the UForge server', required = False)
mainParser.add_argument('-v', action='version', help='displays the current version of the hammr tool', version="%(prog)s version '"+constants.VERSION+"'")
mainParser.add_argument('-h', '--help', dest='help', action='store_true', help='show this help message and exit', required = False)
mainParser.set_defaults(help=False)
mainParser.add_argument('cmds', nargs='*', help='Hammr cmds')
mainArgs, unknown = mainParser.parse_known_args()


if mainArgs.help and not mainArgs.cmds:
        mainParser.print_help()
        exit(0)

if mainArgs.user is not None and mainArgs.url is not None:
        if not mainArgs.password:
                mainArgs.password = getpass.getpass()
        username=mainArgs.user
        password=mainArgs.password
        url=mainArgs.url
        sslAutosigned=True

elif os.path.isfile(generics_utils.get_hammr_dir()+os.sep+"credentials.json"):
        try:                                     
                json_data=open(generics_utils.get_hammr_dir()+os.sep+"credentials.json")
                data = json.load(json_data)
                json_data.close()
                if mainArgs.user:
                        username=mainArgs.user
                elif "user" in data:
                        username=data["user"]
                else:
                        printer.out("username not found in the credential hammr file", printer.ERROR)
                        exit(1)
                if mainArgs.password:
                        password=mainArgs.password
                elif "password" in data:
                        password=data["password"]
                else:
                        printer.out("password not found in the credential hammr file", printer.ERROR)
                        exit(1)
                if mainArgs.url:
                        url=mainArgs.url
                elif "url" in data:
                        url=data["url"]
                else:
                        printer.out("url not found in the credential hammr file", printer.ERROR)
                        exit(1)
                if "acceptAutoSigned" in data:
                        sslAutosigned=data["acceptAutoSigned"]
                else:
                        sslAutosigned=True
        except ValueError as e:
                printer.out("JSON parsing error in the credential hammr file: "+str(e), printer.ERROR)
                exit(1)
        except IOError as e:
                printer.out("File error in the credential hammr file: "+str(e), printer.ERROR)
                exit(1)
else:
        mainParser.print_help()
        exit(1)

        


#UForge API instanciation
client = httplib2.Http(disable_ssl_certificate_validation=sslAutosigned)
#activate http caching
#client = httplib2.Http(generics_utils.get_hammr_dir()+os.sep+"cache")
headers = {}
headers['Authorization'] = 'Basic ' + base64.encodestring( username + ':' + password )
api = Api(url, client = client, headers = headers)
set_globals_cmds(app.subCmds)

if mainArgs.help and len(mainArgs.cmds)>=1:
        argList=mainArgs.cmds + unknown;
        argList.insert(len(mainArgs.cmds)-1, "help")
        app.cmdloop(argList)
elif mainArgs.help:
        app.cmdloop(mainArgs.cmds + unknown + ["-h"])
else:
        app.cmdloop(mainArgs.cmds + unknown)
