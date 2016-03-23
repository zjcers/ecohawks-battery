#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 10 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 10 2016
import exceptions
class ConfigFileException(exceptions.Exception):
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return str(val)
