import threading
from time import sleep

DEFAULT_INTERVAL = 5

class MPDKeepAlive(threading.Thread):
    def __init__(self, mpd, mpdHost, mpdPort, interval = DEFAULT_INTERVAL):
        #setup threading
        threading.Thread.__init__(self)
        
        self.mpd = mpd
        self.interval = interval

        self.running = False
        self.stopped = True

    def run(self):
        self.running = True
        self.stopped = False
        while(not self.stopped):
            try:
                self.mpd.ping()
                
            except mpd.ConnectionError as e:
                print "Ping MPD connection error"
                #try and reconnect
                if self._reconnectMPD():
                    print "MPD reconnected"

            except socket.error as e:
                print "Ping socket error"
                #try and reconnect
                if self._reconnectMPD():
                    print "MPD reconnected"

            sleep(self.interval)

        self.running = False

    def stop(self):
        self.stopped = True
        while(self.running):
            sleep(0.01)

    def _reconnectMPD(self):
        #connect to MPD server
        success = False
        try:
            self.mpd.connect(self.mpdHost, self.mpdPort)
            success = True
        except:
            print "Failed to connect to mpd"
        return success
