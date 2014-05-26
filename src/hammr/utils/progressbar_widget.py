# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from progressbar import Widget



__author__="UShareSoft"


class Status(Widget):
    
    __slots__ = ('format_string',)
    TIME_SENSITIVE = True
    max_size=20

    def __init__(self, format='%s'):
            self.format_string = format


    def update(self, pbar):
            return self.format_string % self.status.percentage+"%: "+self.pretty_text(self.status.message)
    
    
    def pretty_text(self, text):
            if len(text) > self.max_size:
                    return text[0:self.max_size-3]+"..."
            else:
                    return self.stuff_text(text)
    
    def stuff_text(self, text):
            for i in range(self.max_size - len(text)):
                    text+=" "
            return text