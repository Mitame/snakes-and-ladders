from pygame import Color
class colours():
#     grid1 = (62,122,171)
#     grid2 = (175,175,175)
    grid1 = Color("#00aa88ff")
    grid2 = Color("#87decdff")
#     textOverlay1 = Color(120,120,120,150)
#     textOverlay2 = Color(120,120,120,150)
    textOverlay1 = Color("#87decdff")
    textOverlay2 = Color("#00aa88ff")
    signs = Color("#ffffffff")
    signBG = Color("#00000088")

class grid():
    flipVertical = True
    zeroBased = True
    size = (10,10)
    squareSize = (50,50)

class gameplay():
    players = 4
    snakes = 5
    ladders = 6
    minLadderDist = 10
    maxLadderDist = 30
    minSnakeDist = 5
    maxSnakeDist = 30
    itemBuffer = 5

class render():
    fps = 30
    timeToMove = 2
    minLadderWidth = 20
    minSnakeWidth = 10
    dicePauseTime = 2
    sysfont = "Ubuntu"
    
