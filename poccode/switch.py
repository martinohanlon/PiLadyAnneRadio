import RPi.GPIO as GPIO
from time import sleep

PIN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    count = 0
    while True:
        print(str(count) + ":" + str(GPIO.input(PIN)))
        sleep(0.01)
        count += 1
    
finally:
    GPIO.cleanup()
