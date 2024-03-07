from Object import Object

class Cell:
    x = 0
    y = 0
    size_x = 0
    size_y = 0
    
    cellObjects = []
        
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size_x = size
        self.size_y = size
        self.cellObjects = []
    
    def addObject(self, newObject):
        self.cellObjects.append(newObject)
        
    def removeObject(self, index):
        self.cellObjects.pop(index)
        
    def getXCoord(self):
        return self.x
    
    def getYCoord(self):
        return self.y
    
    def getItems(self):
        return self.cellObjects
    