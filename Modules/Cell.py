from Modules.Objects import Object

class Cell:
    x = 0
    y = 0
    size = 0
    
    cellObjects = set()
        
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.cellObjects = set()
    
    def addObject(self, newObject):
        self.cellObjects.add(newObject)
        
    def removeObject(self, obj):
        self.cellObjects.discard(obj)
        
    def getXCoord(self):
        return self.x
    
    def getYCoord(self):
        return self.y
    
    def getSize(self):
        return self.size
    
    def getItems(self):
        return self.cellObjects
    