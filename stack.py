class stack:
    def __init__(self):
        self.arr = []
        self.currentIteration = 0

    def pop(self):
        return self.arr.pop()

    def peek(self):
        return self.arr[-1]

    def add(self, item):
        self.arr.append(item)

    def length(self):
        return len(self.arr)

    def search(self, item):
        if item in self.arr:
            return True

    def clear(self):
        self.arr = []

    def addIteration(self):
        self.currentIteration += 1

    def subIteration(self):
        self.currentIteration -= 1

    def getCurrentItems(self):
        return self.arr[self.currentIteration]

    def getIteration(self):
        return self.currentIteration

    def printArray(self):
        print(self.arr)
