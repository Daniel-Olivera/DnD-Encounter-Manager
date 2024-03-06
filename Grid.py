from Cell import Cell

class Grid:
    size = 0
    cellSize = 0
    numCells = 0
    
    cells = []
    
    def __init__(self, size, cellSize):
        self.size = size
        self.cellSize = cellSize
        self.numCells = pow(size,2)
        self.cells = [Cell(cellSize, None)]*self.numCells
    
    def getSize(self):
        return self.size
    
    def getNumCells(self):
        return self.numCells
    
    def getCellSize(self):
        return self.cellSize
    
    def setGridSize(self, newSize):
        self.size = newSize
        self.numCells = pow(newSize, 2)
        
    def setCellSize(self, newCellSize):
        self.cellSize = newCellSize
        
    def printCells(self):
        for cell in self.cells:
            print(cell)