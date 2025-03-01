import pygame
from Config import *

class Background():
    def __init__(self):
        self.skyImage = pygame.image.load(BACKGROUND_PATH + "Night Background.png").convert()
        self.skyImage = pygame.transform.scale(self.skyImage, (WINDOW_WIDTH, WINDOW_HEIGHT))


    def draw(self, displaySurface):
        displaySurface.blit(self.skyImage, (0, 0))
