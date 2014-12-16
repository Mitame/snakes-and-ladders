import pygame.image, pygame.transform
import os
print("CURRENT DIRECTORY:",os.path.abspath("."))
baseDir = "./data/images/"

def crop(surface,area):
    if type(area) == pygame.Rect:
        newSurf = pygame.Surface(area.size,pygame.SRCALPHA,surface.get_bitsize())
    else:
        newSurf = pygame.Surface(area[2:4],pygame.SRCALPHA,surface.get_bitsize())
    newSurf.blit(surface,(0,0),area)
    return newSurf

class raw():
    snake = pygame.image.load(baseDir+"snake1.png")
    ladder = pygame.transform.smoothscale(pygame.image.load(baseDir+"ladder.png"),(50,800))
    players = pygame.image.load(baseDir+"players.png")
    dice = pygame.image.load(baseDir+"dice.png")
    icon = pygame.image.load(baseDir+"icon.png")

players = {"size1":[crop(raw.players,(0,0,50,50)),
           crop(raw.players,(50,0,50,50)),
           crop(raw.players,(100,0,50,50)),
           crop(raw.players,(0,50,50,50)),
           crop(raw.players,(50,50,50,50)),
           crop(raw.players,(100,50,50,50)),
           crop(raw.players,(0,100,50,50)),
           crop(raw.players,(50,100,50,50)),
           crop(raw.players,(100,100,50,50))],
           "size2":[],
           "size3":[]}
for i in range(9):
    players["size2"].append(pygame.transform.smoothscale(players["size1"][i],tuple(players["size1"][i].get_size()[i]//2 for i in range(2))))
    players["size3"].append(pygame.transform.smoothscale(players["size1"][i],tuple(players["size1"][i].get_size()[i]//3 for i in range(2))))


diceSize = (150,150)
dice = [crop(raw.dice,(0,0,50,50)),
        crop(raw.dice,(50,0,50,50)),
        crop(raw.dice,(100,0,50,50)),
        crop(raw.dice,(0,50,50,50)),
        crop(raw.dice,(50,50,50,50)),
        crop(raw.dice,(100,50,50,50)),
        ]
diceStopping = [crop(raw.dice,(0,100,50,50)),
                crop(raw.dice,(50,100,50,50)),
                crop(raw.dice,(100,100,50,50)),
                crop(raw.dice,(0,150,50,50)),
                crop(raw.dice,(50,150,50,50)),
                crop(raw.dice,(100,150,50,50)),
                ]
diceStopped = [crop(raw.dice,(0,200,50,50)),
               crop(raw.dice,(50,200,50,50)),
               crop(raw.dice,(100,200,50,50)),
               crop(raw.dice,(0,250,50,50)),
               crop(raw.dice,(50,250,50,50)),
               crop(raw.dice,(100,250,50,50)),
               ]
def tests():
    import time
    screen = pygame.display.set_mode(players["size1"][0].get_size())    
    for i in range(len(players["size1"])):
        screen.fill((255,255,255))
        screen.blit(players["size1"][i],(0,0))
        pygame.display.flip()
        time.sleep(1)
    
    for i in range(len(players["size2"])):
        screen.fill((255,255,255))
        screen.blit(players["size2"][i],(0,0))
        pygame.display.flip()
        time.sleep(1)
        
    for i in range(len(players["size2"])):
        screen.fill((255,255,255))
        screen.blit(players["size2"][i],(0,0))
        pygame.display.flip()
        time.sleep(1)
        
if __name__ == "__main__": tests()