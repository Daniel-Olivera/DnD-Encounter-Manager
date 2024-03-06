from Object import Object

class Cell:
    size_x = 0
    size_y = 0
    
    objects = []
    
    def __init__(self, size):
        self.size_x = size
        self.size_y = size
        
    def __init__(self, size, objects):
        self.size_x = size
        self.size_y = size
        self.objects = objects
    
    def addObject(self, newObject):
        self.objects.append(newObject)
        
    def removeObject(self, index):
        self.objects.pop(index)
    