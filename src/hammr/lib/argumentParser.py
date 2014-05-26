# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="UShareSoft"
__date__ ="$Jan 21, 2014 5:48:54 PM$"

import argparse

class ArgumentParserError(Exception): pass

class ArgumentParser(argparse.ArgumentParser):
    
	def error(self, message):
        	raise ArgumentParserError(message)
            
        def format_help(self):
                formatter = self._get_formatter()
                
                # description
                formatter.add_text(self.description)
                
                # usage
                formatter.add_usage(self.usage, self._actions,
                                    self._mutually_exclusive_groups)

                # positionals, optionals and user-defined groups
                for action_group in self._action_groups:
                    formatter.start_section(action_group.title)
                    formatter.add_text(action_group.description)
                    formatter.add_arguments(action_group._group_actions)
                    formatter.end_section()

                # epilog
                formatter.add_text(self.epilog)

                # determine help from format above
                return formatter.format_help()

class HammrArgumentParser(ArgumentParser):
            
        def format_help(self):
                formatter = self._get_formatter()

                # usage
                formatter.add_usage(self.usage, self._actions,
                                    self._mutually_exclusive_groups)

                # description
                formatter.add_text(self.description)

                #Add hammr command help (not managed by argparse but by python cmd2)
                formatter.start_section("commands")
                formatter.add_text("Available hammr commands")
                formatter.add_arguments(self.hammr_actions)
                formatter.end_section()

                # positionals, optionals and user-defined groups
                for action_group in self._action_groups:
                        if action_group.title=="positional arguments":  
                                newGroupActions=[]
                                #search for the cmds positionals argument to remove it from the help message
                                for action in action_group._group_actions:
                                        if action.dest!="cmds":
                                               newGroupActions.append(action)
                                action_group._group_actions=newGroupActions                                
                        formatter.start_section(action_group.title)
                        formatter.add_text(action_group.description)
                        formatter.add_arguments(action_group._group_actions)
                        formatter.end_section()
                
                

                # epilog
                formatter.add_text(self.epilog)

                # determine help from format above
                return formatter.format_help()
   