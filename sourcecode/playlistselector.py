#Radio Control - Playlist Selector
#Martin O'Hanlon
#stuffaboutcode.com

from threading import Timer
from MCP3008 import MCP3008
from analogueswitch import AnalogueSwitch
from event import Event
from time import sleep

SPIBUS = 0
SPIDEVICE = 0
MSPICHANNEL = 4
LSPICHANNEL = 5
SPISWITCHVALUE = 900
REFRESHTIME = 0.1

#what delay should be put in to stop M events being created
# when the selector goes from L to OFF 
SWITCHDELAY = 1

class PlaylistSelector():
    def __init__(self, eventQ):
        self.eventQ = eventQ
        self.waitingMEvent = None

    def start(self):
        self.mSwitch = AnalogueSwitch(SPIBUS, SPIDEVICE, MSPICHANNEL,
                                      SPISWITCHVALUE, REFRESHTIME,
                                      self._mCallback)

        self.lSwitch = AnalogueSwitch(SPIBUS, SPIDEVICE, LSPICHANNEL,
                                      SPISWITCHVALUE, REFRESHTIME,
                                      self._lCallback)

        self.mSwitch.start()
        self.lSwitch.start()

    def _putPlaylistMEvent(self):
        self.eventQ.put(Event(Event.EventType.PLAYLISTM))
    
    def _mCallback(self, on):
        self.m = on
        #if M has gone True create an event on a timer
        if self.m:
            self.waitingMEvent = Timer(SWITCHDELAY, self._putPlaylistMEvent)
            self.waitingMEvent.start()

        #if M has gone False and there is an event waiting on a timer, cancel it
        if not self.m and self.waitingMEvent != None:
            self.waitingMEvent.cancel()
            
    def _lCallback(self, on):
        self.l = on
        if self.l:
            self.eventQ.put(Event(Event.EventType.PLAYLISTL))    
   
    def stop(self):
        self.mSwitch.stop()
        self.lSwitch.stop()
