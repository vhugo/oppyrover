import sys
import pygame
import time

from lib.gameobjects import Rover
from lib.terminal import Terminal
from lib.map import Map, MapGrid
from pygame import QUIT

pygame.init()

# Configuration
x, y = (0, 1)
framerate = 60
screenSize = (800, 600)
tileSize = (23, 23)
terminalSize = (80, 6)  # columns and lines

# Setup
screen = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()

# Game objects
gameObjects = []

# load map
gmap = Map(screenSize, tileSize)

# load rover
player = Rover(gmap)
player.rect.x = tileSize[x]
player.rect.y = tileSize[y]
gameObjects.append(player)

# load terminal
terminal = Terminal(terminalSize[x], terminalSize[y], player)
terminal.rect.x = 0  # screenSize[x] - terminal.image.get_width()
terminal.rect.y = screenSize[y] - terminal.image.get_height()
gameObjects.append(terminal)

# measurements before render
mapSize = (  # (screenSize[x] - gmap.minimapView[x]),
    screenSize[x],
    (screenSize[y] - terminal.image.get_height()))
gmap.setViewSize(mapSize)
mapGrid = MapGrid(mapSize, tileSize, 35, 21)
mmapPos = (screenSize[x] - gmap.minimapView[x], 0)

# Render map, grid and minimap
# screen.blit(gmap.drawMap(), (0, 0))
# screen.blit(mapGrid.image, (0, 0))
# screen.blit(gmap.minimap, mmapPos)

running = True
while running:

    start = time.time()

    if gmap.updated():
        # print("Map")
        screen.blit(gmap.map, (0, 0))
        gadgetUpdated = True
        gmap.onUpdate()

    for idx, gameObj in enumerate(gameObjects):
        gameObj.update()
        if gameObj.updated or gadgetUpdated:
            screen.blit(gameObj.image, (gameObj.rect.x, gameObj.rect.y))
            pygame.display.update(gameObj.rect)
            gameObj.updated = False

    if gadgetUpdated:
        # print("Grid and Minimap")
        screen.blit(mapGrid.image, (0, 0))
        screen.blit(gmap.minimap, mmapPos)
        gadgetUpdated = False
        pygame.display.flip()

    end = time.time()
    elapse = (end - start) * 1000

    # if elapse > 1.0:
    #     print(
    #         "elapse: %10f - time: %10f - rawtime: %10f - fps: %10f" %
    #         (elapse, clock.get_rawtime(), clock.get_time(), clock.get_fps()))

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    clock.tick(framerate)
