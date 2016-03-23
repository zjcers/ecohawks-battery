#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 23 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 23 2016
from abc import abstractmethod, ABCMeta
class Relay(object):
	__metaclass__ = ABCMeta
	@abstractmethod
	def __init__(self):
		pass
	@abstractmethod
	def enable(self, num):
		pass
    def disable(self, num):
        pass
