class CircularList():
	def __init__(self, maxLength):
		self.maxLength = maxLength
		self.internalList = []
	def addElement(self, element):
		if len(self.internalList) == self.maxLength:
			self.internalList.pop()
		self.internalList.append(element)
	def average(self):
		if len(self.internalList) == 0:
			return 0
		return sum(self.internalList)/len(self.internalList)
	def sRule(self, interval):
		if len(self.internalList) != 0:
			return (len(self.internalList)/6.0)*(self.internalList[0]+4*self.internalList[len(self.internalList)/2]+self.internalList[-1])
		return 0.0
