import time
import logentry
from abc import ABCMeta, abstractmethod
class Logger(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def __init__(self):
        """Opens the logging file/database/etc."""
        pass
    def makeEntry(self, currentInReading, currentOutReading, voltageReading, luxReading, relayStatus):
        ret = logentry.Entry()
        ret["time"] = time.time()
        ret["currentInReading"] = currentInReading
        ret["currentOutReading"] = currentOutReading
        ret["voltageReading"] = voltageReading
        ret["luxReading"] = luxReading
        ret["relayStatus"] = relayStatus
        return ret
    def recordEntry(self, entry):
        """Records a log entry to the logging backend"""
        pass
