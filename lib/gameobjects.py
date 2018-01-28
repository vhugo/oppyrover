import pygame

from lib.imageloader import imageLoader


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

    def update(self):
        # Process player Input
        # controls = self.getPlayerInput()
        # self.setMotion(controls)
        # self.setAngle(controls)

        # Continue update
        super().update()

    def getPlayerInput(self):
        pass
        # up = pygame.key.get_pressed()[pygame.K_UP]
        # right = pygame.key.get_pressed()[pygame.K_RIGHT]
        # down = pygame.key.get_pressed()[pygame.K_DOWN]
        # left = pygame.key.get_pressed()[pygame.K_LEFT]
        # return (up, right, down, left)

    def setMotion(self, controls):
        vposx = self.mmap.viewPosition[0]
        vposy = self.mmap.viewPosition[1]

        # map position
        if controls[0] and self.mmap.viewPosition[1] > 0:
            vposy += self.mmap.tileSize[1] * -1

        elif controls[2] and self.mmap.viewPosition[1] < self.mmap.mapSize[1]:
            vposy += self.mmap.tileSize[1]

        elif controls[3] and self.mmap.viewPosition[0] > 0:
            vposx += self.mmap.tileSize[0] * -1

        elif controls[1] and self.mmap.viewPosition[0] < self.mmap.mapSize[0]:
            vposx += self.mmap.tileSize[0]

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
        if controls[0] and \
                self.mmap.viewPosition[1] <= 0 and \
                self.rect.y >= self.mmap.tileSize[1]:
            self.rect.y += self.mmap.tileSize[1] * -1
            self.mmap.viewUpdate = True

        elif controls[2] and \
                self.mmap.viewPosition[1] >= self.mmap.mapSize[1] and \
                self.rect.y <= (self.mmap.viewSize[1] - (self.mmap.tileSize[1] * 2)):
            self.rect.y += self.mmap.tileSize[1]
            self.mmap.viewUpdate = True

        elif controls[3] and \
                self.mmap.viewPosition[0] <= 0 and \
                self.rect.x >= self.mmap.tileSize[0]:
            self.rect.x += self.mmap.tileSize[0] * -1
            self.mmap.viewUpdate = True

        elif controls[1] and \
                self.mmap.viewPosition[0] >= self.mmap.mapSize[0] and \
                self.rect.x <= (self.mmap.viewSize[0] - (self.mmap.tileSize[0] * 2)):
            self.rect.x += self.mmap.tileSize[0]
            self.mmap.viewUpdate = True

        self.mmap.viewPosition = (vposx, vposy)

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
