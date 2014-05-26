"""
	Override the default Cmd from cmd2 module with a subcommand feature
"""

from cmd2 import Cmd as Cmd2, EmptyStatement, ParsedString, Statekeeper
import pyparsing
import inspect
import sys
import datetime
import re
import StringIO
import subprocess
import os

try:
	from termcolor import colored
except ImportError:
	def colored(string, a=None, b=None, attrs=None):
		return string

# Clean up Cmd
class BaseCmd(object):pass
for a in dir(Cmd2):
	if a.startswith('do_'):
		if a != 'do_help':
			f = getattr(Cmd2, a)
			delattr(Cmd2, a)
			setattr(BaseCmd, a, f)

class Cmd(Cmd2, object):
	case_insensitive = False
	debug = True

	def colored(self, val, a=None, b=None, attrs=None):
		if self.stdout == self.initial_stdout:
			return colored(val, a, b , attrs)
        	return val

	def __init__(self):
		Cmd2.__init__(self)
		self.stderr = sys.stderr
		self.initial_stdin = sys.stdin
		self.initial_stderr = sys.stderr
		self.doc_leader = colored(self.__class__.__name__, 'white', attrs=['bold']) + ' help'
		self.doc_header = "Commands (type help <topic>):"
		self.maxcol = 120
		
		# Init functions for a subCmd
		def subCmd(class_, obj, command):
			if inspect.isclass(obj):
				obj = obj()

			def object_(self):
				return obj

			def do_(self, args):
				kept_state = Statekeeper(obj, ('stdout', 'stdin', 'stderr',))
				try:
					obj.stdout = self.stdout
					obj.stdin = self.stdin
					obj.stderr = self.stderr
					if not args:
						self.printError('*** No command\n')
						return obj.do_help("", stdout = self.stderr)
					else:
						if isinstance(args, ParsedString):
							args = args.parsed.args
						return obj.onecmd_plus_hooks(args)
				finally:			
					kept_state.restore()

			def complete_(self, text, line, start_index, end_index):
                                if hasattr(obj, 'subCmds'):
                                        inCmdList=line.split()                                        
                                        for cmd in obj.subCmds:
                                                if inCmdList[len(inCmdList)-1]==cmd:
                                                        return obj.subCmds[cmd].completenames(text)
                                        return obj.completenames(text)
				else:
                                        return obj.completenames(text)
                            
                            
			def help_(self):
				kept_state = Statekeeper(obj, ('stdout', 'stdin', 'stderr'))
				try:
					obj.stdout = self.stdout
					obj.stdin = self.stdin
					obj.stderr = self.stderr
					return obj.onecmd('help')
				finally:			
					kept_state.restore()

			setattr(class_, 'do_' + command, do_)
			setattr(class_, 'complete_' + command, complete_)
			setattr(class_, 'help_' + command, help_)
			setattr(class_, 'object_' + command, object_)
			return obj

		if hasattr(self, 'subCmds'):
			for cmd in self.subCmds:
				subCmd(self.__class__, self.subCmds[cmd], cmd)

	def printError(self, errmsg):
		self.stderr.write(self.colored(str(errmsg), 'red'))

	def default(self, line):
		"""Called on an input line when the command prefix is not recognized.

		If this method is not overridden, it prints an error message and
		returns.

		"""
		self.printError('*** Command not found: %s\n'%line)

	def do_help(self, arg, stdout = None):
		'List available commands with "help" or detailed help with "help cmd".'
		if stdout == None:
			stdout = self.stdout
		# Call help for command
		def callHelp(arg, depth = True, stdout = None, stderr = None):
			if stdout == None:
				stdout = self.stdout
			if stderr == None:
				stderr = self.stderr
			if not depth:
				try:
					func = getattr(self, 'object_' + arg)
					doc = func().__doc__
					if doc:
						stdout.write("%s\n"%str(doc))
					return
				except AttributeError:
					pass
			try:
				func = getattr(self, 'help_' + arg)
				func()
			except AttributeError:
				try:
					doc = getattr(self, 'do_' + arg).__doc__
					if doc:
						stdout.write("%s\n"%str(doc))
						return
				except AttributeError:
					pass
				stderr.write(self.colored("%s\n"%str(self.nohelp % (arg,)), 'red'))

		# Create a help sum
		def sumHelp(arg, column):
			keepstate = Statekeeper(self, ('stdout', 'stderr',))
			keepsys = Statekeeper(sys, ('stdout', 'stderr',))
			try:
				data  = None
				stdout = StringIO.StringIO()

				# Replace stderr and stdout
				sys.stdout = self.stdout = stdout
				self.stderr = sys.stderr = StringIO.StringIO()

				callHelp(arg, False, stdout=stdout)
				data = stdout.getvalue()
				#if not data or len(data) == 0:
				#	data = str(self.nohelp % (arg,))

				data = data.split('\n', 1)[0]
				return  (data[:(column-3)] + '...') if len(data) > column else data
			finally:
				# Restore
				keepstate.restore()
				keepsys.restore()

		# Forward help
		args = re.split('\s+', arg, 1)		
		if len(args) > 1:
			if hasattr(self, 'object_' + args[0]):
				funct = getattr(self, 'object_' + args[0])
				obj = funct()
				return obj.onecmd('help ' + args[1])
			else:
				arg = args[0]

		if arg:
			return callHelp(arg, stdout=stdout)
		else:
			names = self.get_names()
			cmds_doc = []
			cmds_undoc = []
			help = {}
			for name in names:
				if name[:5] == 'help_':
					help[name[5:]]=1
			names.sort()
			# There can be duplicates if routines overridden
			prevname = ''
			for name in names:
				if name[:3] == 'do_':
					if name == prevname:
						continue
					prevname = name
					cmd=name[3:]
					if cmd in help:
						cmds_doc.append(cmd)
						del help[cmd]
					elif getattr(self, name).__doc__:
						cmds_doc.append(cmd)
					else:
						cmds_undoc.append(cmd)

			# Print
			if self.ruler:
				stdout.write("%s\n"%str(self.ruler * self.maxcol))
			stdout.write("%s\n"%str(self.doc_leader))
			if self.ruler:
				stdout.write("%s\n"%str(self.ruler * self.maxcol))
			cmdMaxCol = 30
			helpMaxCol = self.maxcol - cmdMaxCol - 3
			for cmd in cmds_doc:
				stdout.write(str('{0:<'+str(cmdMaxCol)+'}| {1:<' + str(helpMaxCol) + '}\n').format(cmd, sumHelp(cmd, helpMaxCol)))

	def parsed(self, raw, **kwargs):
		if isinstance(raw, ParsedString):
			p = raw
		else:
			# preparse is an overridable hook; default makes no changes
			s = self.preparse(raw, **kwargs)
			s = self.inputParser.transformString(s.lstrip())
			s = self.commentGrammars.transformString(s)
			for (shortcut, expansion) in self.shortcuts:
				if s.lower().startswith(shortcut):
					s = s.replace(shortcut, expansion + ' ', 1)
					break
			result = self.parser.parseString(s)
			if isinstance(result.command, pyparsing.ParseResults):
				result.command = result.command[0]
			if isinstance(result.multilineCommand, pyparsing.ParseResults):
				result.multilineCommand = result.multilineCommand[0]
			result['raw'] = raw		
			result['command'] = result.multilineCommand or result.command	
			result = self.postparse(result)
			p = ParsedString(result.args)
			p.parsed = result
			p.parser = self.parsed
		for (key, val) in kwargs.items():
			p.parsed[key] = val
		return p

	def _init_parser(self):
		#outputParser = (pyparsing.Literal('>>') | (pyparsing.WordStart() + '>') | pyparsing.Regex('[^=]>'))('output')
		outputParser = (pyparsing.Literal(self.redirector *2) | \
					   (pyparsing.WordStart() + self.redirector) | \
						pyparsing.Regex('[^=]' + self.redirector))('output')
		inputMark = pyparsing.Literal('<')('input')
		
		terminatorParser = pyparsing.Or([(hasattr(t, 'parseString') and t) or pyparsing.Literal(t) for t in self.terminators])('terminator')
		stringEnd = pyparsing.stringEnd ^ '\nEOF'
		self.multilineCommand = pyparsing.Or([pyparsing.Keyword(c, caseless=self.case_insensitive) for c in self.multilineCommands])('multilineCommand')
		oneLineCommand = (~self.multilineCommand + pyparsing.Word(self.legalChars))('command')
		pipe = pyparsing.Keyword('|', identChars='|')
		self.commentGrammars.ignore(pyparsing.quotedString).setParseAction(lambda x: '')
		doNotParse = self.commentGrammars | self.commentInProgress | pyparsing.quotedString
		afterElements = \
			pyparsing.Optional(inputMark + pyparsing.SkipTo(outputParser ^ pipe ^ stringEnd, ignore=doNotParse).setParseAction(lambda x: x[0].strip())('inputFrom')) + \
			pyparsing.Optional(pipe + pyparsing.SkipTo(outputParser ^ stringEnd, ignore=doNotParse)('pipeTo')) + \
			pyparsing.Optional(outputParser + pyparsing.SkipTo(stringEnd, ignore=doNotParse).setParseAction(lambda x: x[0].strip())('outputTo'))
		if self.case_insensitive:
			self.multilineCommand.setParseAction(lambda x: x[0].lower())
			oneLineCommand.setParseAction(lambda x: x[0].lower())
		if self.blankLinesAllowed:
			self.blankLineTerminationParser = pyparsing.NoMatch
		else:
			self.blankLineTerminator = (pyparsing.lineEnd + pyparsing.lineEnd)('terminator')
			self.blankLineTerminator.setResultsName('terminator')
			self.blankLineTerminationParser = ((self.multilineCommand ^ oneLineCommand) + pyparsing.SkipTo(self.blankLineTerminator, ignore=doNotParse).setParseAction(lambda x: x[0].strip())('args') + self.blankLineTerminator)('statement')
		self.multilineParser = (((self.multilineCommand ^ oneLineCommand) + pyparsing.SkipTo(terminatorParser, ignore=doNotParse).setParseAction(lambda x: x[0].strip())('args') + terminatorParser)('statement') +
								pyparsing.SkipTo(outputParser ^ inputMark ^ pipe ^ stringEnd, ignore=doNotParse).setParseAction(lambda x: x[0].strip())('suffix') + afterElements)
		self.multilineParser.ignore(self.commentInProgress)
		self.singleLineParser = ((oneLineCommand + pyparsing.SkipTo(terminatorParser ^ stringEnd ^ pipe ^ outputParser ^ inputMark, ignore=doNotParse).setParseAction(lambda x:x[0].strip())('args'))('statement') +
								 pyparsing.Optional(terminatorParser) + afterElements)
		#self.multilineParser = self.multilineParser.setResultsName('multilineParser')
		#self.singleLineParser = self.singleLineParser.setResultsName('singleLineParser')
		self.blankLineTerminationParser = self.blankLineTerminationParser.setResultsName('statement')
		self.parser = self.prefixParser + (
			stringEnd |
			self.multilineParser |
			self.singleLineParser |
			self.blankLineTerminationParser | 
			self.multilineCommand + pyparsing.SkipTo(stringEnd, ignore=doNotParse)
			)
		self.parser.ignore(self.commentGrammars)
		
		fileName = pyparsing.Word(self.legalChars + '/\\')
		inputFrom = fileName('inputFrom')
		# a not-entirely-satisfactory way of distinguishing < as in "import from" from <
		# as in "lesser than"
		self.inputParser = inputMark + pyparsing.Optional(inputFrom) + pyparsing.Optional('>') + \
						   pyparsing.Optional(fileName) + (pyparsing.stringEnd | '|')
		self.inputParser.ignore(self.commentInProgress)


	def redirect_streams(self, statement):
		self.kept_state = Statekeeper(self, ('stdout','stdin','stderr',))			
		self.kept_sys = Statekeeper(sys, ('stdout','stdin','stderr',))
		if statement.parsed.pipeTo:
			self.redirect = subprocess.Popen(statement.parsed.pipeTo, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
			sys.stdout = self.stdout = self.redirect.stdin
		elif statement.parsed.output:
			if (not statement.parsed.outputTo) and (not can_clip):
				raise EnvironmentError('Cannot redirect to paste buffer; install ``xclip`` and re-run to enable')

			if statement.parsed.outputTo:
				mode = 'w'
				if statement.parsed.output == 2 * self.redirector:
					mode = 'a'
				sys.stdout = self.stdout = open(os.path.expanduser(statement.parsed.outputTo), mode)							
			else:
				sys.stdout = self.stdout = tempfile.TemporaryFile(mode="w+")
				if statement.parsed.output == '>>':
					self.stdout.write(get_paste_buffer())

		if statement.parsed.input:
			if (not statement.parsed.inputFrom) and (not can_clip):
				raise EnvironmentError('Cannot redirect from paste buffer; install ``xclip`` and re-run to enable')

			if statement.parsed.inputFrom:
				mode = 'r'
				sys.stdin = self.stdin = open(os.path.expanduser(statement.parsed.inputFrom), mode)					
			else:
				self.stdin.write(get_paste_buffer())

	def restore_streams(self, statement):
		if self.kept_state:
			if statement.parsed.output:
				if not statement.parsed.outputTo:
					self.stdout.seek(0)
					write_to_paste_buffer(self.stdout.read())
				self.stdout.close()
			elif statement.parsed.pipeTo:
				for result in self.redirect.communicate():			  
					self.kept_state.stdout.write(result or '')						
				self.stdout.close()
			if statement.parsed.input:
				self.stdin.close()
			self.kept_state.restore()  
			self.kept_sys.restore()
			self.kept_state = None

	def pseudo_raw_input(self, prompt):
		"""copied from cmd's cmdloop; like raw_input, but accounts for changed stdin, stdout"""
		if self.use_rawinput:
			line = raw_input(prompt)
		else:
			sys.stderr.write(prompt)
			sys.stderr.flush()
			line = self.stdin.readline()
			if not len(line):
				raise EOFError()
			else:
				if line[-1] == '\n': # this was always true in Cmd
					line = line[:-1] 
		return line

	def _cmdloop(self, intro=None):
		"""Repeatedly issue a prompt, accept input, parse an initial prefix
		off the received input, and dispatch to action methods, passing them
		the remainder of the line as argument.
		"""

		# An almost perfect copy from Cmd; however, the pseudo_raw_input portion
		# has been split out so that it can be called separately
		
		self.preloop()
		if self.use_rawinput and self.completekey:
			try:
				import readline
				self.old_completer = readline.get_completer()
				readline.set_completer(self.complete)
				readline.parse_and_bind(self.completekey+": complete")
			except ImportError:
				pass
		try:
			if intro is not None:
				self.intro = intro
			if self.intro:
				self.stdout.write(str(self.intro)+"\n")
			stop = None
			while (stop!=1 or stop!=True):
				try:
					if self.cmdqueue:
						line = self.cmdqueue.pop(0)
					else:
						line = self.pseudo_raw_input(self.prompt)
					if (self.echo) and (isinstance(self.stdin, file)):
						self.stdout.write(line + '\n')
					stop = self.onecmd_plus_hooks(line)
				except EOFError:
					pass
			self.postloop()
		finally:
			if self.use_rawinput and self.completekey:
				try:
					import readline
					readline.set_completer(self.old_completer)
				except ImportError:
					pass	
			return stop
        
        def run_commands_at_invocation(self, callargs):
                for initial_command in callargs:
                    code= self.onecmd_plus_hooks(initial_command + '\n')
                    if code:
                        return code

	def onecmd_plus_hooks(self, line):
		# The outermost level of try/finally nesting can be condensed once
		# Python 2.4 support can be dropped.
		stop = 0
		try:
			try:
				statement = None
				statement = self.complete_statement(line)
				(stop, statement) = self.postparsing_precmd(statement)
				if stop:
					return self.postparsing_postcmd(stop)
				if statement.parsed.command not in self.excludeFromHistory:
					self.history.append(statement.parsed.raw)	  
				try:
					self.redirect_streams(statement)
					timestart = datetime.datetime.now()
					statement = self.precmd(statement)
					stop = self.onecmd(statement)
					stop = self.postcmd(stop, statement)
					if self.timing:
						self.pfeedback('Elapsed: %s' % str(datetime.datetime.now() - timestart))
                                except KeyboardInterrupt:
                                        print "\nExiting command..."
				except BaseException as e:
					self.perror(str(e), statement)
				finally:
					self.restore_streams(statement)
                        except pyparsing.ParseException as e:
                                print "File parsing error with line: "+line.rstrip()
			except EmptyStatement:
				return 0
			except Exception as e:
				self.perror(str(e), statement)	
		except Exception as e:
			self.perror(str(e))			
		finally:
			return self.postparsing_postcmd(stop) 
        

class CmdUtils(BaseCmd, Cmd):
	"""Utility box"""
	def __init__(self):
		super(CmdUtils, self).__init__()
		self.doc_leader = colored("Utility box", 'white', attrs=['bold']) + ' help'
                
class HammrGlobal:
    
        def set_globals(self, api, login, password):
                self.api=api
                self.login=login
                self.password=password

