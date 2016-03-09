#!/usr/bin/python
#Title: Dummy voltage sensor driver
#Original Author: Zane J Cersovsky
#Original Date: Mar 8 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 78 2016
import sys
import random
import sensor
class VoltageSensor(sensor.Sensor):
	def __init__(self, bus=1, addr=0x40):
		self.addr = addr
		self.bus = bus
		print "Dummy voltage sensor starting with parameters: bus=",bus,", addr=",hex(addr)
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
