#Radio Control - Skip Track and Pause Control
#Martin O'Hanlon
#stuffaboutcode.com
from KY040 import KY040
from event import Event

CLOCKPIN = 5
DATAPIN = 6
SWITCHPIN = 13

class SkipTrackPause():
    def __init__(self, eventQ):
        self.eventQ = eventQ
        
        #create rotary encoder class
        self.rotenc = KY040(CLOCKPIN, DATAPIN, SWITCHPIN, self._rotaryChange, self._switchPressed)

    def start(self):
        #start the KY040
        self.rotenc.start()

    def stop(self):
        #stop the KY040
        self.rotenc.stop()

    def _rotaryChange(self, direction):
        #previous
        if direction == KY040.ANTICLOCKWISE:
            self.eventQ.put(Event(Event.EventType.SKIPTRACK, -1))
        #next
        elif direction == KY040.CLOCKWISE:
            self.eventQ.put(Event(Event.EventType.SKIPTRACK, 1))

    def _switchPressed(self):
        #pause
        self.eventQ.put(Event(Event.EventType.PAUSE))

