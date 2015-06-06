#Radio Control - Volume Control
#Martin O'Hanlon
#stuffaboutcode.com
import threading

from MCP3008 import MCP3008
from event import Event
from time import sleep
from collections import deque

#Constants

#SPI constants
SPIBUS = 0
SPIDEVICE = 0
SPICHANNEL = 0

#how often to refresh the volume
REFRESHTIME = 0.1

AVGLENGTH = 5

class VolumeControl(threading.Thread):

    def __init__(self, eventQ):
        #setup threading
        threading.Thread.__init__(self)
    
        self.running = False
        self.stopped = True
        self.eventQ = eventQ
        self.values = deque()
        
    def run(self):
        self.running = True
        self.stopped = False
        #open the spi channel
        with MCP3008(channel = SPICHANNEL) as volumeDial:
            #set initial value
            self.volume = 0
            self.volume = self._readVolume(volumeDial)
            self._raiseEvents(self.volume)
            
            self.lastVolume = self.volume
            while(not self.stopped):
                self.volume = self._readVolume(volumeDial)
                
                #has the volume changed by more than 1? This stops the volume flickering between 2 values
                diff = self.lastVolume - self.volume
                if diff < 0: diff = diff * -1
                if diff > 1:
                    #raise an event
                    self._raiseEvents(self.volume)
                    self.lastVolume = self.volume
                 
                sleep(REFRESHTIME)
                
            self.running = False

    def _raiseEvents(self, volume):
        #raise the event
        self.eventQ.put(Event(Event.EventType.VOL, volume))
        
    def _readVolume(self, volumeDial):
        #read the data
        data = volumeDial.read()

        #debug
        #print "data = {}".format(data)
        
        #add it to the list
        self.values.append(data)
        #if the number of averages is over the length, remove from the list
        if len(self.values) > AVGLENGTH:
            self.values.popleft()
        #work out the average
        avgData = sum(self.values) / len(self.values)
        return self._convertToVolume(avgData)

    def _convertToVolume(self, data):
        volume = (data / 1023.0) * 100
        volume = int(round(volume))
        return volume
    
    def stop(self):
        self.stopped = True
        while(self.running):
            sleep(0.01)

