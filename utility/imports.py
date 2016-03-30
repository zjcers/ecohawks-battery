#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 10 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 24 2016
#handles importing logic for pluggable components (mostly sensors)

#import needed STL modules
import logging
import sys

import cfg
#little helper function to import modules as aliases on the fly
#no error checking is done since the caller is responsible for checking prior to call
importLogger = logging.getLogger("PB.imports")
def importhelper(name, alias):
    importLogger.debug("Loading %s as %s", name, alias)
    sys.modules[alias] = __import__(name)
for mod in cfg.cfg["modules"]:
    importhelper(cfg.cfg[mod], mod)
