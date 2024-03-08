from GameMaster import GameMaster
def main():
    gm = GameMaster(2,5)
    
    # gm.grid.printCells()
    
    gm.addPlayer("jake", "description", 100)
    gm.addPlayer("John", "description", 100)
    gm.addPlayer("EJ", "description", 100)
    
    gm.addEnemy("Morph", "description", 100)
    
    gm.addItem("item1", "description")
    gm.giveItemToCharacter(gm.items[0], gm.players[0])

    # gm.listPlayers()
    
    gm.placeCharacterOnBoard(gm.getPlayers()[0], 0,1)
    
    gm.grid.printCells()
    print(gm.getPlayers()[0].getPos())
    
main()