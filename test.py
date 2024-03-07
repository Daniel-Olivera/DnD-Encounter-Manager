from Grid import Grid

def main():
    grid = Grid(2, 5)
    grid.printCells()
    print("------------------------")
    grid.addObjectToCell(0,1,1)
    grid.addObjectToCell(1,1,5)
    grid.printCells()
    
main()