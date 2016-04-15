import time
import logging
import cfg
import sensorlogger
import logentry
import batteryManager
import circularlist
#import actor abstract
import absactor
class Actor(absactor.Actor):
	def __init__(self):
		self.logger = logging.getLogger("PB.actor.real")
		self.logger.info("Starting up")
		self.batteryManagerObj = batteryManager.BatteryManager()
		self.batteryManagerObj.startThreads()
		self.sensorLogger = sensorlogger.Logger()
		self.keepRunning = True
		self.batteryCur = False
		self.batteryMax = False
		self.currentBuf = circularlist.CircularList(3)
	def run(self):
		try:
			while self.keepRunning:
				currentIn, currentOut, voltage, lux = self.batteryManagerObj.getReadings()
				if lux < cfg.cfg["actor.real.luxThreshold"]:
					if currentOut > cfg.cfg["actor.real.currentOutThreshold"]:
						if self.getSoC() < 1.0:
							rStatus =  self.batteryManagerObj.relay.getStatus(cfg.cfg["actor.real.relay.charge"])
							if rStatus[1] > cfg.cfg["actor.real.relay.chargeTimeout"]:
								self.batteryManagerObj.relay.disable(cfg.cfg["actor.real.relay.charge"])
							else:
								self.batteryManagerObj.relay.enable(cfg.cfg["actor.real.relay.charge"])
				if currentIn < cfg.cfg["actor.real.currentInThreshold"]:
					self.batteryMax = self.batteryCur
				self.currentBuf.addElement(currentIn-currentOut)
				self.batteryCur += self.currentBuf.sRule(cfg.cfg["actor.real.interval"])
				relays = repr(self.batteryManagerObj.relay.status)
				logEntry = logentry.Entry(currentInReading=currentIn, currentOutReading=currentOut, voltageReading=voltage, luxReading=lux, SoCalc=self.getSoC(), ampSeconds=self.batteryCur, relayStatus=relays)
				self.sensorLogger.recordEntry(logEntry)
				time.sleep(cfg.cfg["actor.real.interval"])
		except KeyboardInterrupt:
			self.batteryManagerObj.shutdown()
		self.sensorLogger.fileObj.flush()
		if "sensorlogger.upload.connDetails" in cfg.cfg:
			self.sensorLogger.uploadFile(self.sensorLogger.logFileName)
	def getSoC(self):
		if self.batteryCur and self.batteryMax:
			return self.batteryCur/self.batteryMax
		else:
			return False
