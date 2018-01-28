import pygame


class Map(pygame.sprite.Sprite):
    fullMap = """
ABCDEFGHIJKLMNOPQRSTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTSRQPONMLKJIHGFEDCBA
bX....................................................................B
c.X...................................................................C
d..X..................................................................D
e...X.................................................................E
f....X................................................................F
g.....X...............................................................G
h......X..............................................................H
i.......X.............................................................I
j........X............................................................J
k.........X...........................................................K
l..........X..........................................................L
m...........X.........................................................M
n............X........................................................N
o.............X.......................................................O
p..............X......................................................P
q...............X.....................................................Q
r................X....................................................R
s.................X...................................................S
t..................X..................................................T
t...................X.................................................T
s....................X................................................S
r.....................X...............................................R
q......................X..............................................Q
p.......................X.............................................P
o........................X............................................O
n.........................X...........................................N
m..........................X..........................................M
l...........................X.........................................L
k............................X........................................K
j.............................X.......................................J
i..............................X......................................I
h...............................X.....................................H
g................................X....................................G
f.................................X...................................F
e..................................X..................................E
d...................................X.................................D
c....................................X................................C
b.....................................X...............................B
a......................................X..............................A
a.......................................X.............................A
b........................................X............................B
c.........................................X...........................C
d..........................................X..........................D
e...........................................X.........................E
f............................................X........................F
g.............................................X.......................G
h..............................................X......................H
i...............................................X.....................I
j................................................X....................J
k.................................................X...................K
l..................................................X..................L
m...................................................X.................M
n....................................................X................N
o.....................................................X...............O
p......................................................X..............P
q.......................................................X.............Q
r........................................................X............R
s.........................................................X...........S
t..........................................................X..........T
t...........................................................X.........T
s............................................................X........S
r.............................................................X.......R
q..............................................................X......Q
p...............................................................X.....P
o................................................................X....O
n.................................................................X...N
m..................................................................X..M
l...................................................................X.L
k....................................................................XK
abcdefghijklmnopqrstttttttttttttttttttttttttttttttttsrqponmlkjihgfedcba
    """
    title = {
        ".": (100, 100, 100),
        "X": (255, 0, 0),
        "A": (0, 0, 10),
        "B": (0, 0, 20),
        "C": (0, 0, 30),
        "D": (0, 0, 40),
        "E": (0, 0, 50),
        "F": (0, 0, 60),
        "G": (0, 0, 70),
        "H": (0, 0, 80),
        "I": (0, 0, 90),
        "J": (0, 0, 100),
        "K": (0, 0, 110),
        "L": (0, 0, 120),
        "M": (0, 0, 130),
        "N": (0, 0, 140),
        "O": (0, 0, 150),
        "P": (0, 0, 160),
        "Q": (0, 0, 170),
        "R": (0, 0, 180),
        "S": (0, 0, 190),
        "T": (0, 0, 200),
        "a": (0, 10, 0),
        "b": (0, 20, 0),
        "c": (0, 30, 0),
        "d": (0, 40, 0),
        "e": (0, 50, 0),
        "f": (0, 60, 0),
        "g": (0, 70, 0),
        "h": (0, 80, 0),
        "i": (0, 90, 0),
        "j": (0, 100, 0),
        "k": (0, 110, 0),
        "l": (0, 120, 0),
        "m": (0, 130, 0),
        "n": (0, 140, 0),
        "o": (0, 150, 0),
        "p": (0, 160, 0),
        "q": (0, 170, 0),
        "r": (0, 180, 0),
        "s": (0, 190, 0),
        "t": (0, 200, 0),
    }

    def __init__(self, viewSize, tileSize):
        self.mapArray = []
        self.mapSize = (0, 0)
        self.tileSize = tileSize
        self.viewSize = viewSize
        self.currentViewPosition = (0, 0)
        self.viewPosition = (0, 0)
        self.viewUpdate = False
        self.loadMap()

    def loadMap(self):
        mapYs = [m for m in self.fullMap.split("\n")[:-1]]
        self.mapArray = [[my for my in m] for m in mapYs[1:]]

        fullMapHeight = self.tileSize[1] * len(mapYs[1:])
        fullMapWidth = self.tileSize[0] * len(self.mapArray[0])

        # We need only what we can fit on the screen
        mapWidth = fullMapWidth - self.viewSize[0]
        mapHeight = fullMapHeight - self.viewSize[1]
        self.mapSize = (mapWidth, mapHeight)

    def updated(self):
        return (self.currentViewPosition[0] != self.viewPosition[0] or
                self.currentViewPosition[1] != self.viewPosition[1] or
                self.viewUpdate)

    def drawMap(self):
        self.reset()
        mapSurface = pygame.Surface(self.viewSize)

        viewX = int(self.viewPosition[0] / self.tileSize[0])
        viewY = int(self.viewPosition[1] / self.tileSize[1])

        for yidx, xmap in enumerate(self.mapArray[viewY:]):
            yidx += viewY
            moveY = (self.tileSize[1] * yidx) - self.viewPosition[1]

            for xidx, xym in enumerate(xmap[viewX:]):
                xidx += viewX
                moveX = (self.tileSize[0] * xidx) - self.viewPosition[0]

                terrain = pygame.Rect(
                    moveX, moveY, self.tileSize[0], self.tileSize[1])

                pygame.draw.rect(mapSurface, self.title[xym], terrain)

                if moveX >= self.viewSize[0] and moveY >= self.viewSize[1]:
                    return mapSurface

        return mapSurface

    def reset(self):
        self.viewUpdate = 0
        self.currentViewPosition = self.viewPosition