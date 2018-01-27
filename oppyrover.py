import sys
import pygame

from lib.map import Map
from pygame import QUIT

# Dimensions
w = 800
h = 600

# Configuration
framerate = 60
screenSize = (w, h)
tileSize = (80, 80)

# Setup
screen = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()

# load map
mmap = Map(screenSize, tileSize)
screen.blit(mmap.drawMap(), (0, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    up = pygame.key.get_pressed()[pygame.K_UP]
    right = pygame.key.get_pressed()[pygame.K_RIGHT]
    down = pygame.key.get_pressed()[pygame.K_DOWN]
    left = pygame.key.get_pressed()[pygame.K_LEFT]

    vposx = mmap.viewPosition[0]
    vposy = mmap.viewPosition[1]
    if up and mmap.viewPosition[1] > 0:
        vposy += tileSize[1] * -1
    if down and mmap.viewPosition[1] < mmap.mapSize[1]:
        vposy += tileSize[1] * 1
    if left and mmap.viewPosition[0] > 0:
        vposx += tileSize[0] * -1
    if right and mmap.viewPosition[0] < mmap.mapSize[0]:
        vposx += tileSize[0] * 1

    mmap.viewPosition = (vposx, vposy)

    if mmap.isUpdated():
        screen.blit(mmap.drawMap(), (0, 0))

    pygame.display.flip()
    clock.tick(framerate)
