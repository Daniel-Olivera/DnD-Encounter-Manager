from Modules.Objects import Object

class Cell:
    x = 0
    y = 0
    size = 0
    color_r = 0
    color_g = 0
    color_b = 0
    cellObjects = set()
        
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color_r = 255
        self.color_g = 255
        self.color_b = 255
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
    
    def getColor(self):
        return (self.color_r,self.color_g,self.color_b)
    
    def setColor(self, color):
        self.color_r = color[0]
        self.color_g = color[1]
        self.color_b = color[2]
    
    def hasObjects(self):
        return self.cellObjects != set()
    