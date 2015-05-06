import RPi.GPIO as GPIO
import threading
from time import sleep

class GPIOEdgeDetection(threading.Thread):

	def __init__(self, channel, edgeType, callback, bounceTime = 0, refreshTime = 10):
		self.channel = channel
		self.edgeType = edgeType
		self.callback = callback
		self.bounceTime = bounceTime
		self.refreshTime = refreshTime
		self.running = False
		self.stopped = True

	def start(self):
		self.running = True
		self.stopped = False
		#get value of gpio
		lastValue = GPIO.input(self.channel)
		while(not self.stopped):
			newValue = GPIO.input(self.channel)
			if newValue != lastValue:
                                print "newValue = {} lastValue = {}".format(newValue, lastValue)
			
				if self.edgeType == GPIO.BOTH:
					self._raiseCallback()
				elif newValue < lastValue and self.edgeType == GPIO.FALLING:
					self._raiseCallback()
				elif newValue > lastValue and self.edgeType == GPIO.RISING:
					self._raiseCallback()
				if self.bounceTime > 0: sleep(self.bounceTime / 1000)
			lastValue = newValue
			sleep(self.refreshTime / 1000)
		

	def stop(self):
		self.stopped = True
		while(running):
			sleep(0.01)


	def _raiseCallback(self):
		self.callback(self.channel)
