#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 8 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 23 2016

#Load required STL modules
import os
import logging
#set up logging
logging.getLogger("PB").setLevel(logging.INFO)
logging.basicConfig(format="[%(asctime)s %(name)s] %(message)s")
mainLogger = logging.getLogger("PB.main")
mainLogger.info("Prius Battery control program initializing")
#Load config modules
mainLogger.info("Setting up configuration")
import config
import cfg
if "PB_CONFIG_FILE" in os.environ:
	cfg.cfg = config.config(os.environ["PB_CONFIG_FILE"])
else:
	cfg.cfg = config.config("conf/dummy.conf")
if "debug" in cfg.cfg:
	logging.getLogger("PB").setLevel(logging.DEBUG)
	mainLogger.debug("Debugging enabled")
#import the following pluggable modules (as defined in conf file):
#currentInSensor: dummycurrentsensor | currentsensor
#currentOutSensor: dummycurrentsensor | currentsensor
#luxSensor: dummyluxsensor | localluxsensor | remoteluxsensor
#voltageSensor: dummyvoltagesensor | voltagesensor
#batteryManager: basicbatterymanager
#batteryController: simplebatterycontroller
#actor: dummyactor
import imports
#this is now aliased by imports
import actor
if __name__ == "__main__":
	mainActor = actor.Actor()
	mainActor.run()
