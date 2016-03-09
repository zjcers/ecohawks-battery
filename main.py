#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 8 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 8 2016
TESTING=True
LOCAL_LUX = True
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
import threading
import sys
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
	if len(sys.argv) == 2:
		cfg = config.config(sys.argv[1])
	else:
		cfg = config.config()
	bm = BatteryManager(cfg)
	bm.startThreads()
