import pygame
# import pygame_gui
from GameMaster import GameMaster

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)
LIGHT_GREY = (200, 200, 200)
BLUE = (100,100,200)
WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280
BORDERSIZE = 2

def main():
    
    gm = GameMaster(4, 50)
    gm.addPlayer("bob", "mage", 100)
    gm.placeCharacterOnBoard(gm.getPlayers()[0], 1,1)
    running = True
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption('DND Encounter Simulator')
    time_of_last_click = 0
    offsetx = 0
    offsety = 0
    font = pygame.font.Font('freesansbold.ttf', 15)
    displayText = False
    dragging = False
    scale = 0

    while running:
        SCREEN.fill(GREY)
        drawGrid(gm, time_of_last_click, (offsetx, offsety))
        drawUI()
        if displayText:
            text = font.render('test', True, BLACK, WHITE)
            textRect = text.get_rect()
            textRect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
            SCREEN.blit(text, textRect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    time_of_last_click = pygame.time.get_ticks()
                if event.button == 2:
                    mouse_x, mouse_y = event.pos  
                    drag_start_pos_x = offsetx - mouse_x
                    drag_start_pos_y = offsety - mouse_y
                    dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    dragging = False
                if event.button == 1:
                    mousePos = pygame.mouse.get_pos()
                    if clickedInGrid(mousePos):
                        cell = getClickedCell(gm, mousePos, (offsetx, offsety))
                        if cell is not None:
                            # TODO add cell info to banner
                            cell.setColor(LIGHT_GREY)
                            displayText = True
            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_x, mouse_y = event.pos
                    offsetx = mouse_x + drag_start_pos_x
                    offsety = mouse_y + drag_start_pos_y
            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    scale = 3
                if event.y == -1:
                    scale = (-3)
                gm.setGridCellSize(gm.getGridCellSize() + scale)
    

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            offsety -= 0.15 * gm.getGridSize()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            offsetx -= 0.15 * gm.getGridSize()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            offsety += 0.15 * gm.getGridSize()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            offsetx += 0.15 * gm.getGridSize()
        if keys[pygame.K_SPACE]:
            offsetx = 0
            offsety = 0

        pygame.display.update()

    pygame.quit()
    
    
def drawCell(gm, cell, x,y,size, timeLastClick):
    # print(pygame.time.get_ticks() - time_of_last_click)
    if (pygame.time.get_ticks() - timeLastClick) >= 350:
        cell.setColor(WHITE)
        
    # pygame.draw.rect(SCREEN, BLACK, (x, y, size+BORDERSIZE, size+BORDERSIZE))
    pygame.draw.rect(SCREEN, cell.getColor(), (x, y, size-BORDERSIZE, size-BORDERSIZE))    
    if cell.hasObjects():
        for obj in cell.getItems():
            if obj in gm.getPlayers():
                pygame.draw.circle(SCREEN, BLUE, (x+(size/2),y+(size/2)),size/2.5,0,1,1,1,1)

def drawGrid(gm, timeLastClick, cameraOffset):
    gridCells = gm.getGridCells()
    index = 0
    for i in range(gm.getNumRows()):
        for j in range(gm.getNumCols()):
            cell = gridCells[index]
            drawCell(gm, cell, cell.getXCoord()+(i*cell.getSize())+cameraOffset[0], cell.getYCoord()+(j*cell.getSize())+cameraOffset[1],
                     cell.getSize(), timeLastClick)
            index += 1
  
def getClickedCell(gm, mousePos, offset):
    cellSize = gm.getGridCellSize()
    gridposx, gridposy = mousePos
    gridposx -= offset[0]
    gridposy -= offset[1]
    convertedPos = (int((gridposx - (gridposx/cellSize)) / cellSize), int((gridposy - (gridposy/cellSize)) / cellSize))
    return gm.getCell(convertedPos)

def clickedInGrid(mousePos):
    return (mousePos[0] > 0) and (mousePos[1] > 0) and (mousePos[0] < 950) and (mousePos[1] < 500)
    
    
def drawUI():
    pygame.draw.rect(SCREEN, WHITE, (0,500,950,720))
    pygame.draw.rect(SCREEN, WHITE, (950,0,1280,720))
    pygame.draw.line(SCREEN,BLACK,(950,0),(950,720))
    pygame.draw.line(SCREEN,BLACK,(0,500),(950,500))
    
            
if __name__ == "__main__":
    main()
