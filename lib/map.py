import pygame
from random import shuffle, randrange
class MapGrid():

    def __init__(self, mapSize, tileSize, columns, rows):
        self.image = self.asset = pygame.Surface(mapSize)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        # self.image.set_alpha(90)

        white = (255, 255, 255)
        x, y = (0, 1)
        for xidx in range(columns):
            pygame.draw.line(
                self.image,
                white,
                ((tileSize[x] * xidx), 0),
                ((tileSize[y] * xidx), mapSize[y]))

        for yidx in range(rows):
            pygame.draw.line(
                self.image,
                white,
                (0, (tileSize[y] * yidx)),
                (mapSize[x], (tileSize[x] * yidx)))


class Map(pygame.sprite.Sprite):
    title = {
        ".": (255, 188, 108),
        "X": (252, 141, 0),
    }

    def __init__(self, viewSize, tileSize):
        self.mapArray = []
        self.mapSize = (0, 0)
        self.tileSize = tileSize
        self.viewSize = viewSize
        self.currentViewPosition = (0, 0)
        self.viewPosition = (0, 0)
        self.viewUpdate = False
        self.generateMazeMap()
        self.loadMap()

    def generateMazeMap(self):
        w = 5
        h = 15
        vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
        ver = [["X......"] * w + ['X'] for _ in range(h)] + [[]]
        hor = [["XXXXXXX"] * w + ['X'] for _ in range(h + 1)]

        def walk(x, y):
            vis[y][x] = 1

            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(d)
            for (xx, yy) in d:
                if vis[yy][xx]:
                    continue
                if xx == x:
                    hor[max(y, yy)][x] = "X......"
                if yy == y:
                    ver[y][max(x, xx)] = "......."
                walk(xx, yy)

        walk(randrange(w), randrange(h))

        s = "\n"
        for (a, b) in zip(hor, ver):
            s += ''.join(
                a + ['\n'] +
                b + ['\n'] +
                b + ['\n'] +
                b + ['\n'] +
                b + ['\n'] +
                b + ['\n'] +
                b + ['\n'] +
                b + ['\n'])
        self.fullMap = s

    def loadMap(self):
        x = 0
        y = 1
        mapYs = [m for m in self.fullMap.split("\n")[:-1]]
        self.mapArray = [[my for my in m] for m in mapYs[1:]]

        fullMapWidth = self.tileSize[x] * len(self.mapArray[0])
        fullMapHeight = self.tileSize[y] * len(mapYs[1:])
        self.fullMapSize = (fullMapWidth, fullMapHeight)

        # We need only what we can fit on the screen
        mapWidth = self.fullMapSize[x] - self.viewSize[x]
        mapHeight = self.fullMapSize[y] - self.viewSize[y]
        self.mapSize = (mapWidth, mapHeight)

    def setViewSize(self, viewSize):
        x = 0
        y = 1
        mapWidth = self.fullMapSize[x] - viewSize[x]
        mapHeight = self.fullMapSize[y] - viewSize[y]
        self.viewSize = viewSize
        self.mapSize = (mapWidth, mapHeight)

    def updated(self):
        x = 0
        y = 1
        return (self.currentViewPosition[x] != self.viewPosition[x] or
                self.currentViewPosition[y] != self.viewPosition[y] or
                self.viewUpdate)

    def drawMinimap(self):
        self.miniMapView = (72, 242)
        mapSurface = pygame.Surface(self.miniMapView)

        for yidx, xmap in enumerate(self.mapArray):
            moveY = (2 * yidx)

            for xidx, xym in enumerate(xmap):
                moveX = (2 * xidx)

                terrain = pygame.Rect(
                    moveX, moveY, 2, 2)

                pygame.draw.rect(mapSurface, self.title[xym], terrain)

                if moveX >= self.viewSize[0] and moveY >= self.viewSize[1]:
                    return mapSurface

        for yidx, xmap in enumerate(self.mapArray):
            for xidx, xym in enumerate(xmap):
                terrain = pygame.Rect(0, 0, 2, 2)

                pygame.draw.rect(mapSurface, self.title[xym], terrain)

        return mapSurface

    def drawMap(self):
        x = 0
        y = 1
        self.reset()
        mapSurface = pygame.Surface(self.viewSize)

        viewX = int(self.viewPosition[x] / self.tileSize[x])
        viewY = int(self.viewPosition[y] / self.tileSize[y])

        for yidx, xmap in enumerate(self.mapArray[viewY:]):
            yidx += viewY
            moveY = (self.tileSize[y] * yidx) - self.viewPosition[y]

            for xidx, xym in enumerate(xmap[viewX:]):
                xidx += viewX
                moveX = (self.tileSize[x] * xidx) - self.viewPosition[x]

                terrain = pygame.Rect(
                    moveX, moveY, self.tileSize[x], self.tileSize[y])

                pygame.draw.rect(mapSurface, self.title[xym], terrain)

                if moveX >= self.viewSize[x] and moveY >= self.viewSize[y]:
                    return mapSurface

        return mapSurface

    def reset(self):
        self.viewUpdate = False
        self.currentViewPosition = self.viewPosition
