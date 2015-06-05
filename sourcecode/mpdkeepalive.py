import threading
import mpd
import socket 
from time import sleep
from event import Event

DEFAULT_INTERVAL = 5

class MPDKeepAlive(threading.Thread):
    def __init__(self, eventQ, interval = DEFAULT_INTERVAL):
        #setup threading
        threading.Thread.__init__(self)
        
        self.eventQ = eventQ
        self.interval = interval

        self.running = False
        self.stopped = True

    def run(self):
        self.running = True
        self.stopped = False
        while(not self.stopped):
            self.eventQ.put(Event(Event.EventType.PINGMPD))
            sleep(self.interval)

        self.running = False

    def stop(self):
        self.stopped = True
        while(self.running):
            sleep(0.01)

