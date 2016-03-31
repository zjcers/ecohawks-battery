import sys
import logging
import urllib2
#import sensor abstract
import abstractsensor
class LuxSensor(abstractsensor.Sensor):
    def __init__(self, bus=1, addr="192.168.4.1"):
        self.logger = logging.getLogger("PB.drivers.luxsensor.remote")
        self.logger.info("Starting with parameters:, addr=%s",addr)
        self.addr = addr
    def getReading(self):
        r = urllib2.urlopen("http://"+self.addr+"/lux")
        return float(r.read().strip())
if __name__ == "__main__":
	if len(sys.argv) == 1:
		l = LuxSensor()
	elif len(sys.argv) == 2:
		l = LuxSensor(addr=sys.argv[1])
	else:
		print "Invalid arguments"
		exit(1)
	print "Current Lux: ",l.getReading()
