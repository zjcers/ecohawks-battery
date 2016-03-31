#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 8 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 8 2016
import threading
import time
import cfg
import circularlist
class SensorThread(threading.Thread):
	def __init__(self, sensorObj, shutdownEvent):
		threading.Thread.__init__(self)
		self.reading = (None, time.time())
		self.useAvg = False
		if "sensorAvg" in cfg.cfg:
			self.buf = circularlist.CircularList(cfg.cfg["sensorAvg"])
			self.useAvg = True
		self.sensor = sensorObj
		self.shutdownEvent = shutdownEvent
	def run(self):
		while not self.shutdownEvent.is_set():
			if (time.time()-self.reading[1]) > 0.5:
				self.reading = (self.sensor.getReading(), time.time())
				self.buf.addElement(self.reading[0])
			else:
				time.sleep(0.1)
	def getReading(self):
		if self.useAvg:
			return self.buf.average()
		else:
			return self.reading[0]
