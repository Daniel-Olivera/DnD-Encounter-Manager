import pygame
from GameMaster import GameMaster
from Modules.UI import UI

WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280

def main():
    
    gm = GameMaster(50, 50)
    gm.addPlayer("Evan", "mage", 100)
    gm.addEnemy("Hunnlef", "archer", 100)
    gm.placeCharacterOnBoard(gm.getPlayers()[0], 1,1)
    gm.placeCharacterOnBoard(gm.getEnemies()[0], 2,3)
    running = True
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption('DND Encounter Simulator')
    time_of_last_click = 0
    offsetx = 0
    offsety = 0
    global font
    displayText = False
    dragging = False
    scale = 0
    ui = UI(SCREEN, gm, time_of_last_click=0, offsetx=0, offsety=0)

# MAIN LOOP
    while running:
        font = pygame.font.Font('freesansbold.ttf', int(gm.getGridCellSize()/5))
        ui.draw(gm, time_of_last_click, offsetx, offsety)
        
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
                    if ui.clickedInGrid(mousePos):
                        cell = ui.getClickedCell(gm, mousePos, (offsetx, offsety))
                        if cell is not None:
                            # TODO add cell info to banner
                            cell.setColor(ui.DARK_GREY)
                            ui.displayText(cell)
                    else:
                        newColor = ui.getClickedColor(mousePos)
                        ui.changeCellColor(newColor, cell)
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
                
if __name__ == "__main__":
    main()
