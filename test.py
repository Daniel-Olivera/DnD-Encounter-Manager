from GameMaster import GameMaster
def main():
    gm = GameMaster(2,5)
    
    # gm.grid.printCells()
    
    gm.addPlayer("jake", "bonehead", 100)
    gm.addPlayer("John", "jobless", 100)
    gm.addPlayer("EJ", "pokefile", 100)
    
    gm.addEnemy("Morph", "brick", 100)
    
    gm.addItem("Sword of Healing", "Heals instead of doing damage")
    gm.giveItemToCharacter(gm.items[0], gm.players[0])

    # gm.listPlayers()
    
    gm.placeCharacterOnBoard(gm.getPlayers()[0], 0,1)
    
    gm.grid.printCells()
    print(gm.getPlayers()[0].getPos())
    
main()