import time
import logentry
from abc import ABCMeta, abstractmethod
class Logger(object):
	__metaclass__ = ABCMeta
	@abstractmethod
	def __init__(self):
		r"""Opens the logging file/database/etc."""
		pass
	@abstractmethod
	def recordEntry(self, entry):
		r"""Records a log entry to the logging backend"""
		pass
