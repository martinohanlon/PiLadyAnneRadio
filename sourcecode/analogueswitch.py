#Radio Control - Analogue Switch
#Martin O'Hanlon
#stuffaboutcode.com

import threading

from MCP3008 import MCP3008
from time import sleep

class AnalogueSwitch(threading.Thread):
    """
    A class which uses a MCP3008 analogue to digital converter to read values from a switch which
    outputs a variable voltage and is therefore using digital input is unsuitable.

    threshold is the value at which the switch flicks from false to true
    """
    def __init__(self, bus, device, channel, threshold = 500, refreshTime = 0.1, callback = None):
        
        #setup threading
        threading.Thread.__init__(self)

        #persist properties
        self.bus = bus
        self.device = device
        self.channel = channel
        self.threshold = threshold
        self.refreshTime = refreshTime
        self.callback = callback
        
        self.running = False
        self.stopped = True
 
    def run(self):
        self.running = True
        self.stopped = False
        #open the spi channel
        with MCP3008(self.bus, self.device, self.channel) as switch:
            #set initial value
            self.on = self._readOnOff(switch)
            self._doCallback()
            lastOn = self.on
            while(not self.stopped):
                #has the switch changed?
                self.on = self._readOnOff(switch)
                if self.on != lastOn:
                    self._doCallback()
                    lastOn = self.on
                sleep(self.refreshTime)
                
            self.running = False

    def _readOnOff(self, switch):
        data = switch.read()
        if data >= self.threshold:
            return True
        else:
            return False

    def _doCallback(self):
        if self.callback != None:
            self.callback(self.on)
            
    def stop(self):
        self.stopped = True
        while(self.running):
            sleep(0.01)

#tests
if __name__ == "__main__":

    def myCallback(value):
        print value

    switch = AnalogueSwitch(0,0,1,100,0.1,myCallback)
    
    try:
        switch.start()
        while True:
            sleep(0.1)
            
    finally:
        switch.stop()

    
        
