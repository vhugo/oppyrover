import pygame

from lib.imageloader import imageLoader
from enum import Enum


class Direction(Enum):
    NORTH = ("n", "north", 0, -1, 0)
    NORTHEAST = ("ne", "northeast", 1, -1, 315)
    EAST = ("e", "east", 1, 0, 270)
    SOUTHEAST = ("se", "southeast", 1, 1, 225)
    SOUTH = ("s", "south", 0, 1, 180)
    SOUTHWEST = ("sw", "southwest", -1, 1, 135)
    WEST = ("w", "west", -1, 0, 90)
    NORTHWEST = ("nw", "northwest", -1, -1, 45)

    def __init__(self, shortname, fullname, x, y, angle):
        self.shortname = shortname
        self.fullname = fullname
        self.x = x
        self.y = y
        self.angle = angle

    @property
    def xy(self):
        return (self.x, self.y)


class Sprite(pygame.sprite.Sprite):

    def __init__(self, asset):
        self.sprite = []
        self.asset = asset
        self.updated = True
        self.loadSprite()

    def loadSprite(self):
        pass


class GameAsset(pygame.sprite.Sprite):

    def __init__(self, gmap, image, scale, area):
        self.gmap = gmap
        self.updated = True
        self.image = self.asset = imageLoader(image, scale, area)
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect()
        self.collision = False

    def update(self):
        pass


class Rover(GameAsset):
    targetDistance = 0
    targetDirection = (0, 0)
    speed = 3

    def __init__(self, gmap):
        super().__init__(gmap, "images/player.bmp", 1, (25, 1, 23, 23))

    def drive(self, distance, direction):
        self.targetDistance = self.gmap.tileSize[0] * distance
        self.targetDirection = direction

    def update(self):
        self.checkForCollisions()

        if not self.collision:
            self.setMotion()

        # Continue update
        super().update()

    def setMotion(self):
        if self.targetDistance <= 0:
            return
        else:
            self.targetDistance -= self.speed
            self.updated = True
            self.gmap.refresh()

        x, y = (0, 1)
        direction = self.targetDirection
        travel = self.speed
        bounds = (self.gmap.tileSize[x] * 3, self.gmap.tileSize[y])
        mapmoved = True

        # map moviment
        vposx = self.gmap.viewPosition[x]
        vposy = self.gmap.viewPosition[y]
        halfwayx = (self.gmap.viewSize[x] / 2)
        halfwayy = (self.gmap.viewSize[y] / 2)
        if self.rect.x > halfwayx:
            vposx = self.gmap.viewPosition[x] + (travel * direction[x])
            if vposx > self.gmap.mapSize[x]:
                vposx = self.gmap.mapSize[x]
            # elif vposx > 0 and vposx <= self.gmap.tileSize[x]:
            #     vposx = self.gmap.tileSize[x]
            elif vposx < 0:
                vposx = 0

        if self.rect.y > halfwayy:
            vposy = self.gmap.viewPosition[y] + (travel * direction[y])
            if vposy > self.gmap.mapSize[y]:
                vposy = self.gmap.mapSize[y]
            # elif vposy > 0 and vposy <= self.gmap.tileSize[y]:
            #     vposy = self.gmap.tileSize[y]
            elif vposy < 0:
                vposy = 0

        if (vposx, vposy) != self.gmap.viewPosition:
            self.gmap.viewPosition = (vposx, vposy)
        else:
            mapmoved = False

        #  Rover moviment
        rectx = self.rect.x
        recty = self.rect.y
        if rectx <= halfwayx or \
                self.gmap.viewPosition[x] == self.gmap.mapSize[x]:
            mxmapX = self.gmap.viewSize[x] - bounds[x]
            roverX = rectx + (travel * direction[x])

            if direction[x] > 0 and roverX > mxmapX:
                rectx = mxmapX

            elif direction[x] < 0 and roverX < 0:
                rectx = 0

            else:
                rectx = roverX

        if recty <= halfwayy or \
                self.gmap.viewPosition[y] == self.gmap.mapSize[x]:
            mxmapY = self.gmap.viewSize[y] - bounds[y]
            roverY = recty + (travel * direction[y])

            if direction[y] > 0 and roverY > mxmapY:
                recty = mxmapY

            elif direction[y] < 0 and roverY < 0:
                recty = 0

            else:
                recty = roverY

        if (rectx, recty) != (self.rect.x, self.rect.y):
            self.rect.x = rectx
            self.rect.y = recty
        elif not mapmoved:
            self.targetDistance = 0

        print(
            "%5d:target" % self.targetDistance,
            "%5d:rect.x" % self.rect.x,
            "%5d:rect.y" % self.rect.y,
            "%5d:vposx" % vposx,
            "%5d:vposy" % vposy,
            "viewSize %5d:x %5d:y" % self.gmap.viewSize,
            "viewPosition: %5d:x %5d:y" % self.gmap.viewPosition,
            "mapSize: %5d:x %5d:y" % self.gmap.mapSize)

    def checkForCollisions(self):
        pass
        # for idx, mpoint in enumerate(self.gmap.mapArray):

        #     if mpoint != ".":
        #         self.collision = self.rect.colliderect(asset.rect)
        #         print("COLLISION", self.collisionCause.__class__.__name__)
        #         self.collision = True
        #         break

        # for asset in self.collisionGroup:
        #     self.collision = self.rect.colliderect(asset.rect)
        #     if self.collision:
        #         self.collisionCause = asset
        #         print("COLLISION", self.collisionCause.__class__.__name__)
        #         self.onCollision()
        #         break

    def restart(self):
        self.targetDistance = 0
        self.gmap.__init__(self.gmap.viewSize, self.gmap.tileSize)
        self.gmap.viewUpdate = True
