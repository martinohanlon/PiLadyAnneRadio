#Radio Control - Average Volume Readings
#Martin O'Hanlon
#www.stuffaboutcode.com

#This program outputs average values which should be used to create a
# dictionary for use in the volumecontrol.py module

from MCP3008 import MCP3008
from time import sleep

#SPI constants
SPIBUS = 0
SPIDEVICE = 0
SPICHANNEL = 0

STEPS = 11

AVGLENGTH = 20

def getAverage():
    print "Getting average"
    values = []
    with MCP3008(channel = SPICHANNEL) as volumeDial:
        for count in range(AVGLENGTH):
            data = volumeDial.read()
            print data
            values.append(data)
            sleep(0.1)
    return sum(values) / len(values)

values = ""

#loop through the steps and get averages
for step in range(STEPS):
    print "move to step {} of {}".format(step + 1, STEPS)
    raw_input("enter to continue")

    dataAvg = getAverage()
    
    print "Step {} average = {}".format(step + 1, dataAvg)
    values += "{} : {}\n".format(step + 1, dataAvg)

print values
