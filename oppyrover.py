import sys
import pygame

from lib.gameobjects import Rover
from lib.terminal import Terminal
from lib.map import Map
from pygame import QUIT

pygame.init()

# Dimensions
w = 800
h = 600

# Configuration
framerate = 60
screenSize = (w, h)
tileSize = (23, 23)

# Setup
screen = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()

# Game objects
gameObjects = []

# load map
mmap = Map(screenSize, tileSize)

# load rover
player = Rover(mmap, "images/player.bmp", 1, (25, 1, 23, 23), (w, h))
gameObjects.append(player)

# load terminal
terminal = Terminal(80, 6, player)
terminal.rect.x = 0  # screenSize[0] - terminal.image.get_width()
terminal.rect.y = screenSize[1] - terminal.image.get_height()
gameObjects.append(terminal)

# draw map
mapSize = (screenSize[0], screenSize[1] - terminal.image.get_height())
mmap.viewSize = mapSize
screen.blit(mmap.drawMap(), (0, 0))

cycle = 0
running = True
while running:

    if mmap.updated():
        screen.blit(mmap.drawMap(), (0, 0))

    for idx, gameObj in enumerate(gameObjects):
        gameObj.update()
        screen.blit(gameObj.image, (gameObj.rect.x, gameObj.rect.y))

    cycle += 1

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    pygame.display.flip()
    clock.tick(framerate)
