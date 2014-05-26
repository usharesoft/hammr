# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="UShareSoft"

from termcolor import colored,cprint


WARNING="WARNING"
ERROR="ERROR"
OK="OK"

def out(text, state=""):
        if state==WARNING:
                cprint(WARNING+": ","yellow", attrs=['bold'], end=text+"\n")
        elif state==ERROR:
                cprint(ERROR+": ","red", attrs=['bold'], end=text+"\n")
        elif state==OK:
                cprint(OK+": ","green", attrs=['bold'], end=text+"\n")
        else:
                print(text)
