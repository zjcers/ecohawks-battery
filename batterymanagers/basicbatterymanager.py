#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 10 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 23 2016
import threading
import logging
import cfg
import sensorthread
#drivers (aliased by imports)
import currentInSensor
import currentOutSensor
import voltageSensor
import luxSensor
import relay
#starts threads for: currentInSensor, currentOutSensor, voltageSensor, LuxSensor
class BatteryManager():
	def __init__(self):
		self.logger = logging.getLogger("PB.batterymanager.basic")
		self.logger.info("Initializing...")
		self.shutdownEvent = threading.Event()
		self.currentInS = currentInSensor.CurrentSensor(bus=cfg.cfg["currentInBus"], addr=cfg.cfg["currentInAddr"], shuntCurrent=cfg.cfg["currentInShunt"])
		self.currentInThread = sensorthread.SensorThread(self.currentInS, self.shutdownEvent)
		self.currentOutS = currentOutSensor.CurrentSensor(bus=cfg.cfg["currentOutBus"], addr=cfg.cfg["currentOutAddr"], shuntCurrent=cfg.cfg["currentOutShunt"])
		self.currentOutThread = sensorthread.SensorThread(self.currentOutS, self.shutdownEvent)
		self.voltageS = voltageSensor.VoltageSensor(bus=cfg.cfg["voltageBus"], addr=cfg.cfg["voltageAddr"])
		self.voltageThread = sensorthread.SensorThread(self.voltageS, self.shutdownEvent)
		self.luxS = luxSensor.LuxSensor(bus=cfg.cfg["luxSensorBus"], addr=cfg.cfg["luxSensorAddr"])
		self.luxThread = sensorthread.SensorThread(self.luxS, self.shutdownEvent)
		self.relay = relay.Relay(port=cfg.cfg["relayPort"])
	def getReadings(self):
		return self.currentInThread.getReading(), self.currentOutThread.getReading(), self.voltageThread.getReading(), self.luxThread.getReading()
	def startThreads(self):
		self.logger.info("Starting threads")
		self.currentInThread.start()
		self.currentOutThread.start()
		self.voltageThread.start()
		self.luxThread.start()
	def shutdown(self):
		self.logger.info("Shutting down threads")
		self.shutdownEvent.set()
		self.logger.debug("Waiting for currentInThread")
		self.currentInThread.join()
		self.logger.debug("Waiting for currentOutThread")
		self.currentOutThread.join()
		self.logger.debug("Waiting for luxThread")
		self.luxThread.join()
		self.logger.debug("Waiting for voltageThread")
		self.voltageThread.join()
