import pygame.sprite,pygame.event
import math
import copy
import random

from data import settings,images

class userevents():
    stopRolling = 1
    finishedMoving = 2
    
class Grid(pygame.sprite.OrderedUpdates):
    
    def __init__(self,size=None,squareSize=None,parent = None,invisible = None,textOverlay=False,name = None):
        pygame.sprite.OrderedUpdates.__init__(self)
        if parent is not None:
            try:
                self.parent = parent
                self.size = parent.size
                self.squareSize = parent.squareSize
                if name is None:
                    self.parent.children[len(self.parent.children)] = self
                else:
                    self.parent.children[name] = self
            except NameError:
                raise TypeError("Argument 'parent' must be grid, not '%s'" % str(type(parent)))
        else:
            self.size = pygame.Rect((0,0),size)
            self.squareSize = squareSize
        
        self.textOverlay = textOverlay
        self.invisible = invisible
        self.genImage()
        
        self.children = {}
        self.list = []
        self.fillList(0)
    def genImage(self):
        self.rect = pygame.Rect((0,0),tuple(self.size.size[i] * self.squareSize[i] for i in range(2)))
        if self.invisible:
            self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        else:
            self.image = pygame.Surface(self.rect.size)
            for x in range(self.size.w):
                for y in range(self.size.h):
                    colour = [settings.colours.grid1,settings.colours.grid2][(x+y)%2]
                    self.image.fill(colour, rect=(tuple((x,y)[i]*self.squareSize[i] for i in range(2)),self.squareSize))
            if self.textOverlay:
                font = pygame.font.SysFont("Ubuntu", 12, False, False)
                for x in range(self.size.w):
                    for y in range(self.size.h):
                        if y % 2 == 0:
                            pos = y*self.size.w + x
                        else:
                            pos = (y+1)*self.size.w - (x+1)
                        if settings.grid.zeroBased:
                            pos += 1
                        colour = [settings.colours.textOverlay1,settings.colours.textOverlay2][(x+y)%2]
                        Surf = font.render("FINISH" if pos == 100 else str(pos), True, colour)
                        self.image.blit(Surf,tuple((x,y)[i] * self.squareSize[i] for i in range(2)))
        
    def fillList(self,value,doCopy=False):
        if len(self.list):
            for x in range(len(self.list)):
                self.list[x] = value if doCopy is False else copy.deepcopy(value)
        else:
            self.list = []
            for x in range(self._conv(pos=tuple(self.size.size[i] - 1 for i in range(2)))):
                self.list.append(value if doCopy is False else copy.deepcopy(value))
    
    def get(self,pos):
        if self.isWithin(pos,True):
            return self.list[self._conv(pos)]
    
    def set(self,pos,value,replace=False):
        if self.isWithin(pos,True):
            self.list[self._conv(pos)] = value
            
    def isWithin(self,pos,throwError=False):
        if (0<=pos[0]<self.size.w) and (0<=pos[1]<self.size.h):
            return True
        else:
            if throwError:
                raise IndexError(str(pos)+" is outside the grid (size %s)." % self.size.size)
    
    def _conv(self,pos=None,index=None):
        if pos and self.isWithin(pos):
            return self.size.w*pos[1]+pos[0]
        else:
            return (index % self.size.w,index // self.size.w)

    def draw(self, surface):
        surface.blit(self.image,self.rect)
        pygame.sprite.OrderedUpdates.draw(self, surface)

class Snake(pygame.sprite.Sprite):    
    def __init__(self,parent,startPos,endPos):
        pygame.sprite.Sprite.__init__(self,parent)
        self.parent = parent
        self.startPos = startPos
        self.endPos = endPos
        self.parent.set(self.startPos,self)
        self.genImage()

    def genImage(self,image=images.raw.snake,minWidth = settings.render.minSnakeWidth):
        diff = tuple(self.endPos[i]-self.startPos[i] for i in range(2))
        length = math.sqrt((diff[0]*self.parent.squareSize[0])**2+(diff[1]*self.parent.squareSize[1])**2)
        try:
            rotate = math.degrees(math.atan(diff[0]/diff[1]))
            if diff[1] < 0: 
                rotate += 180
        except ZeroDivisionError:
            rotate = 0
            if diff[1] == 0:
                rotate += 90
            if diff[0] < 0:
                rotate += 180
        
        
        scale = length/image.get_size()[1]
        self.image = pygame.transform.smoothscale(image,tuple(int(max(image.get_size()[i] * scale,minWidth)) for i in range(2)))
        self.image = pygame.transform.rotate(self.image,rotate)
#         offset = (0.5,-1.5)
        offset = (0,0)
        midPoint = tuple((self.startPos[i]+self.endPos[i]+offset[i]*2)/2 for i in range(2))
        center = tuple((midPoint[i]+0.5)*self.parent.squareSize[i] for i in range(2))
        self.rect = self.image.get_rect(center=center)
        
        
class Ladder(Snake):
    
    def genImage(self, image=images.raw.ladder,minWidth=settings.render.minLadderWidth):
        Snake.genImage(self, image=image, minWidth=minWidth)

class PlayerGrid(Grid):
    
    def __init__(self, size=None, squareSize=None, parent=None, invisible=None, textOverlay=False, name=None):
        Grid.__init__(self, size=size, squareSize=squareSize, parent=parent, invisible=invisible, textOverlay=textOverlay, name=name)
        self.fillList([],True)
    
    def set(self, pos, value, replace=False):
        if self.isWithin(pos):
            self.list[self._conv(pos)].append(value)
        else:
            raise IndexError(str(pos)+" is outside the range of the grid.")
    
    def remove(self,pos,value):
        self.list[self._conv(pos)].remove(value)
    
    def get(self,pos,index=None):
        if index is not None:
            return self.list[self._conv(pos)][index]
        else:
            x = self._conv(pos)
            return self.list[x]
            
class Player(pygame.sprite.Sprite):
    
    def __init__(self,parent,playerIndex=None,pos=(0,0)):
        pygame.sprite.Sprite.__init__(self,parent)
        self.parent = parent
        if playerIndex is not None:
            self.playerIndex = playerIndex
        else:
            self.playerIndex = len(self.parent.spritedict.keys())-1
        self.pos = pos
        self.parent.set(self.pos,self)
        self.genImage()
        self.rectList = [self.rect]
    
    def genImage(self,stopRecursion=False,setRect=True):
        playerInSquare = len(self.parent.get(self.pos))
        index = self.parent.get(self.pos).index(self)
        if playerInSquare == 1:
            self.image = images.players["size1"][self.playerIndex]
            extra = (0,0)
        elif playerInSquare <= 4:
            if playerInSquare == 2 and not stopRecursion:
                for x in self.parent.get(self.pos):
                    x.genImage(True)
            self.image = images.players["size2"][self.playerIndex]
            
            extra = ((index // 2)/2,(index % 2)/2)
        else:
            if playerInSquare == 5 and not stopRecursion:
                for x in self.parent.get(self.pos):
                    x.genImage(True)
            self.image = images.players["size3"][self.playerIndex]
            extra = ((index % 3)/3,(index // 3)/3)
            
        if setRect:
            self.rect = self.image.get_rect(topleft = tuple((self.pos[i]+extra[i])*self.parent.squareSize[i] for i in range(2)))
            try:
                if len(self.rectList) == 1:
                    self.rectList[0] == self.rect
            except AttributeError:
                pass
                
        else:
            return self.image.get_rect(topleft = tuple((self.pos[i]+extra[i])*self.parent.squareSize[i] for i in range(2)))
        
    def move(self,pos,overFrames = settings.render.fps*settings.render.timeToMove, itemCheck = True):
        if pos == self.pos:
            return
        prevPos = self.pos
        prevRect = self.rect
        self.parent.remove(self.pos,self)
        self.pos = pos
        self.parent.set(self.pos,self)
        newRect = self.genImage(setRect=False)
        for x in self.parent.get(self.pos):
            x.genImage()
        
        pixDiff = tuple(newRect.topleft[i]-self.rectList[-1][i] for i in range(2))
        startRect = self.rectList[-1]
        for frame in range(1,overFrames+1):
            self.rectList.append(pygame.Rect(tuple(int(startRect[i]+pixDiff[i]*(frame/overFrames)) for i in range(2)),newRect.size))
        
        if itemCheck:
            snake = self.parent.parent.children["snake"].get(self.pos)
            ladder = self.parent.parent.children["ladder"].get(self.pos)
            if snake:
                self.move(snake.endPos)
            if ladder:
                self.move(ladder.endPos)
        
    def update(self):
        self.rect = self.rectList.pop(0)
        if len(self.rectList) == 0:
            self.rectList.append(self.rect)
        elif len(self.rectList) == 1:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT,code=userevents.finishedMoving))
              
    def advance(self,spaces):
        cornered = 1
        if self.pos[1] == self.parent.size.w-1:
            if self.pos[1] % 2 == 0:
                if self.pos[0] + spaces > self.parent.size.w:
                    self.move((self.parent.size.w-1,self.pos[1]),overFrames=int(settings.render.timeToMove*settings.render.fps/2),itemCheck = False)
                    pos = (self.parent.size.w-(self.pos[1]+spaces-self.parent.size.w),self.pos[1])
                    cornered = 2
                else:
                    pos = (self.parent.size.w-(spaces-(self.parent.size.w-self.pos[0]))-1,self.pos[1]+1)
                
            else:
                if self.pos[0]-spaces < 0:
                    pos = (-self.pos[0]+spaces,self.pos[1])
                    self.move((0,self.pos[1]),overFrames=int(settings.render.timeToMove*settings.render.fps/2),itemCheck = False)
                    cornered = 2
                else:
                    pos = (self.pos[0]-spaces,self.pos[1])
        
        elif self.pos[1] % 2 == 0:
            if self.pos[0]+spaces >= self.parent.size.w:
                pos = (self.parent.size.w-(spaces-(self.parent.size.w-self.pos[0]))-1,self.pos[1]+1)
                self.move((self.parent.size.w-1,self.pos[1]),overFrames=int(settings.render.timeToMove*settings.render.fps/3),itemCheck = False)
                self.move((self.parent.size.w-1,self.pos[1]+1),overFrames=int(settings.render.timeToMove*settings.render.fps/3),itemCheck = False)
                cornered = 3
            else:
                pos = (self.pos[0]+spaces,self.pos[1])
        else:
            if self.pos[0] - spaces < 0:
                pos = (-self.pos[0]+spaces-1,self.pos[1]+1)
                self.move((0,self.pos[1]),overFrames=int(settings.render.timeToMove*settings.render.fps/3),itemCheck = False)
                self.move((0,self.pos[1]+1),overFrames=int(settings.render.timeToMove*settings.render.fps/3),itemCheck = False)
                cornered = 3
            else:
                pos = (self.pos[0]-spaces,self.pos[1])
        print("advancing to %s" % str(pos), "from %s" % str(self.pos))
        if cornered != 1:
            self.move(pos,overFrames=int(settings.render.timeToMove*settings.render.fps/cornered))
        else:
            self.move(pos)
        

class Dice(pygame.sprite.Sprite):
    
    def __init__(self,rect):
        self.rollCount = 0
        self.rect = rect
        
        self.rolling = False
        self.rollSpeed = 200
        self.roll = random.randint(0,len(images.dice)-1)
        
        self.image = images.diceStopping[self.roll]
    def draw(self,Surface):
        
        if self.rollCount >= self.rollSpeed and self.rollSpeed > 0:
            self.rollCount = 0
            
            prevRoll = self.roll
            while self.roll == prevRoll:
                self.roll = random.randint(0,len(images.dice)-1)
                
            if self.rollSpeed > 20:
                self.image = images.diceStopped[self.roll]
                self.rollSpeed = -1
                pygame.event.post(pygame.event.Event(pygame.USEREVENT,code=userevents.stopRolling))
                
            elif not self.rolling:
                self.rollSpeed *= 1.25
                self.image = images.diceStopping[self.roll]
            else:
                self.rollSpeed = 2
                self.image = images.dice[self.roll]
        
        self.rollCount += 1
        
        Surface.blit(self.image,self.rect)
    
    def toggle(self):
        self.rolling = not self.rolling
        self.rollSpeed = 2
    
    def startRoll(self):
        self.rolling = True
        self.rollSpeed = 2
    
    def stop(self,fullStop=False):
        self.rolling = False
        if fullStop:
            self.rollSpeed = -1

class Sign(pygame.sprite.Sprite):
    
    def __init__(self,timeout = -1,*groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.timeout = timeout
    
    def update(self, *args):
        self.timeout -= 1
        if self.timeout == 0:
            self.kill()
        
class Signs(pygame.sprite.Group):
    
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.signdict = {}
        self.renderDict = {}
    def createSign(self,text,font,name,bg = None, hidden = False, timeout=-1,rect=None, **kwargs):
        s = Sign(timeout,self)
        textRender = font.render(text,True,settings.colours.signs)
        s.image = pygame.Surface(textRender.get_rect().size,pygame.SRCALPHA,32)
        if bg is not None:
            s.image.fill(bg)
        s.image.blit(textRender,(0,0))
        s.name = name
        if rect is not None:
            s.rect = rect
        else:
            s.rect = s.image.get_rect(**kwargs)
        self.signdict[name] = s
        self.renderDict[name] = not bool(hidden)
    
    def hide(self,name):
        self.renderDict[name] = False
    
    def show(self,name):
        self.renderDict[name] = True
        
    def draw(self, surface):
        for spr in self.sprites():
            if self.renderDict[spr.name] is True:
                surface.blit(spr.image,spr.rect)
def tests():
    import time,random
    pygame.font.init()
    
    grid = Grid((10,10),(50,50),textOverlay=True)
    snakegrid = Grid(parent=grid, invisible=True,name = "snake")
    laddergrid = Grid(parent=grid, invisible=True, name = "ladder")
    playergrid = PlayerGrid(parent=grid, invisible=True, name = "player")
    
    Ladder(laddergrid,(1,1),(8,8))
    Snake(snakegrid,(1,2),(0,9))
    
    Player(playergrid,pos=(0,0))
    Player(playergrid,pos=(0,0)).move((1,1))
    Player(playergrid,pos=(0,0))
    Player(playergrid,pos=(0,0))
    Player(playergrid,pos=(0,0))
    Player(playergrid,pos=(0,0))
    Player(playergrid,pos=(0,0))
    Player(playergrid,pos=(0,0))
    Player(playergrid,pos=(0,0)).move((1,2))
    
    screen = pygame.display.set_mode(grid.rect.size)
    grid.draw(screen)
    snakegrid.draw(screen)
    laddergrid.draw(screen)
    playergrid.draw(screen)
    pygame.display.flip()
    time.sleep(10)
                

