#MCP3008 Python Class
#Martin O'Hanlon
#stuffaboutcode.com
from spidev import SpiDev

class MCP3008:
    def __init__(self, bus = 0, device = 0, channel = 0):
        self.bus, self.device, self.channel = bus, device, channel
        self.spi = SpiDev()

    def __enter__(self):
        self.open()
        return self

    def open(self):
        self.spi.open(self.bus, self.device)
    
    def read(self):
        adc = self.spi.xfer2([1, (8 + self.channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def __exit__(self, type, value, traceback):
            self.close()
            
    def close(self):
        self.spi.close()

#test
if __name__ == "__main__":    
    with MCP3008(channel = 0) as ch0:
        print ch0.read()
