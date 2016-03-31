#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 23 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 23 2016
#import needed STL modules
import sys
import logging
#import pySerial
import serial
#import abstract relay
import abstractrelay
class Relay(abstractrelay.Relay):
	def __init__(self, port="/dev/ttyUSB0"):
		self.logger = logging.getLogger("PB.drivers.relay.usbrelay")
		self.logger.info("starting on port: "+port)
		self.s = serial.Serial(port="/dev/ttyUSB0")
		self.status = [False, False, False, False]
	def sendCmd(self, relay, status):
		assert type(relay) == int
		assert relay >= 1
		assert relay <= 4
		assert type(status) == bool
		self.status[relay-1] = status
		s.write(bytearray((255,relay,int(status))))
		s.flush()
	def enable(self, relay):
        if not self.status[num-1]:
            self.logger.info("Enabling relay #%i",num)
            self.status[num-1] = True
			self.sendCmd(relay, True)
	def disable(self, relay):
        if self.status[num-1]:
            self.logger.info("Disabling relay #%i",num)
            self.status[num-1] = False
			self.sendCmd(relay, False)
if __name__ == "__main__":
	relay = Relay()
	if len(sys.argv) == 3:
		num = int(sys.argv[1])
		state = ('n' in sys.argv[2].lower())
		relay.sendCmd(num,state)
	elif len(sys.argv) == 2:
		state = ('n' in sys.argv[1].lower())
		for i in xrange(1,5):
			relay.sendCmd(i,state)
	else:
		print "Usage: ",sys.argv[0]," <relay number> <on/off>"
		print "       ",sys.argv[0]," <on/off>"
