#!/usr/bin/python
#Title: Dummy current sensor driver
#Original Author: Zane J Cersovsky
#Original Date: Mar 8 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 23 2016
import sys
import random
import logging
#import sensor abstract
import abstractsensor
class CurrentSensor(abstractsensor.Sensor):
	def __init__(self, bus=1, addr=0x40, shunt=0.1):
		self.logger = logging.getLogger("PB.drivers.currentsensor.dummy")
		self.addr = addr
		self.bus = bus
		self.shunt = shunt
		self.logger.info("Starting with parameters: bus=%i, addr=%x, shunt=%f",self.bus,self.addr,self.shunt)
	#returns the current across the shunt
	def getReading(self):
		return 5.0-(random.random()*0.5)
if __name__ == "__main__":
	if len(sys.argv) == 1:
		c = CurrentSensor()
	elif len(sys.argv) == 2:
		c = CurrentSensor(addr=sys.argv[1])
	elif len(sys.argv) == 3:
		c = CurrentSensor(bus=sys.argv[1], addr=sys.argv[2])
	else:
		print "Invalid arguments"
		exit(1)
	print "Current: ",c.getReading()
