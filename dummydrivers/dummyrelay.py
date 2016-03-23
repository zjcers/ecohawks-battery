#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 23 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 23 2016
import logging
#import relay abstract
import relay
class Relay(relay.Relay):
    def __init__(self):
        self.logger = logging.getLogger("PB.drivers.relay.dummy")
        self.logger.info("Starting")
    def enable(self, num):
        assert type(num) == int
        self.logger.info("Enabling relay #%i",num)
    def disable(self, num):
        assert type(num) == int
        self.logger.info("Disabling relay #%i",num)
