#Radio Control - Event
#Martin O'Hanlon
#stuffaboutcode.com

#Generic class to hold an event
#Events are queued and handled FIFO
class Event():
    class EventType():
        ON = 0
        OFF = 1
        PLAYLISTL = 2
        PLAYLISTM = 3
        VOL = 4
        SKIPTRACK = 5
        PAUSE = 6
        SHUTDOWN = 7
        PINGMPD = 8
        
    def __init__(self, eventType, value = None):
        self.eventType = eventType
        self.value = value

