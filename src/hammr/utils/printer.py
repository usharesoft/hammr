# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="UShareSoft"

from termcolor import cprint

WARNING="WARNING"
ERROR="ERROR"
INFO="INFO"
OK="OK"

def out(text, state="", exitCode=None):
    if state==WARNING:
        cprint(WARNING+": ","yellow", attrs=['bold'], end=text+"\n")
    elif state==ERROR:
        cprint(ERROR+": ","red", attrs=['bold'], end=text+"\n")
    elif state==INFO:
        cprint(INFO+": ","blue", attrs=['bold'], end=text+"\n")
    elif state==OK:
        cprint(OK+": ","green", attrs=['bold'], end=text+"\n")
    else:
        print(text)
    if exitCode:
        exit(exitCode)
