from __future__ import division
from hurry.filesize import size

from hammr.lib.argumentParser import ArgumentParser, ArgumentParserError
from hammr.lib.cmdHamr import Cmd, HammrGlobal
from hammr.utils import *

__author__="UShareSoft"


class Quota(Cmd, HammrGlobal):
        """List the status of all the quotas that can be set for the user (disk usage, generations, scans and number of templates)"""
    
        cmd_name="quota"
    
        def __init__(self):
                super(Quota, self).__init__()
                
        def arg_list(self):
                doParser = ArgumentParser(prog=self.cmd_name+" list", add_help = True, description="Displays the user’s quota information")
                return doParser           

        def do_list(self, args):
                try:                        
                        #call UForge API
                        printer.out("Getting quotas for ["+self.login+"] ...")
                        quotas = self.api.Users(self.login).Quotas.Get()
                        if quotas is None or not hasattr(quotas, 'get_quota'):
                                printer.out("No quotas available")
                        else:            
                                values={};
                                for quota in quotas.get_quota():
                                        if quota.limit==-1:
                                                nb=" ("+str(quota.nb)+")"
                                        else:
                                                nb=" ("+str(quota.nb)+"/"+str(quota.limit)+")"
                                                
                                        if quota.type_ == constants.QUOTAS_SCAN:                                                
                                                text="Scan"+ ("s" if quota.nb>1 else "") +nb
                                        elif quota.type_ == constants.QUOTAS_TEMPLATE:
                                                text="Template"+ ("s" if quota.nb>1 else "") +nb
                                        elif quota.type_ == constants.QUOTAS_GENERATION:
                                                text="Generation"+ ("s" if quota.nb>1 else "") +nb
                                        elif quota.type_ == constants.QUOTAS_DISK_USAGE:
                                                text="Disk usage"+" ("+size(quota.nb)+")"
                                    
                                        if quota.limit!=-1:
                                                values[text]=int(quota.nb/quota.limit*50)
                                        else:
                                                values[text]=-1
                               
                                ascii_bar_graph.print_graph(values)
                        return 0
                                         
                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
                        self.help_list()
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
                    
        def help_list(self):
                doParser = self.arg_list()
                doParser.print_help()
                
        