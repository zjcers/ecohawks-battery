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
#Taken from https://github.com/scottjw/subfact_pi_ina219/Subfact_ina219.py
# ===========================================================================
#    CONFIG REGISTER (R/W)
# ===========================================================================
	__INA219_REG_CONFIG                      = 0x00
# ===========================================================================
	__INA219_CONFIG_RESET                    = 0x8000  # Reset Bit
	__INA219_CONFIG_BVOLTAGERANGE_MASK       = 0x2000  # Bus Voltage Range Mask
	__INA219_CONFIG_BVOLTAGERANGE_16V        = 0x0000  # 0-16V Range
	__INA219_CONFIG_BVOLTAGERANGE_32V        = 0x2000  # 0-32V Range

	__INA219_CONFIG_GAIN_MASK                = 0x1800  # Gain Mask
	__INA219_CONFIG_GAIN_1_40MV              = 0x0000  # Gain 1, 40mV Range
	__INA219_CONFIG_GAIN_2_80MV              = 0x0800  # Gain 2, 80mV Range
	__INA219_CONFIG_GAIN_4_160MV             = 0x1000  # Gain 4, 160mV Range
	__INA219_CONFIG_GAIN_8_320MV             = 0x1800  # Gain 8, 320mV Range

	__INA219_CONFIG_BADCRES_MASK             = 0x0780  # Bus ADC Resolution Mask
	__INA219_CONFIG_BADCRES_9BIT             = 0x0080  # 9-bit bus res = 0..511
	__INA219_CONFIG_BADCRES_10BIT            = 0x0100  # 10-bit bus res = 0..1023
	__INA219_CONFIG_BADCRES_11BIT            = 0x0200  # 11-bit bus res = 0..2047
	__INA219_CONFIG_BADCRES_12BIT            = 0x0400  # 12-bit bus res = 0..4097

	__INA219_CONFIG_SADCRES_MASK             = 0x0078  # Shunt ADC Resolution and Averaging Mask
	__INA219_CONFIG_SADCRES_9BIT_1S_84US     = 0x0000  # 1 x 9-bit shunt sample
	__INA219_CONFIG_SADCRES_10BIT_1S_148US   = 0x0008  # 1 x 10-bit shunt sample
	__INA219_CONFIG_SADCRES_11BIT_1S_276US   = 0x0010  # 1 x 11-bit shunt sample
	__INA219_CONFIG_SADCRES_12BIT_1S_532US   = 0x0018  # 1 x 12-bit shunt sample
	__INA219_CONFIG_SADCRES_12BIT_2S_1060US  = 0x0048  # 2 x 12-bit shunt samples averaged together
	__INA219_CONFIG_SADCRES_12BIT_4S_2130US  = 0x0050  # 4 x 12-bit shunt samples averaged together
	__INA219_CONFIG_SADCRES_12BIT_8S_4260US  = 0x0058  # 8 x 12-bit shunt samples averaged together
	__INA219_CONFIG_SADCRES_12BIT_16S_8510US = 0x0060  # 16 x 12-bit shunt samples averaged together
	__INA219_CONFIG_SADCRES_12BIT_32S_17MS   = 0x0068  # 32 x 12-bit shunt samples averaged together
	__INA219_CONFIG_SADCRES_12BIT_64S_34MS   = 0x0070  # 64 x 12-bit shunt samples averaged together
	__INA219_CONFIG_SADCRES_12BIT_128S_69MS  = 0x0078  # 128 x 12-bit shunt samples averaged together

	__INA219_CONFIG_MODE_MASK                = 0x0007  # Operating Mode Mask
	__INA219_CONFIG_MODE_POWERDOWN           = 0x0000
	__INA219_CONFIG_MODE_SVOLT_TRIGGERED     = 0x0001
	__INA219_CONFIG_MODE_BVOLT_TRIGGERED     = 0x0002
	__INA219_CONFIG_MODE_SANDBVOLT_TRIGGERED = 0x0003
	__INA219_CONFIG_MODE_ADCOFF              = 0x0004
	__INA219_CONFIG_MODE_SVOLT_CONTINUOUS    = 0x0005
	__INA219_CONFIG_MODE_BVOLT_CONTINUOUS    = 0x0006
	__INA219_CONFIG_MODE_SANDBVOLT_CONTINUOUS = 0x0007
# ===========================================================================

# ===========================================================================
#   SHUNT VOLTAGE REGISTER (R)
# ===========================================================================
	__INA219_REG_SHUNTVOLTAGE                = 0x01
# ===========================================================================

# ===========================================================================
#   BUS VOLTAGE REGISTER (R)
# ===========================================================================
	__INA219_REG_BUSVOLTAGE                  = 0x02
# ===========================================================================

# ===========================================================================
#   POWER REGISTER (R)
# ===========================================================================
	__INA219_REG_POWER                       = 0x03
# ===========================================================================

# ==========================================================================
#    CURRENT REGISTER (R)
# ===========================================================================
	__INA219_REG_CURRENT                     = 0x04
# ===========================================================================

# ===========================================================================
#    CALIBRATION REGISTER (R/W)
# ===========================================================================
	__INA219_REG_CALIBRATION                 = 0x05
# ===========================================================================
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
