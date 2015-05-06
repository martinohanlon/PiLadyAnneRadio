import spidev
from time import sleep

CHANNEL = 0

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

try:
    while True:
        sleep(0.25)
        print ReadChannel(CHANNEL)
finally:
    spi.close()
