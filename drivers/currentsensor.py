#!/usr/bin/python
#Title: INA219 shunt-voltage current sensor driver
#Original Author: Zane J Cersovsky
#Original Date: Mar 7 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 23 2016
import sys
import smbus
import logging
import i2cutil
#import sensor abstract
import abstractsensor
class CurrentSensor(abstractsensor.Sensor):
	def __init__(self, bus=1, addr=0x40, shuntCurrent=2.0):
		self.logger = logging.getLogger("PB.drivers.currentsensor.local")
		self.logger.info("Starting with parameters bus=%i, addr=%x, shunt=%f",bus,addr,shuntCurrent)
		self.addr = addr
		self.bus = smbus.SMBus(bus)
		self.shuntCurrent = shuntCurrent
		self.shuntVdrop = 50.0 #50mv shunts (will make this not a constant in later versions)
	#returns the current across the shunt
	def getReading(self):
		shuntvoltage = self.getShuntVoltage()
		return (shuntvoltage/self.shuntVdrop)*self.shuntCurrent
	#gets shunt voltage reading in millivolts
	def getShuntVoltage(self):
		reading = i2cutil.reverse_word(self.bus.read_word_data(self.addr, 0x01)) #read and reverse bytes
		reading = i2cutil.twocomplement(reading)
		print "Got shunt reading of: ",reading
		return reading*0.01
	#gets the current shunt voltage divider (not used since I don't want to make more bugs)
	def getPGA(self):
		configreg = i2cutil.reverse_word(self.bus.read_word_data(self.addr, 0x00)) #read config register (see datasheet pg 18)
		configreg = (configreg >> 11) & 3 #extract bits 12 and 11 from from the config register (see datasheet pg 19)
		return 2**configreg #the divider is 2^pgabits (datasheet pg 19)
if __name__ == "__main__":
	if len(sys.argv) == 1:
		c = CurrentSensor()
	elif len(sys.argv) == 2:
		c = CurrentSensor(addr=int(sys.argv[1], 16))
	elif len(sys.argv) == 3:
		c = CurrentSensor(bus=int(sys.argv[1]), addr=int(sys.argv[2],16))
	elif len(sys.argv) == 4:
		c = CurrentSensor(bus=int(sys.argv[1]), addr=int(sys.argv[2],16), shuntCurrent=float(sys.argv[3]))
	else:
		print "Invalid arguments"
		exit(1)
	print "Current: ",c.getReading()
