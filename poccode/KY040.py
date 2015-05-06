import RPi.GPIO as GPIO
from time import sleep

CLOCKPIN = 5
DATAPIN = 6
SWITCHPIN = 13

def clockCallback(pin):
    data = GPIO.input(DATAPIN)
    if data == 1:
        print "anti-clockwise"
    else:
        print "clockwise"

def switchCallback(pin):
    if GPIO.input(SWITCHPIN) == 0:
        print "switch pressed"
    
GPIO.setmode(GPIO.BCM)

#pin setup for KY040 module with pull ups
GPIO.setup(CLOCKPIN, GPIO.IN)
GPIO.setup(DATAPIN, GPIO.IN)
GPIO.setup(SWITCHPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(CLOCKPIN, GPIO.FALLING, callback=clockCallback, bouncetime=250)
GPIO.add_event_detect(SWITCHPIN, GPIO.FALLING, callback=switchCallback, bouncetime=300)

try:
    while True:    
        sleep(0.1)
finally:
    GPIO.cleanup()

    
