import RPi.GPIO as GPIO
from time import sleep

ONPIN = 5

def mycallback(channel):
    if GPIO.input(ONPIN) == 1:
        print("rising")
    else:
        print("falling")

GPIO.setmode(GPIO.BCM)

GPIO.setup(ONPIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(ONPIN, GPIO.BOTH, callback=mycallback, bouncetime=200)

while(True):
    sleep(1)
