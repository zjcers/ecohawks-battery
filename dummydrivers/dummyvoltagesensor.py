#!/usr/bin/python
#Title: Dummy voltage sensor driver
#Original Author: Zane J Cersovsky
#Original Date: Mar 8 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 23 2016
import sys
import random
import logging
#import sensor abstract
import abstractsensor
class VoltageSensor(abstractsensor.Sensor):
	def __init__(self, bus=1, addr=0x40):
		self.logger = logging.getLogger("PB.drivers.voltagesensor.dummy")
		self.addr = addr
		self.bus = bus
		self.logger.info("Starting with parameters: bus=%i, addr=%x",self.bus,self.addr)
	#returns the current across the shunt
	def getReading(self):
		return 5.0-(random.random()*0.5)
if __name__ == "__main__":
	if len(sys.argv) == 1:
		v= VoltageSensor()
	elif len(sys.argv) == 2:
		v = VoltageSensor(addr=sys.argv[1])
	elif len(sys.argv) == 3:
		v = VoltageSensor(bus=sys.argv[1], addr=sys.argv[2])
	else:
		print "Invalid arguments"
		exit(1)
	print "Voltage: ",v.getReading()
