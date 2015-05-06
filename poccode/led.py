import RPi.GPIO as GPIO
from time import sleep

PIN = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)

try:

    while True:
        GPIO.output(PIN, True)
        sleep(0.5)
        GPIO.output(PIN, False)
        sleep(0.5)
    
finally:
    GPIO.cleanup()
