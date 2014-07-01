# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="UShareSoft"

from texttable import Texttable
from hammr.lib.argumentParser import ArgumentParser, ArgumentParserError
from hammr.lib.cmdHamr import Cmd, HammrGlobal
from hammr.utils import *

class User(Cmd, HammrGlobal):
        """Lists information about a user, including login, email, name, date created, and status"""
    
        cmd_name="user"
    
        def __init__(self):
                super(User, self).__init__()
                
        def arg_info(self):
                doParser = ArgumentParser(prog=self.cmd_name+" info", add_help = True, description="Displays informations of provided user")
                return doParser   
        
        def do_info(self, args):
                try:

                        #call UForge API                                               
                        printer.out("Getting user ["+self.login+"] ...")
                        user = self.api.Users(self.login).Get()                

                        if user is None:
                                printer.out("user "+ self.login +"does not exist", printer.ERROR)
                        else:
                            table = Texttable(200)
                            table.set_cols_align(["c", "l", "c", "c", "c", "c", "c", "c"])
                            table.header(["Login", "Email", "Lastname",  "Firstname",  "Created", "Active", "Promo Code", "Creation Code"])
                            table.add_row([user.loginName, user.email, user.surname , user.firstName, user.created.strftime("%Y-%m-%d %H:%M:%S"), "X", user.promoCode, user.creationCode])
                            print table.draw() + "\n"
                        return 0
                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
                        self.help_info()
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
        
        def help_info(self):
                doParser = self.arg_info()
                doParser.print_help()
                