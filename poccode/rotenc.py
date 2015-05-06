import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN)
GPIO.setup(6, GPIO.IN)

try:
    count = 0
    while True:
        print(str(count) + ":" + str(GPIO.input(5)) + " " + str(GPIO.input(6)))
        
        sleep(0.01)
        count += 1
    
finally:
    GPIO.cleanup()
