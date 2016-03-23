#!/usr/bin/python2
#Original Author: Zane J Cersovsky
#Original Date: Mar 10 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 23 2016
#handles importing logic for pluggable components (mostly sensors)

#import needed STL modules
import sys
#import needed custom modules
import cfg
#by now cfg should have already been loaded by main.py, so cfg.cfg should be accessable
#if that's not the case, we need to halt right here
cfg.cfg #will throw an exception if cfg not loaded

#little helper function to import modules as aliases on the fly
#no error checking is done since the caller is responsible for checking prior to call
def importhelper(name, alias):
    module = __import__(name)
    sys.modules[alias] = module

#import rest of custom modules
modules = cfg.cfg["modules"]
for mod in modules:
    importhelper(cfg.cfg[mod], mod)
