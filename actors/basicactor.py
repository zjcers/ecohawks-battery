#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 24 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 24 2016
import time
import logging
import cfg
import sensorlogger
import batteryManager
import circularlist
import logentry
#import actor abstract
import absactor
class Actor(absactor.Actor):
	def __init__(self):
		self.logger = logging.getLogger("PB.actor.basic")
		self.logger.info("Starting up")
		self.checkConfig()
		self.batteryManagerObj = batteryManager.BatteryManager()
		self.batteryManagerObj.startThreads()
		self.sensorLogger = sensorlogger.Logger()
		self.batteryCur = 0.0
		self.currentBuf = circularlist.CircularList(3)
		self.keepRunning = True
	def run(self):
		try:
			while self.keepRunning:
				currentIn, currentOut, voltage, lux = self.batteryManagerObj.getReadings()
				relays = repr(self.batteryManagerObj.relay.status)
				self.currentBuf.addElement((currentIn-currentOut)*voltage)
				self.batteryCur += self.currentBuf.sRule(cfg.cfg["actor.basic.interval"])
				logEntry = logentry.Entry(currentInReading=currentIn, currentOutReading=currentOut, voltageReading=voltage, luxReading=lux, wattSeconds=self.batteryCur, relayStatus=relays)
				self.sensorLogger.recordEntry(logEntry)
				self.act(voltage, lux)
				time.sleep(cfg.cfg["actor.basic.interval"])
		except KeyboardInterrupt:
			self.batteryManagerObj.shutdown()
			self.sensorLogger.fileObj.flush()
			if "sensorlogger.connDetails" in cfg.cfg:
				self.sensorLogger.uploadFile(self.sensorLogger.logFileName)
	def checkConfig(self):
		for key in ["interval","relay.charge","relay.output","action.lux.threshold","action.lux.high","action.lux.low","action.voltage.threshold","action.voltage.high","action.voltage.low"]:
			cfg.cfg["actor.basic."+key] #throw key exception if the key isn't found
	def act(self, voltage, lux):
		self.actGeneric("voltage", voltage)
		self.actGeneric("lux", lux)
	def actGeneric(self, name, value):
		self.logger.debug("actor.basic.action."+name+".threshold: "+repr(cfg.cfg["actor.basic.action."+name+".threshold"]))
		self.logger.debug(name+": "+repr(value))
		valThresh = "low" if value < cfg.cfg["actor.basic.action."+name+".threshold"] else "high"
		valTokens = cfg.cfg["actor.basic.action."+name+"."+valThresh].split('.')
		relayStatus = valTokens[2].lower() == 'on'
		relayName = '.'.join(valTokens[0:2])
		if valThresh == "high":
			self.logger.debug(name+" above threshold")
		else:
			self.logger.debug(name+" below threshold")
			self.changeRelay(relayName, relayStatus)
	def changeRelay(self, relayName, relayStatus):
		relayIndex = self.resolveRelayName(relayName)
		if relayStatus:
			self.batteryManagerObj.relay.enable(relayIndex)
		else:
			self.batteryManagerObj.relay.disable(relayIndex)
	def resolveRelayName(self, relayName):
		return cfg.cfg["actor.basic."+relayName]
