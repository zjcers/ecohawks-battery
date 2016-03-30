#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 24 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 24 2016
import time
import logging
import cfg
import logger
import batteryManager
#import actor abstract
import absactor
class Actor(absactor.Actor):
    def __init__(self):
        self.logger = logging.getLogger("PB.actor.basic")
        self.logger.info("Starting up")
        self.batteryManagerObj = batteryManager.BatteryManager()
        self.batteryManagerObj.startThreads()
        self.sensorLogger = logger.Logger()
        self.keepRunning = True
        self.checkConfig()
    def run(self):
        try:
            while self.keepRunning:
                currentIn, currentOut, voltage, lux = self.batteryManagerObj.getReadings()
                relays = repr(self.batteryManagerObj.relay.status)
                logEntry = self.sensorLogger.makeEntry(currentIn[0], currentOut[0], voltage[0], lux[0], relays)
                self.sensorLogger.recordEntry(logEntry)
                self.act(currentIn, currentOut, voltage, lux)
                time.sleep(1)
        except KeyboardInterrupt:
            self.batteryManagerObj.shutdown()
    def checkConfig(self):
        for key in ["relay.charger","relay.output","action.lux.threshold","action.lux.high","action.lux.low","action.voltage.threshold","action.voltage.high","action.voltage.low"]:
            cfg.cfg["actor.basic."+key] #throw key exception if the key isn't found
    def act(self, voltage, lux):
        self.actGeneric("voltage", voltage)
        self.actGeneric("lux", lux)
    def actGeneric(self, name, value):
        valThresh = "low" if value < cfg.cfg["actor.basic."+name+".threshold"] else "high"
        valTokens = cfg.cfg["actor.basic.action."+name+"."+valThresh]
        relayStatus = valTokens[2].lower() == 'on'
        relayName = '.'.join(valTokens[0:2])
        if valOnOff:
            self.logger.info(name+" above threshold")
        else:
            self.logger.info(name+" below threshold")
        self.changeRelay(relayName, relayStatus)
    def changeRelay(self, relayName, relayStatus):
        relayIndex = resolveRelayName(relayName)
        self.batteryManagerObj.relay()
