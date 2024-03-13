import pygame
import pygame_gui
from GameMaster import GameMaster

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)
LIGHT_GREY = (200, 200, 200)
BLUE = (100,100,200)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

def main():
    
    gm = GameMaster(4, 50)
    gm.addPlayer("bob", "mage", 100)
    gm.placeCharacterOnBoard(gm.getPlayers()[0], 1,1)
    running = True
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(GREY)
    time_of_last_click = 0

    while running:
        drawGrid(gm, time_of_last_click)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                time_of_last_click = pygame.time.get_ticks()     
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                cell = getClickedCell(gm, pos)
                cell.setColor(LIGHT_GREY)
        
        pygame.display.update()

    pygame.quit()
    
    
def drawCell(gm, cell, x,y,size,borderSize, timeLastClick):
    # print(pygame.time.get_ticks() - time_of_last_click)
    if (pygame.time.get_ticks() - timeLastClick) >= 350:
        cell.setColor(WHITE)
        
    pygame.draw.rect(SCREEN, BLACK, (x, y, size+borderSize, size+borderSize))
    pygame.draw.rect(SCREEN, cell.getColor(), (x+borderSize/2, y+borderSize/2, size, size))    
    if cell.hasObjects():
        for obj in cell.getItems():
            if obj in gm.getPlayers():
                pygame.draw.circle(SCREEN, BLUE, (x+(size/1.8),y+(size/1.8)),18,0,1,1,1,1)

def drawGrid(gm, timeLastClick):
    gridCells = gm.getGridCells()
    index = 0
    for i in range(gm.getNumRows()):
        for j in range(gm.getNumCols()):
            cell = gridCells[index]
            drawCell(gm, cell, cell.getXCoord()+(i*cell.getSize()), cell.getYCoord()+(j*cell.getSize()), cell.getSize(), 8, timeLastClick)
            index += 1
  
            
def getClickedCell(gm, pos):
    cellSize = gm.getGridCellSize()
    convertedPos = (int(pos[0] / cellSize), int(pos[1] / cellSize))
    return gm.getCell(convertedPos)
            
            
if __name__ == "__main__":
    main()
