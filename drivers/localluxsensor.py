#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 7 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 23 2016
import time
import smbus
#import sensor abstract
import abstractsensor
class LuxSensor(abstractsensor.Sensor):
	def __init__(self,bus=1,addr="0x39",**kwargs):
		self.logger = logging.getLogger("PB.drivers.luxsensor.local")
		self.logger.info("Starting with parameters bus=%i, addr=%x",bus,addr)
		self.addr = addr
		self.bus = smbus.SMBus(bus)
	#this method may hang for a while as the sensor gets recallibrated, run in a thread
	def getReading(self):
		while True:
			lowADC,highADC = self.readADC()
			gain,integ = self.getTiming()
			if lowADC == 65535 or highADC == 65535:
				self.logger.debug("Overexposed, reducing integration time")
				if gain:
					self.setTiming(False, integ)
				elif integ > 0:
					self.setTiming(False, integ-1)
				time.sleep(0.4)
			elif lowADC < 5 or highADC < 5:
				self.logger.debug("Underexposed, increasing integration time")
				if not gain:
					self.setTiming(True, integ)
				elif integ < 2:
					self.setTiming(True, integ+1)
				time.sleep(0.4)
			else:
				break
		gain,integ = self.getTiming()
		if highADC/lowADC <= 0.5:
			lux = (0.0304*lowADC)-(0.062*lowADC*(highADC/lowADC)**1.4)
		elif highADC/lowADC <= 0.61:
			lux = (0.0224*lowADC)-(0.031*highADC)
		elif highADC/lowADC <= 0.8:
			lux = (0.0128*lowADC)-(0.0153*highADC)
		elif highADC/lowADC <= 1.30:
			lux = (0.00146*lowADC)-(0.00112*highADC)
		elif highADC/lowADC > 1.30:
			lux = 0.0
		return lux
	def setReg(self, reg):
		assert reg >= 0
		assert reg < 16
		self.bus.write_byte(self.addr, 0b10010000 | reg) #see page 14 of DS for command reg documentation
	def enable(self):
		self.setReg(0x00)
		self.bus.write_byte(self.addr, 0b00000011)
		self.logger.debug("ctrl reg %s",bin(self.bus.read_byte(self.addr)))
	def disable(self):
		self.setReg(0x00)
		self.bus.write_byte(self.addr, 0b00000000)
		self.logger.debug("ctrl reg %s",bin(self.bus.read_byte(self.addr)))
	def setTiming(self, gain, integ):
		assert type(gain) == bool
		assert type(integ) == int
		assert integ >= 0 && integ <= 3
		gain = 0b00010000 if gain else 0b00000000
		self.setReg(0x01)
		self.bus.write_byte(self.addr, gain | integ)
	def getTiming(self):
		self.setReg(0x01)
		timeReg = self.bus.read_byte(self.addr)
		gain = (timeReg & 0b10000) != 0
		integ = (timeReg &0b11)
		return gain, integ
	def readADC(self):
		ch0 = i2cutil.reverse_word(self.bus.read_word(self.addr, 0xAC)) #As per DS pg 19
		ch1 = i2cutil.reverse_word(self.bus.read_word(self.addr, 0xAE))
		self.logger.debug("CH0 ADC Value: %i CH1 ADC Value: %i",ch0,ch1)
		return ch0, ch1
if __name__ == "__main__":
	l = LocalLuxSensor()
	print "Current Lux: ",l.getReading()
