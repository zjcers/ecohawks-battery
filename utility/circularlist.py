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
