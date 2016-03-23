#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 8 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 23 2016
import random
import sys
import logging
#import sensor abstract
import abssensor
class LuxSensor(abssensor.Sensor):
	def __init__(self, bus=1, addr=0x39 normValue=20000, delta=2000,**kwargs):
		self.logger = logging.getLogger("PB.drivers.luxsensor.dummy")
		self.normValue = normValue
		self.delta = delta
	 	self.logger.info("Starting with parameters bus=%i, addr=%x normValue=%i delta=%i",bus,addr,normValue,delta)
	def getReading(self):
		return max(self.normValue+self.getSign()*random.random()*self.delta, 0)
	def getSign(self):
		if random.random() < 0.5:
			return -1
		else:
			return 1
if __name__ == "__main__":
	if len(sys.argv) == 1:
		l = LuxSensor()
	elif len(sys.argv) == 2:
		l = LuxSensor(normValue=int(sys.argv[1]))
	elif len(sys.argv) == 3:
		l = LuxSensor(normValue=int(sys.argv[1]), delta=int(sys.argv[2]))
	else:
		print "Usage: ",sys.argv[0]," [normValue] [delta]"
		exit(1)
	print "Lux: ",l.getReading()
