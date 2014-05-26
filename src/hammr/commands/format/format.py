
__author__="UShareSoft"


from texttable import Texttable
from hammr.lib.argumentParser import ArgumentParser, ArgumentParserError
from hammr.lib.cmdHamr import Cmd, HammrGlobal
from hammr.utils import *



class Format(Cmd, HammrGlobal):
        """List all the formats the user has access to (cloud, virtual, physical)"""
    
        cmd_name="format"
    
        def __init__(self):
                super(Format, self).__init__()    
                
        def arg_list(self):
                doParser = ArgumentParser(prog=self.cmd_name+" list", add_help = True, description="Displays all the machine image formats for the user")
                return doParser  

        def do_list(self, args):
                try:
                        
                        #call UForge API
                        printer.out("Getting generation formats for ["+self.login+"] ...")
                        formats = self.api.Users(self.login).Formats.Getall(None, None)
                        if formats is None or not hasattr(formats, 'get_imageFormat'):
                                printer.out("No generation formats available")
                        else:
                                table = Texttable(800)
                                table.set_cols_dtype(["t","t","t","t","t","t"])
                                table.set_cols_align(["l", "l", "l", "c", "c", "c"])
                                table.header(["Name", "Access", "Active", "Virtual Format", "Cloud Format", "Physical Format"])
                                formats = generics_utils.oder_list_object_by(formats.get_imageFormat(), "name")
                                for format in formats:
                                        for mappedFormat in generate_utils.VIRTUAL_FORMATS:
                                                if isinstance(generate_utils.VIRTUAL_FORMATS[mappedFormat], list):
                                                        for ff in generate_utils.VIRTUAL_FORMATS[mappedFormat]:
                                                                if format.name==ff:
                                                                        table.add_row([mappedFormat, format.access, format.active, "X", "", ""])
                                                elif format.name==generate_utils.VIRTUAL_FORMATS[mappedFormat]:
                                                        table.add_row([mappedFormat, format.access, format.active, "X", "", ""])
                                for format in formats:
                                        for mappedFormat in generate_utils.CLOUD_FORMATS:
                                                if isinstance(generate_utils.CLOUD_FORMATS[mappedFormat], list):
                                                        for ff in generate_utils.CLOUD_FORMATS[mappedFormat]:
                                                                if format.name==ff:
                                                                        table.add_row([mappedFormat, format.access, format.active, "", "X", ""])
                                                elif format.name==generate_utils.CLOUD_FORMATS[mappedFormat]:
                                                        table.add_row([mappedFormat, format.access, format.active, "", "X", ""])
                                for format in formats:
                                        for mappedFormat in generate_utils.PHYSICAL_FORMATS:
                                                if isinstance(generate_utils.PHYSICAL_FORMATS[mappedFormat], list):
                                                        for ff in generate_utils.PHYSICAL_FORMATS[mappedFormat]:
                                                                if format.name==ff:
                                                                        table.add_row([mappedFormat, format.access, format.active, "", "", "X"])
                                                elif format.name==generate_utils.PHYSICAL_FORMATS[mappedFormat]:
                                                        table.add_row([mappedFormat, format.access, format.active, "", "", "X"])
                                print table.draw() + "\n"
                                printer.out("Found "+str(len(formats))+" generation formats")
                                
                        return 0
                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
                        self.help_list()
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
                    
        def help_list(self):
                doParser = self.arg_list()
                doParser.print_help()
                
        