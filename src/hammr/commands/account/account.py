
__author__="UShareSoft"

from texttable import Texttable
from hammr.lib.argumentParser import ArgumentParser, ArgumentParserError
from hammr.lib.cmdHamr import Cmd, HammrGlobal
from hammr.utils import *
from uforge.objects.xsd0 import *


class Account(Cmd, HammrGlobal):
        """List, create or delete a cloud account"""
    
        cmd_name="account"
    
        def __init__(self):
                super(Account, self).__init__()        
        
        
        def arg_list(self):
                doParser = ArgumentParser(prog=self.cmd_name+" list", add_help = True, description="Displays all the cloud accounts for the user")
                return doParser   

        def do_list(self, args):  
                        try:
                                #call UForge API
                                printer.out("Getting all your accounts ...")
                                accounts = self.api.Users(self.login).Accounts.Getall()
                                if accounts is None or not hasattr(accounts, 'get_credAccount'):
                                        printer.out("No accounts available")
                                else:
                                        table = Texttable(800)
                                        table.set_cols_dtype(["t", "t","t", "t"])
                                        table.header(["Id", "Name", "Type", "Created"])
                                        accounts = generics_utils.oder_list_object_by(accounts.get_credAccount(), "name")
                                        for account in accounts:
                                                table.add_row([account.dbId, account.name, account.type_, account.created.strftime("%Y-%m-%d %H:%M:%S")])
                                        print table.draw() + "\n"
                                        printer.out("Found "+str(len(accounts))+" accounts")
                                return 0
                        except Exception as e:        
                                print generics_utils.print_uforge_exception(e)
                                

                    
        def help_list(self):
                doParser = self.arg_list()
                doParser.print_help()
            
                
        def arg_create(self):
                doParser = ArgumentParser(prog=self.cmd_name+" create", add_help = True, description="Creates a new cloud account")
                mandatory = doParser.add_argument_group("mandatory arguments")
                mandatory.add_argument('--file', dest='file', required=True, help="json file providing the cloud account parameters")
                return doParser     
                
        def do_create(self, args):
                try:            
                        #add arguments
                        doParser = self.arg_create()
                        try:
                                doArgs = doParser.parse_args(args.split())
                        except SystemExit as e:
                                return
                        #--
                        file = generics_utils.get_file(doArgs.file)
                        if file is None:
                                return 2                        
                        data = generics_utils.check_json_syntax(file)
                        if data is None:
                                return 2
                        if "builders" in data:
                                accounts_file_type = "builders"
                                iterables=generics_utils.check_mandatory_create_account(data["builders"], accounts_file_type)
                        elif "accounts" in data:
                                accounts_file_type = "accounts"
                                iterables=generics_utils.check_mandatory_create_account(data["accounts"], accounts_file_type)
                        else:
                                printer.out("Error: no builders or accounts section found", printer.ERROR)
                                return 2
                        if iterables is None:
                                return 2
                        try:
                                for iterable in iterables:
                                            try:
                                                    myCredAccount=None
                                                    if "type" in iterable:
                                                            account_type=iterable["type"]
                                                    elif "account" in iterable:
                                                            account_type=iterable["account"]["type"]
                                                    func = getattr(account_utils, generics_utils.remove_special_chars(account_type), None)
                                                    if func:
                                                            if accounts_file_type == "builders" and "account" in iterable:
                                                                    myCredAccount = func(credAccount(), iterable["account"])
                                                            elif accounts_file_type == "accounts":
                                                                    myCredAccount = func(credAccount(), iterable)
                                                            else:
                                                                    pass
                                                                    #DO NOTHING - no account in builder to create

                                                    #TODO
                                                    #the account type must be in the account part, if no builder part (independant file)
                                                            if myCredAccount is not None:
                                                                    printer.out("Create account for '"+account_type+"'...")
                                                                    self.api.Users(self.login).Accounts.Create(myCredAccount)
                                                                    printer.out("Account create successfully for ["+account_type+"]", printer.OK)
                                            except Exception as e:
                                                    if generics_utils.is_uforge_exception(e):
                                                            print generics_utils.print_uforge_exception(e)
                                                    else:
                                                            raise
                                                    
                                return 0       
                            
                        except KeyError as e:
                                printer.out("unknown error template json file", printer.ERROR)
                              
                except IOError as e:
                        printer.out("File error: "+e.strerror, printer.ERROR)
                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
                        self.help_create()
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
                        
        def help_create(self):
                doParser = self.arg_create()
                doParser.print_help()
                
                
        def arg_delete(self):
                doParser = ArgumentParser(prog=self.cmd_name+" delete", add_help = True, description="Deletes an existing cloud account")
                mandatory = doParser.add_argument_group("mandatory arguments")
                mandatory.add_argument('--id', dest='id', required=True, help="the ID of the cloud account to delete")
                optional = doParser.add_argument_group("optional arguments")
                optional.add_argument('--no-confirm', dest='no_confirm', action='store_true', required=False, help="do not ask before delete the cloud account") 
                doParser.set_defaults(no_confirm=False)
                return doParser  
            
        def do_delete(self, args):
                try:
                        #add arguments
                        doParser = self.arg_delete()
                        try:
                                doArgs = doParser.parse_args(args.split())
                        except SystemExit as e:
                                return
                        #call UForge API
                        printer.out("Searching account with id ["+doArgs.id+"] ...")
                        account = self.api.Users(self.login).Accounts(doArgs.id).Get()
                        if account is None or type(account) is not credAccount:
                                printer.out("No Account available", printer.WARNING)
                        else:
                                table = Texttable(800)
                                table.set_cols_dtype(["t", "t","t", "t"])
                                table.header(["Id", "Name", "Type", "Created"])
                                table.add_row([account.dbId, account.name, account.type_, account.created.strftime("%Y-%m-%d %H:%M:%S")])
                                print table.draw() + "\n"
                                if doArgs.no_confirm:
                                        self.api.Users(self.login).Accounts(doArgs.id).Delete()
                                        printer.out("Account deleted", printer.OK)
                                elif generics_utils.query_yes_no("Do you really want to delete account with id "+str(account.dbId)):
                                        self.api.Users(self.login).Accounts(doArgs.id).Delete() 
                                        printer.out("Account deleted", printer.OK)
                        return 0
            
                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
                        self.help_delete()
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
                    
        def help_delete(self):
                doParser = self.arg_delete()
                doParser.print_help()
                
        