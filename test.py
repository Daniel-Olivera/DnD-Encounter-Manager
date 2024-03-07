from Grid import Grid
from Objects import Character
from Objects import Item

def main():
    grid = Grid(2, 5)
    grid.printCells()
    print("------------------------")
    grid.addObjectToCell(0,0, Character(Character.TYPE_CHARACTER, "jake", "retard", 100, 4, None))
    grid.printCells()
    print("------------------------")
    
main()