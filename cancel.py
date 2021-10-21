class cancelId:
    def __init__(self):
        self.id = [] 
        self.time = 0
        self.flag = False

    def getFlag(self):
        return self.flag

    def setFlag(self, value):
        self.flag = value

    def add(self, num):
        self.id.append(num)

    def getId(self):
        return self.id

    def getTime(self):
        return self.time