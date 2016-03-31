#!/bin/bash
#Original Author: Zane J Cersovsky
#Original Date: Mar 10 2016
#Last Modified By: Zane J Cersovsky
#Last Modified On: Mar 23 2016
set -e
#finds the base directory of the project from the location of this script
export PB_BASE_DIR=$(dirname $0)
#checks if a config file was passed, if not, uses the default one
if [ -z "$1" ]
  then
    export PB_CONFIG_FILE=$PB_BASE_DIR/conf/default.conf
  else
    export PB_CONFIG_FILE=$PB_BASE_DIR/conf/$1
fi
#shows python where all of the custom modules are
export PYTHONPATH=$PYTHONPATH":dummydrivers:utility:drivers:batterymanagers:actors:sensorLoggers"
#starts the project
python main.py
