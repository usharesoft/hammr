
__author__="UShareSoft"

from hurry.filesize import size

from texttable import Texttable
from hammr.lib.argumentParser import ArgumentParser, ArgumentParserError
from argparse import RawTextHelpFormatter
from hammr.lib.cmdHamr import Cmd, HammrGlobal
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer
from hammr.utils import *



class Os(Cmd, HammrGlobal):
        """List all the OSes the user has access to. Includes, name, version, architecture and release date. You can also search for available packages"""
    
        cmd_name="os"
    
        def __init__(self):
                super(Os, self).__init__()

    
        def arg_list(self):
                doParser = ArgumentParser(prog=self.cmd_name+" list", add_help = True, description="Displays all the operating systems available to use by the use")
                return doParser   

        def do_list(self, args):
                try:                        
                        #call UForge API
                        printer.out("Getting distributions for ["+self.login+"] ...")
                        distributions = self.api.Users(self.login).Distros.Getall(None, None)
                        if distributions is None or not hasattr(distributions, 'get_distribution'):
                                printer.out("No distributions available")
                        else:
                                table = Texttable(800)
                                table.set_cols_dtype(["t","t","t","t","t", "t"])
                                table.header(["Id", "Name", "Version", "Architecture", "Release Date", "Profiles"])
                                distributions = generics_utils.oder_list_object_by(distributions.get_distribution(), "name")
                                for distribution in distributions:
                                        profiles = self.api.Distributions(distribution.dbId).Profiles.Getall()
                                        if hasattr(profiles, 'distribProfile'):
                                                profile_text=""
                                                for profile in profiles.distribProfile:
                                                        profile_text+=profile.name+"\n"
                                                table.add_row([distribution.dbId, distribution.name, distribution.version, distribution.arch, distribution.releaseDate.strftime("%Y-%m-%d %H:%M:%S") if distribution.releaseDate is not None else "", profile_text])
                                
                                        else:
                                                table.add_row([distribution.dbId, distribution.name, distribution.version, distribution.arch, distribution.releaseDate.strftime("%Y-%m-%d %H:%M:%S") if distribution.releaseDate is not None else "", "-"])
                                print table.draw() + "\n"
                                printer.out("Found "+str(len(distributions))+" distributions")
                        return 0
                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
                        self.help_list()
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
                    
        def help_list(self):
                doParser = self.arg_list()
                doParser.print_help()
              
                
                
        def arg_search(self):
                doParser = ArgumentParser(prog=self.cmd_name+" search", add_help = True, description="Search packages from an OS", formatter_class=RawTextHelpFormatter)
                mandatory = doParser.add_argument_group("mandatory arguments")
                mandatory.add_argument('--id', dest='id', required=True, help="Os id")
                mandatory.add_argument('--pkg', dest='pkg', required=True, help='''\
                Regular expression of the package:\n\
                "string" : search all packages wich contains "string"\n\
                "^string": search all packages wich start with "string"\n\
                "string$": search all packages wich end with "string"''')
                return doParser

        def do_search(self, args):
                try:
                        #add arguments
                        doParser = self.arg_search()
                        try:
                                doArgs = doParser.parse_args(args.split())
                        except SystemExit as e:
                                return
                        #call UForge API
                        printer.out("Search package '"+doArgs.pkg+"' ...")
                        distribution = self.api.Distributions(doArgs.id).Get()
                        printer.out("for OS '"+distribution.name+"', version "+distribution.version)
                        pkgs = self.api.Distributions(distribution.dbId).Pkgs.Getall(Search=doArgs.pkg, Version=distribution.version)
                        
                        if pkgs is None or not hasattr(pkgs, 'pkgs'):
                                printer.out("No package found")
                        else:
                            table = Texttable(800)
                            table.set_cols_dtype(["t","t","t","t","t","t"])
                            table.header(["Name", "Version", "Arch", "Release", "Build date", "Size"])
                            pkgs = generics_utils.oder_list_object_by(pkgs.get_pkgs().get_pkg(), "name")
                            for pkg in pkgs:
                                    table.add_row([pkg.name, pkg.version, pkg.arch, pkg.release, pkg.pkgBuildDate.strftime("%Y-%m-%d %H:%M:%S"), size(pkg.size)])
                            print table.draw() + "\n"
                            printer.out("Found "+str(len(pkgs))+" packages")
                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: "+str(e), printer.ERROR)
                        self.help_search()
                except Exception as e:        
                        print generics_utils.print_uforge_exception(e)
                    
        def help_search(self):
                doParser = self.arg_search()
                doParser.print_help()
                
        