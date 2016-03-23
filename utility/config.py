#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 8 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 10 2016
import sys
import os
import pb_exceptions
class config(dict):
	def __init__(self, fileName):
		self.fileName = fileName
		if "PB_CONFIG_KEYS" in os.environ:
			self.loadRequiredKeys(os.environ["PB_CONFIG_KEYS"])
		else:
			self.loadRequiredKeys("conf/keys")
		self.loadConfig()
	def loadRequiredKeys(self, fileName):
		f = open(fileName, 'r')
		self.requiredKeys = {}
		try:
			for line in f:
				if not (line.startswith('#') or len(line) <= 1):
					line = line.rstrip('\n')
					[key, value] = line.split('=')
					self.requiredKeys[key] = self.resolveTypes(value)
		except:
			raise pb_exceptions.ConfigFileException("Error parsing keys file")
	def loadConfig(self):
		f = open(self.fileName,'r')
		try:
			for line in f:
				line = line.strip('\n')
				if not (line.startswith('#') or line == ''):
					[key, value] = line.split('=')
					if key in self.requiredKeys.keys():
						value = self.requiredKeys[key](value)
						self[key] = value
		except:
			raise pb_exceptions.ConfigFileException("Error parsing config file")
	def resolveTypes(self, typeStr):
		try:
			return {
			"str": str,
			"int": int,
			"bool": bool,
			"float": float,
			"hex": self.dehex
			}[typeStr]
		except:
			return str
	def dehex(self, num):
		return int(num, 16)
	def delist(self, inputString):
		return inputString.split(',')
if __name__ == "__main__":
	if len(sys.argv) == 2:
		print "Loading configuration file: ",sys.argv[1]
		cfg = config(sys.argv[1])
		print repr(cfg)
	else:
		print "Invalid number of arguments"
