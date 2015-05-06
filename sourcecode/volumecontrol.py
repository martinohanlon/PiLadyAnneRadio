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

#how low and high the volume control goes
SPIMINVALUE = 200
SPIMAXVALUE = 1023

#volume to spi analogue ranges
VOLUMETOANALOGUE = {0: [0, 0.0, 400.0],
                    35: [35, 300.0, 500.0],
                    40: [40, 490.0, 530.0],
                    45: [45, 520.0, 570.0],
                    50: [50, 560.0, 625.0],
                    55: [55, 615.0, 660.0],
                    60: [60, 640.0, 730.0],
                    65: [65, 720.0, 850.0],
                    70: [70, 800.0, 950.0],
                    75: [75, 900.0, 1000.0],
                    79: [75, 990.0, 1024.0]}

AVGLENGTH = 15

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
            
            lastVolume = self.volume
            while(not self.stopped):
                self.volume = self._readVolume(volumeDial)
                #has the volume changed?
                if lastVolume != self.volume:
                    #raise an event
                    self._raiseEvents(self.volume)
                    lastVolume = self.volume
                 
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
        #has the current volume moved outside its SPI range
        if data < VOLUMETOANALOGUE[self.volume][1] or data > VOLUMETOANALOGUE[self.volume][2]:
            #find the new range
            for volumeRange in VOLUMETOANALOGUE:
                if data > VOLUMETOANALOGUE[volumeRange][1] and data < VOLUMETOANALOGUE[volumeRange][2]:
                    return VOLUMETOANALOGUE[volumeRange][0]
        else:
            return self.volume
    
    def stop(self):
        self.stopped = True
        while(self.running):
            sleep(0.01)
