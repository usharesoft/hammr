
__author__="UShareSoft"

from texttable import Texttable
from hammr.lib.argumentParser import ArgumentParser, ArgumentParserError
from hammr.lib.cmdHamr import Cmd, HammrGlobal
from hammr.utils import *
from uforge.objects.xsd0 import *
from hurry.filesize import size

class Bundle(Cmd, HammrGlobal):
        """List or delete existing bundles (mysoftware) on UForge"""
    
        cmd_name="bundle"
    
        def __init__(self):
                super(Bundle, self).__init__()
                
        def arg_list(self):
                doParser = ArgumentParser(prog=self.cmd_name+" list", add_help = True, description="Lists all the bundles that have been registered in the UForge server")
                return doParser   

        def do_list(self, args):  
                        try:
                                #call UForge API
                                printer.out("Getting all your bundles ...")
                                bundles = self.api.Users(self.login).Mysoftware.Getall()
                                if bundles is None or not hasattr(bundles, 'get_mySoftwareItem') or len(bundles.get_mySoftwareItem())<1:
                                        printer.out("No bundles available")
                                else:
                                        table = Texttable(800)
                                        table.set_cols_dtype(["t","t","t", "t","t", "t"])
                                        table.header(["Id", "Name", "Version", "Description", "Size", "Imported"]) 
                                        bundles = generics_utils.oder_list_object_by(bundles.get_mySoftwareItem(), "name")
                                        for bundle in bundles:
                                                table.add_row([bundle.dbId, bundle.name, bundle.version, bundle.description, size(bundle.size), "X" if bundle.imported else ""])
                                        print table.draw() + "\n"
                                        printer.out("Found "+str(len(bundles))+" bundles")
                                        
                                return 0
                        except Exception as e:        
                                print generics_utils.print_uforge_exception(e)
                                

                    
        def help_list(self):
                doParser = self.arg_list()
                doParser.print_help()
                
        
        def arg_delete(self):
                doParser = ArgumentParser(prog=self.cmd_name+" delete", add_help = True, description="Deletes an existing bundle")
                mandatory = doParser.add_argument_group("mandatory arguments")
                mandatory.add_argument('--id', dest='id', required=True, help="the ID of the bundle to delete")
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
                        printer.out("Searching bundle with id ["+doArgs.id+"] ...")
                        myBundle = self.api.Users(self.login).Mysoftware(doArgs.id).Get()
                        if myBundle is None or type(myBundle) is not mySoftware:
                                printer.out("Bundle not found", printer.WARNING)
                        else:
                                table = Texttable(800)
                                table.set_cols_dtype(["t","t","t", "t","t", "t"])
                                table.header(["Id", "Name", "Version", "Description", "Size", "Imported"])
                                table.add_row([myBundle.dbId, myBundle.name, myBundle.version, myBundle.description, size(myBundle.size), "X" if myBundle.imported else ""])
                                print table.draw() + "\n"                            
                                if generics_utils.query_yes_no("Do you really want to delete bundle with id "+str(myBundle.dbId)):
                                        self.api.Users(self.login).Mysoftware(myBundle.dbId).Delete() 
                                        printer.out("Bundle deleted", printer.OK)
                                
            
                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
                        self.help_delete()
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
                                

                    
        def help_delete(self):
                doParser = self.arg_delete()
                doParser.print_help()
        