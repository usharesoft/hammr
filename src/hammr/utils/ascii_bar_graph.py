# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="UShareSoft"

def print_graph(values):
        max=0
        for v in values:
                if len(v)>max:
                        max=len(v)
        for v in values:
                if len(v)<max:
                        newV=v+(" " * int(max-len(v)))
                        if values[v]!=-1:
                                print newV, values[v]*'|'+'-'*int(50-values[v])
                        else:
                                print newV,20*'-'+"UNLIMITED"+21*'-'
                else:
                        if values[v]!=-1:
                                print v, values[v]*'|'+'-'*int(50-values[v])
                        else:
                                print v,20*'-'+"UNLIMITED"+21*'-'
                        
                        
