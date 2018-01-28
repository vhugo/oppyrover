import pygame


def imageLoader(image, scale, area):
    asset = pygame.image.load(image)
    clipped = pygame.Surface(area[2:])
    clipped.blit(asset, (0, 0), area)
    scaledClipArea = (area[2] * scale, area[3] * scale)
    return pygame.transform.scale(clipped, scaledClipArea)
