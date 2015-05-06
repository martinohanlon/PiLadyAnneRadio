import RPi.GPIO as GPIO
from time import sleep

PIN1 = 5
PIN2 = 6

global count

def mycallback(pin):
    global count
    print(str(count) + ":" + str(GPIO.input(PIN1)) + " " + str(GPIO.input(PIN2)))
    
    count += 1

count = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PIN2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(PIN1, GPIO.BOTH, callback=mycallback)
GPIO.add_event_detect(PIN2, GPIO.BOTH, callback=mycallback)

try:
    while True:
        sleep(0.25)
        
finally:
    GPIO.cleanup()
