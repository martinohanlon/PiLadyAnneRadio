#Radio Control - On/Off Switch
#Martin O'Hanlon
#stuffaboutcode.com
import threading

from MCP3008 import MCP3008
from analogueswitch import AnalogueSwitch
from event import Event
from time import sleep

SPIBUS = 0
SPIDEVICE = 0
SPICHANNEL = 1
SPISWITCHVALUE = 900
REFRESHTIME = 0.1

class OnOffSwitch():
    def __init__(self, eventQ):
        self.eventQ = eventQ

    def start(self):
        self.switch = AnalogueSwitch(SPIBUS,SPIDEVICE,SPICHANNEL,
                                     SPISWITCHVALUE,REFRESHTIME,
                                     self._onOffCallback)
        self.switch.start()

    def _onOffCallback(self, on):
        self.on = on
        self._raiseEvents()

    def _raiseEvents(self):
        #has the switch turned on or off? create an event
        if self.on:
            self.eventQ.put(Event(Event.EventType.ON))
        else:
            self.eventQ.put(Event(Event.EventType.OFF))

    def stop(self):
        self.switch.stop()

class OLDOnOffSwitch(threading.Thread):

    def __init__(self, eventQ):
        #setup threading
        threading.Thread.__init__(self)
        
        self.running = False
        self.stopped = True
        self.eventQ = eventQ
        
    def run(self):
        self.running = True
        self.stopped = False
        #open the spi channel
        with MCP3008(channel = SPICHANNEL) as onoff:
            #set initial value
            self.on = self._readOnOff(onoff)
            self._raiseEvents()

            lastOn = self.on
            while(not self.stopped):
                #has the switch changed?
                self.on = self._readOnOff(onoff)
                if lastOn != self.on:
                    self._raiseEvents()
                    lastOn = self.on
                
                sleep(REFRESHTIME)
                
            self.running = False

    def _raiseEvents(self):
        #has the switch turned on or off? create an event
        if self.on:
            self.eventQ.put(Event(Event.EventType.ON))
        else:
            self.eventQ.put(Event(Event.EventType.OFF))
        
    def _readOnOff(self, onoff):
        data = onoff.read()
        if data >= SPISWITCHVALUE:
            return True
        else:
            return False
            
    def stop(self):
        self.stopped = True
        while(self.running):
            sleep(0.01)
