#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 8 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 8 2016
class config(dict):
	def __init__(self, fileName):
		self.fileName = fileName
		try:
			f = open(self.fileName,'r')
		except:
			self.fileName = "default.conf"
			f = open(self.fileName, 'r') # can throw, but it needs to
		for line in f:
			if not line.startswith('#'):
				[key, value] = line.split('=')
				self[key] = value
	def __init__(self):
		self.fileName = "default.conf"
		f = open(self.fileName, 'r') # can throw, but it needs to
		for line in f:
			if not line.startswith('#'):
				[key, value] = line.split('=')
				self[key] = value
