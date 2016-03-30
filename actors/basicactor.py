#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 24 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 24 2016
import time
import cfg
import logger
import batteryManager
#import actor abstract
import absactor
class Actor(absactor.Actor):
    def __init__(self):
        self.batteryManagerObj = batteryManager.BatteryManager()
        self.batteryManagerObj.startThreads()
        self.sensorLogger = logger.Logger()
        self.keepRunning = True
    def run(self):
        try:
            while self.keepRunning:
                currentIn, currentOut, voltage, lux = self.batteryManagerObj.getReadings()
                relays = repr(self.batteryManagerObj.relay.status)
                logEntry = self.sensorLogger.makeEntry(currentIn[0], currentOut[0], voltage[0], lux[0], relays)
                self.sensorLogger.recordEntry(logEntry)
                time.sleep(1)
        except KeyboardInterrupt:
            self.batteryManagerObj.shutdown()
