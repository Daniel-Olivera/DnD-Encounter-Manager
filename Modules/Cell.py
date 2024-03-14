from Modules.Objects import Object

class Cell:
        
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.permanentColor_r = 25
        self.permanentColor_g = 25
        self.permanentColor_b = 30
        self.color_r = 25
        self.color_g = 25
        self.color_b = 30
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
    
    def setSize(self, newSize):
        self.size = newSize
    
    def getItems(self):
        return self.cellObjects
    
    def getColor(self):
        return (self.color_r,self.color_g,self.color_b)
    
    def setColor(self, color):
        self.color_r = color[0]
        self.color_g = color[1]
        self.color_b = color[2]
        
    def getPermanentColor(self):
        return (self.permanentColor_r,self.permanentColor_g,self.permanentColor_b)
    
    def setPermanentColor(self, color):
        self.permanentColor_r = color[0]
        self.permanentColor_g = color[1]
        self.permanentColor_b = color[2]
    
    def hasObjects(self):
        return self.cellObjects != set()
    