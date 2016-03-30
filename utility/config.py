#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 8 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 10 2016
import sys
import os
import string
import logging
import pb_exceptions
class config(dict):
	def __init__(self, fileName):
		self.logger = logging.getLogger("PB.config")
		self.fileName = fileName
		self.loadConfig()
	def loadConfig(self):
		self.logger.info("Loading configuration file: %s", self.fileName)
		f = open(self.fileName,'r')
		try:
			for line in f:
				line = line.strip('\n')
				if not (line.startswith('#') or line == ''):
					[key, value] = line.split('=')
					self.logger.debug("Detecting %s as: %s", value, repr(self.detectType(value)(value)))
					value = self.detectType(value)(value)
					self[key] = value
		except:
			raise pb_exceptions.ConfigFileException("Error parsing config file")
	def detectType(self, value):
		if value.startswith("0x"):
			return self.dehex
		elif value[:1] in "0123456789":
			if "." in value:
				return float
			else:
				return int
		elif value.upper() == "TRUE" or value.upper() == "FALSE":
			return self.debool
		elif ',' in value:
			return self.delist
		else:
			return str
	def dehex(self, value):
		return int(value, 16)
	def delist(self, value):
		return value.split(',')
	def debool(self, value):
		return value.upper() == "TRUE"
if __name__ == "__main__":
	if len(sys.argv) == 2:
		print "Loading configuration file: ",sys.argv[1]
		cfg = config(sys.argv[1])
		print repr(cfg)
	else:
		print "Invalid number of arguments"
