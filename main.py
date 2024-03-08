import pygame
from GameMaster import GameMaster

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

def main():
    
    gm = GameMaster(4, 50)
    
    running = True
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(GREY)

    while running:
        drawGrid(gm)
        # drawCell(0,0,50,8)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()

    pygame.quit()
    
    
def drawCell(x,y,size,borderSize):
    pygame.draw.rect(SCREEN, BLACK, (x, y, size+borderSize, size+borderSize))
    pygame.draw.rect(SCREEN, WHITE, (x+borderSize/2, y+borderSize/2, size, size))

def drawGrid(gm):
    gridCells = gm.getGridCells()
    for i in range(gm.getNumRows()):
        for j in range(gm.getNumCols()):
            cell = gridCells[i]
            drawCell(cell.getXCoord()+(j*cell.getSize()), cell.getYCoord()+(i*cell.getSize()), cell.getSize(), 8)
            
            
if __name__ == "__main__":
    main()
