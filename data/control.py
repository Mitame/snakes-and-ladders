import pygame.display,pygame.font,pygame.event
import random
import time
from data import *

def main():
    #Init pygame
    pygame.font.init()
    pygame.init()
    
    #set a randomiser seed
    random.seed(input("Enter a seed for proc. gen.\n>"))
    
    #set up display 
    global screen,screenRect   
    screen = pygame.display.set_mode(tuple(settings.grid.size[i] * settings.grid.squareSize[i] for i in range(2)))
    pygame.display.set_caption("Snakes and Ladders")
    pygame.display.set_icon(images.raw.icon)
    screenRect = screen.get_rect()
    
    #create grids
    global grid,snakegrid,laddergrid,playergrid
    grid = objects.Grid(settings.grid.size,settings.grid.squareSize,textOverlay=True)
    snakegrid = objects.Grid(parent=grid, invisible=True,name = "snake")
    laddergrid = objects.Grid(parent=grid, invisible=True, name = "ladder")
    playergrid = objects.PlayerGrid(parent=grid, invisible=True, name = "player")
    
    #create onScreen dice
    global showDice,dice
    dice = objects.Dice(images.dice[0].get_rect(center = screen.get_rect().center))
    dice.startRoll()
    showDice = True
    
    #track empty spaces so you can't ride around the map on multiple snakes
    avaliablespaces = []
    avaliablespaces.extend(range(0,len(grid.list)))
    
    #add snakes
    for i in range(settings.gameplay.snakes):
        start = random.randint(settings.gameplay.itemBuffer,len(avaliablespaces)-1-settings.gameplay.itemBuffer-settings.gameplay.minSnakeDist)
        startpos = avaliablespaces.pop(start)
        end = random.randint(0,start-settings.gameplay.minSnakeDist)
        endpos = avaliablespaces.pop(end)
        objects.Snake(snakegrid,grid._conv(index=startpos),grid._conv(index=endpos))
    
    #add ladders
    for i in range(settings.gameplay.ladders):
        start = random.randint(settings.gameplay.itemBuffer,len(avaliablespaces)-1-settings.gameplay.itemBuffer-settings.gameplay.minLadderDist)
        startpos = avaliablespaces.pop(start)
        end = random.randint(start+settings.gameplay.minLadderDist,min(len(avaliablespaces)-1-settings.gameplay.itemBuffer,start+settings.gameplay.maxLadderDist))
        endpos = avaliablespaces.pop(end)
        objects.Ladder(snakegrid,grid._conv(index=startpos),grid._conv(index=endpos))
    
    #add players
    for i in range(settings.gameplay.players):
        objects.Player(playergrid,pos=(0,0))
    
    #add tracking variables
    global curPlayer
    curPlayer = 0
    
    #add some instruction signs
    global signs,font
    font = pygame.font.SysFont(settings.render.sysfont,20,bold=True)
    signs = objects.Signs()
    signs.createSign("Press 'r' to stop rolling",font,"stopDice",bg = settings.colours.signBG, centerx = screenRect.centerx,centery = screenRect.centery+70)
    
    
    while 1:
        startTime = time.time()
        screen.fill((0,0,0))
        
        #control turns
        getInputs()
        
        
        #update players
        playergrid.update()
        
        #draw grids
        grid.draw(screen)
        snakegrid.draw(screen)
        laddergrid.draw(screen)
        playergrid.draw(screen)
        
        #draw dice if it's visible atm
        if showDice:
            dice.draw(screen)

        #update and draw signs
        signs.update()
        signs.draw(screen)
                
        pygame.display.flip()
        try:
            time.sleep(startTime-time.time()+1/settings.render.fps)
        except ValueError:
            pass
        
def getInputs():
    global curPlayer,showDice
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.unicode == "r":
                dice.rolling = False
                signs.hide("stopDice")
        elif event.type == pygame.USEREVENT:
            if event.code == objects.userevents.stopRolling:
                time.sleep(settings.render.dicePauseTime)
                playergrid.sprites()[curPlayer].advance(dice.roll+1)
                showDice = False
            elif event.code == objects.userevents.finishedMoving:
                if playergrid.get((playergrid.size.w-1 if playergrid.size.h-1 % 2 == 0 else 0, playergrid.size.h-1)):
                    signs.createSign("Player %s has won!" % str(curPlayer+1),font,"winningPlayer", timeout = -1, bg=settings.colours.signBG,
                                     centerx = screenRect.centerx,centery = screenRect.centery)
                else:
                    curPlayer = (curPlayer + 1) % len(playergrid.sprites())
                    signs.createSign("It's Player %s's turn!" % str(curPlayer+1),font,"newPlayer", timeout = 60, bg=settings.colours.signBG,
                                     x = screenRect.left+5,y = screenRect.top+5)
                    showDice = True
                    dice.startRoll()
                    signs.show("stopDice")

def gridToPix(pos):
    pass

if __name__ == "__main__":
    main()
