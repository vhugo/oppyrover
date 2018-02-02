import pygame
import re

from random import shuffle, randrange
from lib.imageloader import imageLoader


class MapBlock():

    def __init__(self, image):
        self.image = self.asset = image
        self.rect = image.get_rect()


class MapBlockImage(MapBlock):

    def __init__(self, image, scale, area):
        image = imageLoader(image, scale, area)
        image.set_colorkey(self.image.get_at((0, 0)))
        super().__init__(image)


class MapBlockColor(MapBlock):

    def __init__(self, color, tileSize):
        surface = pygame.Surface(tileSize)
        surface.fill(color)
        super().__init__(surface)


class MapGrid():

    def __init__(self, mapSize, tileSize, columns, rows):
        self.image = self.asset = pygame.Surface(mapSize)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.image.set_alpha(60)

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

    def __init__(self, viewSize, tileSize):
        self.map = None
        self.minimap = None
        self.minimapTile = (2, 2)
        self.mapArray = []
        self.mapArrayAsset = []
        self.mapSize = (0, 0)
        self.tileSize = tileSize
        self.viewSize = viewSize
        self.currentViewPosition = (0, 0)
        self.viewPosition = (0, 0)
        self.viewUpdate = True

        self.minitile = {
            ".": MapBlockColor((255, 188, 108), self.minimapTile),
            "a": MapBlockColor((30, 40, 32), self.minimapTile),
            "b": MapBlockColor((60, 141, 90), self.minimapTile),
            "c": MapBlockColor((97, 162, 107), self.minimapTile),
        }
        self.tile = {
            '.': MapBlockColor((231, 212, 169), self.tileSize),
            'a': MapBlockColor((30, 40, 32), self.tileSize),
            'b': MapBlockColor((60, 141, 90), self.tileSize),
            'c': MapBlockColor((97, 162, 107), self.tileSize),
            # "X": MapBlockImage("images/ground.png", 1, (23 * 2, 23 * 1, 23, 23)),
        }

        self.generateMazeMap()
        self.loadMap()

    def generateMazeMap(self):
        w, h = (5, 15)
        vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
        ver = [["abc      "] * w + ['c'] for _ in range(h)] + [[]]
        hor = [["cbaaaaabc"] * w + ['c'] for _ in range(h + 1)]

        def walk(x, y):
            vis[y][x] = 1

            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(d)
            for (xx, yy) in d:
                if vis[yy][xx]:
                    continue
                if xx == x:
                    hor[max(y, yy)][x] = "abc      "
                if yy == y:
                    ver[y][max(x, xx)] = "         "
                walk(xx, yy)

        walk(randrange(w), randrange(h))

        s = "\n"
        for (a, b) in zip(hor, ver):

            # walls = a
            # re.sub(r'X(X+)X', repl, string)
            section = ''.join(
                a + ['\n'] +
                b + ['\n'] +
                b + ['\n'] +
                b + ['\n'] +
                b + ['\n'] +
                b + ['\n'] +
                b + ['\n'])

            s += section

        print("block: \n", s)
        self.fullMap = s

    def loadMap(self):
        x, y = (0, 1)
        mapYs = [m for m in self.fullMap.split("\n")[:-1]]
        self.mapArray = [[my for my in m] for m in mapYs[1:]]
        self.minimapView = (
            self.minimapTile[x] * len(self.mapArray[0]),
            self.minimapTile[y] * (len(self.mapArray) - 6))  # magic num :-P

        fullMapWidth = self.tileSize[x] * len(self.mapArray[0])
        fullMapHeight = self.tileSize[y] * len(self.mapArray)
        self.fullMapSize = (fullMapWidth, fullMapHeight)

        # We need only what we can fit on the screen
        mapWidth = self.fullMapSize[x] - self.viewSize[x]
        mapHeight = self.fullMapSize[y] - self.viewSize[y]
        self.mapSize = (mapWidth, mapHeight)
        self.loadMinimap()
        self.drawMap()

    def setViewSize(self, viewSize):
        x, y = (0, 1)
        mapWidth = self.fullMapSize[x] - viewSize[x]
        mapHeight = self.fullMapSize[y] - viewSize[y]
        self.viewSize = viewSize
        self.mapSize = (mapWidth, mapHeight)

    def updated(self):
        x, y = (0, 1)
        return (self.currentViewPosition[x] != self.viewPosition[x] or
                self.currentViewPosition[y] != self.viewPosition[y] or
                self.viewUpdate)

    def loadMinimap(self):
        x, y = (0, 1)
        # self.minimapView = (72, 242)
        # self.miniMapTile = (2, 2)
        self.minimap = pygame.Surface(self.minimapView)
        self.minimap.fill((231, 212, 169))
        # self.minimap.set_colorkey((0, 0, 0))

        for yidx, xmap in enumerate(self.mapArray):
            moveY = (self.minimapTile[y] * yidx)

            for xidx, xym in enumerate(xmap):
                moveX = (self.minimapTile[x] * xidx)
                if xym is not " ":
                    self.minimap.blit(self.minitile[xym].image, (moveX, moveY))

    def drawMap(self):
        x, y = (0, 1)
        self.map = pygame.Surface(self.viewSize)
        self.map.fill((231, 212, 169))

        viewX = int(self.viewPosition[x] / self.tileSize[x])
        viewY = int(self.viewPosition[y] / self.tileSize[y])

        for yidx, xmap in enumerate(self.mapArray[viewY:]):
            yidx += viewY
            moveY = (self.tileSize[y] * yidx) - self.viewPosition[y]

            for xidx, xym in enumerate(xmap[viewX:]):
                xidx += viewX
                moveX = (self.tileSize[x] * xidx) - self.viewPosition[x]
                if xym is not " ":
                    self.map.blit(self.tile[xym].image, (moveX, moveY))

                if moveX >= self.viewSize[x] and moveY >= self.viewSize[y]:
                    return

    def refresh(self):
        self.viewUpdate = True
        self.drawMap()

    def onUpdate(self):
        self.viewUpdate = False
        self.currentViewPosition = self.viewPosition
