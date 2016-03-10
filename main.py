#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 8 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 8 2016

#import python standard modules
import sys
import threading
import os
#set variables
try:
	TESTING = bool(os.environ["PB_TESTING"])
except:
	TESTING = False
try:
	LOCAL_LUX = bool(os.environ["PB_LOCAL_LUX"])
except:
	LOCAL_LUX = False
try:
	CONFIG_FILE = bool(os.environ["PB_CONFIG_FILE"])
except:
	CONFIG_FILE = "default.conf"
#import custom modules
if TESTING:
	import dummyluxsensor as luxsensor
	import dummyvoltagesensor as voltagesensor
	import dummycurrentsensor as currentsensor
	import dummyrelay as relay
else:
	if LOCAL_LUX:
		import localluxsensor as luxsensor
	else:
		import luxsensor
	import voltagesensor
	import currentsensor
	import relay
import sensorthread
import config
class BatteryManager():
	def __init__(self, config):
		self.shutdownEvent = threading.Event()
		self.currentInS = currentsensor.CurrentSensor(bus=config["bus"], addr=config["currentInAddr"])
		self.currentInThread = sensorthread.SensorThread(self.currentInS, self.shutdownEvent)
		self.currentOutS = currentsensor.CurrentSensor(bus=config["bus"], addr=config["currentOutAddr"])
		self.currentOutThread = sensorthread.SensorThread(self.currentOutS, self.shutdownEvent)
		self.voltageS = voltagesensor.VoltageSensor(bus=config["bus"], addr=config["voltageAddr"])
		self.voltageThread = sensorthread.SensorThread(self.voltageS, self.shutdownEvent)
		self.luxS = luxsensor.LuxSensor(bus=config["bus"], addr=config["luxAddr"])
		self.luxThread = sensorthread.SensorThread(self.luxS, self.shutdownEvent)
		self.relay = relay.USBRelay(port=config["port"])
	def startThreads(self):
		self.currentInThread.start()
		self.currentOutThread.start()
		self.luxThread.start()
	def returnReadings(self):
		return self.currentInThread.reading, self.currentOutThread.reading, self.voltageThread.reading
if __name__ == "__main__":
	try:
		cfg = config.config(CONFIG_FILE)
	except:
		cfg = config.config()
	bm = BatteryManager(cfg)
	bm.startThreads()
