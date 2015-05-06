import mpd
from time import sleep

MPD_HOST = "localhost"
MPD_PORT = "6600"
MPD_PASSWORD = "volumio" # password for Volumio / MPD

LEEPLAYLISTNAME = "Testplaylist"
MARTPLAYLISTNAME = "Testplaylist2"

def safeMPDExecute(func, *arg): 
    success = False
    try:
        func(*arg)
        success = True
    except mpd.CommandError as e:
        print "Error({0})".format(e.args)
    return success
        

# Connect with MPD
client = mpd.MPDClient()
connected = False
client.connect(MPD_HOST, MPD_PORT)
print("Connected")
print(client.status())
print(client.status()["state"])

def _startPlayback():
    state = client.status()["state"]
    print state
    if state == "pause":
        client.pause(0)
    elif state == "stop":
        #print "play"
        client.play()

def _pausePlayback():
    client.pause(1)

def _nextTrack():
    state = client.status()["state"]
    if state == "play":
        client.next()
        
def _prevTrack():
    state = client.status()["state"]
    if state == "play":
        client.previous()

try:
    _prevTrack()
    print(client.mpd_version)


    #_startPlayback()

    #_pausePlayback()
    
    #client.play()
    #resume
    #client.pause(0)
    #pause
    #client.pause(1)
    #client.stop()
    #client.repeat(1)
    
    #print(client.status())
    #print(client.playlist())
    #print(client.playlistinfo())
    #print(client.listplaylists())
    #save a current q to a playlist, by removing it first
    #safeMPDExecute(client.rm, LEEPLAYLISTNAME)
    #client.rm("dasd")
    #client.save(LEEPLAYLISTNAME)
    #client.setvol(10)
    #client.volume(-1)
    #client.clear()
    #try:
    #    client.load(LEEPLAYLISTNAME)
    #except mpd.CommandError:
    #    #load error no such playlist
    #    print "command error"
    
                    
finally:
    client.close()
    client.disconnect()

