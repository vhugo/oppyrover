import pygame

from lib.imageloader import imageLoader
from enum import Enum


class Direction(Enum):
    NORTH = ("n", "north", 0, -1)
    NORTHEAST = ("ne", "northeast", 1, -1)
    EAST = ("e", "east", 1, 0)
    SOUTHEAST = ("se", "southeast", 1, 1)
    SOUTH = ("s", "south", 0, 1)
    SOUTHWEST = ("sw", "southwest", -1, 1)
    WEST = ("w", "west", -1, 0)
    NORTHWEST = ("nw", "northwest", -1, -1)

    def __init__(self, shortname, fullname, x, y):
        self.shortname = shortname
        self.fullname = fullname
        self.x = x
        self.y = y

    @property
    def xy(self):
        return (self.x, self.y)


class Sprite(pygame.sprite.Sprite):

    def __init__(self, asset):
        self.sprite = []
        self.asset = asset
        self.loadSprite()

    def loadSprite(self):
        pass


class GameAsset(pygame.sprite.Sprite):

    def __init__(self, mmap, image, scale, area, bounds):
        self.image = self.asset = imageLoader(image, scale, area)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect()

        self.mmap = mmap

    def update(self):
        pass


class Rover(GameAsset):
    targetDistance = 0
    targetDirection = (0, 0)
    speed = 1

    def drive(self, distance, direction):
        self.targetDistance = self.mmap.tileSize[0] * distance
        self.targetDirection = direction

    def update(self):
        self.setMotion()

        # Continue update
        super().update()

    def setMotion(self):
        if self.targetDistance <= 0:
            return
        else:
            self.targetDistance -= self.speed

        x = 0
        y = 1

        direction = self.targetDirection
        travel = self.speed

        # map moviment
        vposx = self.mmap.viewPosition[x]
        vposy = self.mmap.viewPosition[y]
        if self.rect.x == 0 or self.rect.x == self.mmap.tileSize[x]:
            vposx = self.mmap.viewPosition[x] + (travel * direction[x])
            if vposx > self.mmap.mapSize[x]:
                vposx = self.mmap.mapSize[x]
            elif vposx < 0:
                vposx = 0

        if self.rect.y == 0 or self.rect.y == self.mmap.tileSize[y]:
            vposy = self.mmap.viewPosition[y] + (travel * direction[y])
            if vposy > self.mmap.mapSize[y]:
                vposy = self.mmap.mapSize[y]
            elif vposy < 0:
                vposy = 0

        self.mmap.viewPosition = (vposx, vposy)

        #  Rover moviment
        if self.mmap.viewPosition[x] == self.mmap.mapSize[x]:
            mxmapX = self.mmap.viewSize[x] - self.mmap.tileSize[x]
            roverX = self.rect.x + (travel * direction[x])

            if direction[x] > 0 and roverX > mxmapX:
                self.rect.x = mxmapX

            elif direction[x] < 0 and roverX < 0:
                self.rect.x = 0

            else:
                self.rect.x = roverX

            self.mmap.viewUpdate = True

        if self.mmap.viewPosition[y] == self.mmap.mapSize[y]:
            mxmapY = self.mmap.viewSize[y] - self.mmap.tileSize[y]
            roverY = self.rect.y + (travel * direction[y])

            if direction[y] > 0 and roverY > mxmapY:
                self.rect.y = mxmapY

            elif direction[y] < 0 and roverY < 0:
                self.rect.y = 0

            else:
                self.rect.y = roverY

            self.mmap.viewUpdate = True

        # print(
        #     "%5d:rect.x" % self.rect.x,
        #     "%5d:rect.y" % self.rect.y,
        #     "%5d:vposx" % vposx,
        #     "%5d:vposy" % vposy,
        #     "viewSize %5d:x %5d:y" % self.mmap.viewSize,
        #     "viewPosition: %5d:x %5d:y" % self.mmap.viewPosition,
        #     "mapSize: %5d:x %5d:y" % self.mmap.mapSize)

        # vposx = self.mmap.viewPosition[0]
        # vposy = self.mmap.viewPosition[1]

        # # map position
        # if controls[0] and self.mmap.viewPosition[1] > 0:
        #     vposy += self.mmap.tileSize[1] * -1

        # elif controls[2] and self.mmap.viewPosition[1] < self.mmap.mapSize[1]:
        #     vposy += self.mmap.tileSize[1]

        # elif controls[3] and self.mmap.viewPosition[0] > 0:
        #     vposx += self.mmap.tileSize[0] * -1

        # elif controls[1] and self.mmap.viewPosition[0] < self.mmap.mapSize[0]:
        #     vposx += self.mmap.tileSize[0]

        # print(
        #     "rectX: %5d" % self.rect.x,
        #     "viewSize: %5d" % self.mmap.viewSize[0],
        #     "viewPosition: %5d" % self.mmap.viewPosition[0],
        #     "mapSize: %5d" % self.mmap.mapSize[0])

        # print(
        #     "rect: %5d" % self.rect.y,
        #     "viewSize: %5d" % self.mmap.viewSize[1],
        #     "viewPosition: %5d" % self.mmap.viewPosition[1],
        #     "mapSize: %5d" % self.mmap.mapSize[1])

        # rover position
        # if controls[0] and \
        #         self.mmap.viewPosition[1] <= 0 and \
        #         self.rect.y >= self.mmap.tileSize[1]:
        #     self.rect.y += self.mmap.tileSize[1] * -1
        #     self.mmap.viewUpdate = True

        # elif controls[2] and \
        #         self.mmap.viewPosition[1] >= self.mmap.mapSize[1] and \
        #         self.rect.y <= (self.mmap.viewSize[1] - (self.mmap.tileSize[1] * 2)):
        #     self.rect.y += self.mmap.tileSize[1]
        #     self.mmap.viewUpdate = True

        # elif controls[3] and \
        #         self.mmap.viewPosition[0] <= 0 and \
        #         self.rect.x >= self.mmap.tileSize[0]:
        #     self.rect.x += self.mmap.tileSize[0] * -1
        #     self.mmap.viewUpdate = True

        # elif controls[1] and \
        #         self.mmap.viewPosition[0] >= self.mmap.mapSize[0] and \
        #         self.rect.x <= (self.mmap.viewSize[0] - (self.mmap.tileSize[0] * 2)):
        #     self.rect.x += self.mmap.tileSize[0]
        #     self.mmap.viewUpdate = True

        # self.mmap.viewPosition = (vposx, vposy)

    def setAngle(self, controls):
        # up
        if controls == (1, 0, 0, 0):
            self.angle = 0

        # right + up
        elif controls == (1, 1, 0, 0):
            self.angle = 315

        # right
        elif controls == (0, 1, 0, 0):
            self.angle = 270

        # right + down
        elif controls == (0, 1, 1, 0):
            self.angle = 225

        # down
        elif controls == (0, 0, 1, 0):
            self.angle = 180

        # left + down
        elif controls == (0, 0, 1, 1):
            self.angle = 135

        # left
        elif controls == (0, 0, 0, 1):
            self.angle = 90

        # left + up
        elif controls == (1, 0, 0, 1):
            self.angle = 45
