import logging
import csv
import subprocess
import time
import cfg
import logentry
import abssensorlogger
class Logger(abssensorlogger.Logger):
	def __init__(self):
		self.logger = logging.getLogger("PB.logger.csv")
		self.fieldnames = cfg.cfg["sensorlogger.fieldnames"]
		self.interval = cfg.cfg["sensorlogger.interval"]
		self.lastTime = 0
		self.switchFiles()
		if "sensorlogger.upload.connDetails" in cfg.cfg:
			self.connDetails = cfg.cfg["sensorlogger.upload.connDetails"]
			self.upload = True
		else:
			self.upload = False
		if "sensorlogger.lines" in cfg.cfg:
			self.lines = cfg.cfg["sensorlogger.lines"]
		else:
			self.lines = 100
		self.writtenLines = 0
	def recordEntry(self, entry):
		assert type(entry) == logentry.Entry
		if time.time()-self.lastTime > self.interval:
			self.lastTime = time.time()
			self.logger.debug("Writing %s", repr(entry))
			self.writer.writerow(entry)
			self.writtenLines += 1
			self.fileObj.flush()
			self.handleFiles()
	def handleFiles(self):
		if self.writtenLines == self.lines:
			self.logger.info("Line count reached, switching files")
			oldName = self.logFileName
			self.switchFiles()
		if self.upload:
			self.uploadFile(oldName)
	def uploadFile(self, fileName):
		s = subprocess.Popen(["sftp", self.connDetails], stdin=subprocess.PIPE)
		s.stdin.write("put "+fileName+"\n")
		s.stdin.close()
	def getTimeStamp(self):
		return time.strftime("%Y%m%d-%H%M%S")
	def switchFiles(self):
		self.logFileName = cfg.cfg["sensorlogger.target"]+self.getTimeStamp()+".csv"
		self.logger.info("Log target is now: %s", self.logFileName)
		self.fileObj = open(self.logFileName, 'w')
		self.writer = csv.DictWriter(self.fileObj, fieldnames=self.fieldnames)
		self.writer.writeheader()
		self.fileObj.flush()
