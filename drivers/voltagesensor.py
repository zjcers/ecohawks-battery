#!/usr/bin/python
#Original Author: Zane J Cersovsky
#Original Date: Mar 6 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 7 2016
import smbus
import sys
import sensor
import i2cutil
class VoltageSensor(sensor.Sensor):
	def __init__(self, bus=1, addr=0x40):
		self.addr = addr
		self.bus = smbus.SMBus(bus)
	def getReading(self):
		return (i2cutil.reverse_word(self.bus.read_word_data(self.addr, 0x02))/66536.0)*32
if __name__ == "__main__":
	if len(sys.argv) == 1:
		v = VoltageSensor()
	elif len(sys.argv) == 2:
		v = VoltageSensor(addr=sys.argv[1])
	elif len(sys.argv) == 3:
		v = VoltageSensor(bus=sys.argv[1], addr=sys.argv[2])
	else:
		print "Invalid arguments"
		exit(1)
	print "Current Voltage: ",v.getReading()
