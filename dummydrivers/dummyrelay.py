#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 23 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 23 2016
import logging
#import relay abstract
import abstractrelay
class Relay(abstractrelay.Relay):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger("PB.drivers.relay.dummy")
        self.logger.info("Starting")
        self.status = [False, False, False, False]
    def enable(self, num):
        assert type(num) == int
        assert num >= 1 and num <= 4
        if not self.status[num-1]:
            self.logger.info("Enabling relay #%i",num)
            self.status[num-1] = True
    def disable(self, num):
        assert type(num) == int
        assert num >= 1 and num <= 4
        if self.status[num-1]:
            self.logger.info("Disabling relay #%i",num)
            self.status[num-1] = False
