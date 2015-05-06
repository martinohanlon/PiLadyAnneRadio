import spidev
from time import sleep
from collections import deque

CHANNEL = 0
AVGLENGTH = 20

spi = spidev.SpiDev()
spi.open(0,0)
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
    #print channel
    adc = spi.xfer2([1,(8+channel)<<4,0])
    print adc
    data = ((adc[1]&3) << 8) + adc[2]
    #print data
    return data

values = deque()

try:
    while True:
        sleep(0.1)
        newValue = ReadChannel(CHANNEL)
        values.append(newValue)
        if len(values) > AVGLENGTH:
            values.popleft()
        avgValue = sum(values) / len(values)
        
        print "new = {}: avg = {}".format(newValue, avgValue)
finally:
    spi.close()
