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
    offsetx = 0
    offsety = 0

    while running:
        SCREEN.fill(GREY)
        drawGrid(gm, time_of_last_click, (offsetx, offsety))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                time_of_last_click = pygame.time.get_ticks()     
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                cell = getClickedCell(gm, pos, (offsetx, offsety))
                cell.setColor(LIGHT_GREY)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            offsety -= 0.25
            print("w")
        if keys[pygame.K_a]:
            offsetx -= 0.25
            print("a")
        if keys[pygame.K_s]:
            offsety += 0.25
            print("s")
        if keys[pygame.K_d]:
            offsetx += 0.25
            print("d")

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

def drawGrid(gm, timeLastClick, cameraOffset):
    gridCells = gm.getGridCells()
    index = 0
    for i in range(gm.getNumRows()):
        for j in range(gm.getNumCols()):
            cell = gridCells[index]
            drawCell(gm, cell, cell.getXCoord()+(i*cell.getSize())+cameraOffset[0], cell.getYCoord()+(j*cell.getSize())+cameraOffset[1],
                     cell.getSize(), 8, timeLastClick)
            index += 1
  
            
def getClickedCell(gm, pos, offset):
    cellSize = gm.getGridCellSize()
    convertedPos = (int((pos[0] / cellSize)+offset[0]), int((pos[1] / cellSize)+offset[1]))
    return gm.getCell(convertedPos)
            
            
if __name__ == "__main__":
    main()
