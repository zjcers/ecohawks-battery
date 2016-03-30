#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 10 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 24 2016
from abc import ABCMeta, abstractmethod
class Actor():
    @abstractmethod
    def __init__(self, batteryManagerObj):
        pass
    @abstractmethod
    def act(self):
        pass
