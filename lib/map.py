import pygame


class Map(pygame.sprite.Sprite):
    # 20x20 - Maps will need to be draw as a square
    fullMap = """
ABCDEFGHIJKLMNOPQRST.X.X.X.X.XA
b...X....X....X....A..........B
c.............................C
d.............................D
e.............................E
f.............................F
g.............................G
h.............................H
i.............................I
j.............................J
k.............................K
l.............................L
m.............................M
n.............................N
o.............................O
p.............................P
q.............................Q
r.............................R
s.............................S
t.............................T
    """
    title = {
        ".": (255, 255, 0),
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

    def isUpdated(self):
        return (self.currentViewPosition[0] != self.viewPosition[0] or
                self.currentViewPosition[1] != self.viewPosition[1])

    def drawMap(self):

        recalibratePositionX = self.viewPosition[0]
        if recalibratePositionX > self.mapSize[0]:
            recalibratePositionX = self.mapSize[0]
        elif recalibratePositionX < 0:
            recalibratePositionX = 0

        recalibratePositionY = self.viewPosition[1]
        if recalibratePositionY > self.mapSize[1]:
            recalibratePositionY = self.mapSize[1]
        elif recalibratePositionY < 0:
            recalibratePositionY = 0

        self.viewPosition = (recalibratePositionX, recalibratePositionY)

        self.currentViewPosition = self.viewPosition
        mapSurface = pygame.Surface(self.viewSize)

        viewX = int(self.viewPosition[0] / self.tileSize[0])
        viewY = int(self.viewPosition[1] / self.tileSize[1])

        # print("X: %5d" % viewX, "Y: %5d" % viewY)

        for yidx, xmap in enumerate(self.mapArray[viewY:]):
            yidx += viewY
            moveY = (self.tileSize[1] * yidx) - self.viewPosition[1]

            # print(
            #     "MOVY: %5d" % moveY,
            #     "MAPY: %5d" % self.mapSize[1],
            #     "VPOY: %5d" % self.viewPosition[1]
            # )

            for xidx, xym in enumerate(xmap[viewX:]):
                xidx += viewX
                moveX = (self.tileSize[0] * xidx) - self.viewPosition[0]

                # print(
                #     "MOVX: %5d" % moveX,
                #     "MAPX: %5d" % self.mapSize[0],
                #     "VPOX: %5d" % self.viewPosition[0]
                # )

                # print("X: %5d" % xidx, "Y: %5d" % yidx)
                # print("X: %5d" % moveX, "Y: %5d" % moveY)

                terrain = pygame.Rect(
                    moveX, moveY, self.tileSize[0], self.tileSize[1])

                pygame.draw.rect(mapSurface, self.title[xym], terrain)

                if moveX >= self.viewSize[0] and moveY >= self.viewSize[1]:
                    return mapSurface

        return mapSurface

    # def isOufOfBoundary(self, move):
