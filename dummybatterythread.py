#!/usr/bin/python2

import time
import threading
from batterystatus import BatteryStatus
battStatus = BatteryStatus()
lock = threading.Lock()
stop = threading.Event()
class DummyBatteryThread(threading.Thread):
	def __init__(self):
		self.chargeEnable = False
		self.chargeCurrent = 0.0 #mA
		self.capacity = 0.0 #mAh
		self.voltage = 11.5 #v
		self.INTEGRATIONTIME = 0.5 #s
		self.MAXCHARGECURRENT = 10.0 #mA
		self.MINCAPACITY = 0.0 #mAh
		self.MAXCAPACITY = 100.0 #mAh
		self.MINVOLTAGE = 11.5 #v
		self.MAXVOLTAGE = 13.5 #v
	def run():
		global battStatus
		global lock
		global stop
		while not stop.is_set():
			time.sleep(0.5)
			if self.capacity <= self.MAXCAPACITY:
				self.chargeEnable = True
				self.chargeCurrent = self.MAXCHARGECURRENT*(1-self.capacity/self.MAXCAPACITY)
			else:
				self.chargeEnable = False
				self.chargeCurrent = -1.0
			newCapacity = self.capacity+self.chargeCurrent*(1.0/7200.0)
			self.capacity = min(max(newCapacity, self.MINCAPACITY), self.MAXCAPACITY)
			self.voltage = self.MINVOLTAGE+((self.capacity-self.MINCAPACITY)/self.MAXCAPACITY)*(self.MAXVOLTAGE-self.MINVOLTAGE)
			self.lock.acquire(True)
			battStatus = BatteryStatus(chargeEnable = self.chargeEnable, chargeCurrent = self.chargeCurrent, voltage = self.voltage)
			self.lock.release()
