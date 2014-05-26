# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="UShareSoft"

from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer

class Download():
        
        def __init__(self, name='Status: '):
                #widgets = ['Status: ', Percentage(), ' ', Bar('>'), ' ', ETA(), ' ', FileTransferSpeed()]
                widgets = [name, Percentage(), ' ', Bar('>'), ' ', ETA()]
                self.pbar = ProgressBar(widgets=widgets, maxval=100).start()
        
        
        def progress_update(self, count, blockSize, totalSize):    
                percent=None
                if totalSize-blockSize<=0:
                        percent=50
                else:
                        if totalSize-(count*blockSize)>=0:
                                percent = int(count*blockSize*100/totalSize)
                if percent is not None:
                        self.pbar.update(percent)
                
        def progress_finish(self):
                self.pbar.finish()