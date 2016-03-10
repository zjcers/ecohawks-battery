#!/bin/bash
export PB_CONFIG_FILE = "test.conf"
export PB_TESTING = "True"
export PB_LOCAL_LUX = "True"
export PYTHON_PATH = $PYTHON_PATH:"dummydrivers":"utility":"drivers"
python main.py
