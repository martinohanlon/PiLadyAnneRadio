#Radio Control
#Martin O'Hanlon
#stuffaboutcode.com

#imports
import RPi.GPIO as GPIO
import mpd
import socket

from time import sleep
from Queue import Queue
from threading import Timer

from event import Event
from onoffswitch import OnOffSwitch
from playlistselector import PlaylistSelector
from volumecontrol import VolumeControl
from skiptrackpause import SkipTrackPause
from mpdkeepalive import MPDKeepAlive

#Constants

#GPIO pin constants
AMPMUTEPIN = 22
SHUTDOWNPIN = 12
LEDPIN = 16

#MPD constants
MPDHOST = "localhost"
MPDPORT = "6600"

#Playlist constants
PLAYLISTNAMEM = "MartPlaylist"
PLAYLISTNAMEL = "LeePlaylist"

#previous track timeout
PREVTRACKTIMEOUT = 5.0

#shutdown button press time
SHUTDOWNBUTTONTIME = 2

class Amp():
    def __init__(self, mutePin):
        self.mutePin = mutePin

        #setup pins
        GPIO.setup(mutePin, GPIO.OUT)

    @property
    def muted(self):
        if GPIO.input(self.mutePin) == 1:
            return True
        else:
            return False

    def unmute(self):
        GPIO.output(self.mutePin, 1)

    def mute(self):
        GPIO.output(self.mutePin, 0)

class ShutdownButton():
    def __init__(self, eventQ):
        self.eventQ = eventQ
        GPIO.setup(SHUTDOWNPIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def start(self):
        GPIO.add_event_detect(SHUTDOWNPIN, GPIO.RISING, callback=self._shutdownCallback, bouncetime=250)
    
    def stop(self):
        GPIO.remove_event_detect(SHUTDOWNPIN)

    def _shutdownCallback(self, pin):
        #start the shutdown timer
        self.shutdownTimer = Timer(SHUTDOWNBUTTONTIME, self._shutdownTimer)
        self.shutdownTimer.start()
        
    def _shutdownTimer(self):
        #if the shutdown button is still pressed, raise the event
        if GPIO.input(SHUTDOWNPIN) == True:
            self.eventQ.put(Event(Event.EventType.SHUTDOWN))

class LED():
    def __init__(self, ledPin):
        self.ledPin = ledPin
        GPIO.setup(ledPin, GPIO.OUT)

    def on(self):
        GPIO.output(self.ledPin, True)

    def off(self):
        GPIO.output(self.ledPin, False)

class RadioControl():
    def __init__(self, mpdHost = "localhost", mpdPort = "6600"):
        #create properties
        self.mpdHost = mpdHost
        self.mpdPort = mpdPort
        self.playing = False
        self.playlist = None
        self.stopped = True
        self.prevTrackSkipActive = False

        #create events queue
        self.eventQ = Queue()

        #Create objects to manage controls

        #create on led
        self.onLED = LED(LEDPIN)
    
        #create amp
        self.amp = Amp(AMPMUTEPIN)

        #create on/off switch
        self.onOffSwitch = OnOffSwitch(self.eventQ)

        #create m/l selector
        self.playlistSwitch = PlaylistSelector(self.eventQ)

        #create volume control
        self.volControl = VolumeControl(self.eventQ)

        #create skip track & pause control
        self.stp = SkipTrackPause(self.eventQ)

        #create shutdown button control
        self.shutdownButton = ShutdownButton(self.eventQ)
        
    def start(self):

        #turn on led
        self.onLED.on()

        #create connection to MPD client / volumio
        self.mpd = mpd.MPDClient()
        self.mpd.connect(MPDHOST, MPDPORT)

        #create the mpd keep alive object
        mpdKeepAlive = MPDKeepAlive(self.mpd, MPDHOST, MPDPORT)
        mpdKeepAlive.start()
        
        #start up the controls
        self.onOffSwitch.start()
        self.playlistSwitch.start()
        self.volControl.start()
        self.stp.start()
        self.shutdownButton.start()

        try:
            self.stopped = False
            #process events
            while(not self.stopped):
                
                while not self.eventQ.empty():
                    event = self.eventQ.get()
                    #print(event.eventType)
                    self._processEvent(event)
                    
                sleep(0.1)
                
        finally:
            #stop the controls
            self.shutdownButton.stop()
            self.stp.stop()
            self.onOffSwitch.stop()
            self.playlistSwitch.stop()
            self.volControl.stop()

            #stop mpd keep alive
            mpdKeepAlive.stop()

            #turn off led
            self.onLED.off()

    def _processEvent(self, event):
        #on
        if (event.eventType == Event.EventType.ON):    
            print("ON")
            self._on()
            
        #off
        elif (event.eventType == Event.EventType.OFF):
            print("OFF")
            self._off()

        #shutdown
        elif (event.eventType == Event.EventType.SHUTDOWN):
            print("SHUTDOWN")
            self._shutdown()
            
        #m selected
        elif (event.eventType == Event.EventType.PLAYLISTM):
            print("PLAYLISTM")
            self._switchPlaylist(PLAYLISTNAMEM)
            
        #l selected
        elif (event.eventType == Event.EventType.PLAYLISTL):
            print("PLAYLISTL")
            self._switchPlaylist(PLAYLISTNAMEL)

        #volume changes
        elif (event.eventType == Event.EventType.VOL):
            print("VOL - {}".format(event.value))
            self._setVolume(event.value)

        #pause
        elif (event.eventType == Event.EventType.PAUSE):
            print("PAUSE")
            self._pauseResumePlayback()

        #skip track
        elif (event.eventType == Event.EventType.SKIPTRACK):
            print("SKIPTRACK - {}".format(event.value))
            self._skipTrack(event.value)
            
    def _safeMPDExec(self, func, *arg): 
        success = False

        try:
            func(*arg)
            success = True

        except mpd.CommandError as e:
            print "Error({0})".format(e.args)

        except mpd.ConnectionError as e:
            print "MPD connection error"
            #try and reconnect
            if self._reconnectMPD():
                print "MPD reconnected"
                #rerun function
                self._safeMPDExec(func, *arg)

        except socket.error as e:
            print "socket error"
            #try and reconnect
            if self._reconnectMPD():
                print "MPD reconnected"
                #rerun function
                self._safeMPDExec(func, *arg)

        return success

    def _safeMPDStatus(self):
        status = None
        try:
            status = self.mpd.status()
        except mpd.ConnectionError as e:
            print "MPD connection error"
            #try and reconnect
            if self._reconnectMPD():
                print "MPD reconnected"
                #rerun function
                status = self._safeMPDStatus()

        except socket.error as e:
            print "socket error"
            #try and reconnect
            if self._reconnectMPD():
                print "MPD reconnected"
                #rerun function
                status = self._safeMPDStatus()

        return status
    
    def _reconnectMPD(self):
        #connect to MPD server
        success = False
        try:
            self.mpd.connect(MPDHOST, MPDPORT)
            success = True
        except:
            print "Failed to connect to mpd"
        return success
    
    def _on(self):
        #unmute amp
        self.amp.unmute()
        
        #if there is a playlist selected, resume playback
        if self.playlist != None:
            self._startPlayback()

    def _off(self):
        #if there is playlist selected - pause it
        if self.playlist != None:
            #stop playback
            self._stopPlayback()

        #mute amp
        self.amp.mute()

    def _startPlayback(self):
        #state = self.mpd.status()["state"]
        state = self._safeMPDStatus()["state"]
        if state == "pause":
            self._safeMPDExec(self.mpd.pause,0)
        elif state == "stop":
            self._safeMPDExec(self.mpd.play)

    def _stopPlayback(self):
        self._safeMPDExec(self.mpd.stop)
    
    def _pausePlayback(self):
        self._safeMPDExec(self.mpd.pause,1)

    def _pauseResumePlayback(self):
        state = self._safeMPDStatus()["state"]
        if state == "play":
            self._pausePlayback()
        elif state == "pause":
            self._startPlayback()

    def _loadPlaylist(self, playlistname):
        self._safeMPDExec(self.mpd.clear)
        if not self._safeMPDExec(self.mpd.load, playlistname):
            print "Failed to load playlist ({})".format(playlistname)
        self.playlist = playlistname
        #set repeat on
        self._safeMPDExec(self.mpd.repeat, 1)
        
    def _savePlaylist(self, playlistname):
        #remove the playlist
        self._safeMPDExec(self.mpd.rm, playlistname)
        self._safeMPDExec(self.mpd.save, playlistname)

    def _switchPlaylist(self, playlistname):
        #if a different playlist is playing save it
        if self.playlist != playlistname:
            #save the previous playlist
            self._savePlaylist(self.playlist)

            #load the playlist and start playback
            self._loadPlaylist(playlistname)
            self._startPlayback()

    def _setVolume(self, vol):
        self._safeMPDExec(self.mpd.setvol, vol)

    def _skipTrack(self, direction):
        if direction == 1:
            self._nextTrack()
        elif direction == -1:
            self._prevTrack()

    def _nextTrack(self):
        state = self._safeMPDStatus()["state"]
        if state == "play":
            self._safeMPDExec(self.mpd.next)

    def _prevTrack(self):
        state = self._safeMPDStatus()["state"]
        if state == "play":
            #if we are skipping back through tracks, goto the previous, otherwise restart the current track
            if self.prevTrackSkipActive:
                #goto the previous track
                self._safeMPDExec(self.mpd.previous)
            else:
                #restart the current track
                self._safeMPDExec(self.mpd.seekcur, 0)

            #start / restart the timer
            self._startPrevTrackSkip()

    def _startPrevTrackSkip(self):
        #print "track skip started"
        #if its active cancel it
        if self.prevTrackSkipActive:
            self.prevTrackSkipTimer.cancel()
            
        self.prevTrackSkipActive = True
        self.prevTrackSkipTimer = Timer(PREVTRACKTIMEOUT, self._cancelPrevTrackSkip)
        self.prevTrackSkipTimer.start()

    def _cancelPrevTrackSkip(self):
        #print "track skip cancelled"
        self.prevTrackSkipActive = False

    def _shutdown(self):
        #if there is playlist selected - pause it
        if self.playlist != None:
            #stop playback
            self._stopPlayback()
            #save the playlist
            self._savePlaylist(self.playlist)
        
        #mute amp
        self.amp.mute()

        #stop the program
        self.stopped = True
    
#main program
if __name__ == "__main__":

    #set GPIO mode
    GPIO.setmode(GPIO.BCM)

    #create radio control
    radioControl = RadioControl(MPDHOST, MPDPORT)
    
    try:
        #start the radio control
        radioControl.start()
    
    finally:
        #tidy up GPIO
        GPIO.cleanup()


"""
Requirements:

ON/OFF

If the power switch is ON the amp should be unmuted.
If the power switch is OFF the amp should be muted.

When the power switch is turned ON:
- Unmute the amp
- If a playlist is paused
 - unpaused the playback

When the power switch is turned OFF:
- If a playlist was playing
  - pause the playback
- Mute the amp

PLAYBACK

There should be 2 default playlists which are selected when M or L is selected:
- MartPlaylist
- LeePlaylist
* if the playlist doesn't exist create one from a backup


When M/L is selected:
- If the M/L is paused:
  - unpause the playback
- If the M/L has changed:
  - if its playing stop the playback
  - save the queue to the playlist
  - persist in memory the track which was playing
- load the playlist
- set the playlist to repeat
- if there is track in memory set it to play that one

When the top is closed the music should pause.

"""
