import pygame
from pygame import mixer
from pytmx.util_pygame import load_pygame
from Config import *
from ClassBee import Bee
from ClassHero import Hero
from ClassTile import Tile
from ClassBackground import Background

class Level():
    def __init__(self, displaySurface):
        # Load the level tmx file
        # self.levelData = load_pygame(LEVELS_PATH + "Level1/level.tmx")
        self.levelData = load_pygame(LEVELS_PATH + "Level1/nightLevel.tmx")

        # Camera scroll effect
        self.cameraOffsetX = 0
        self.scrollThreshold = WINDOW_WIDTH // 2

        # Zoom effect variables
        self.zoom_factor = 2.5      # Start with a high zoom level
        self.zoom_speed = 0.002     # How quickly the zoom out happens
        self.target_zoom = 1.0      # The normal zoom level
        self.zooming = True         # Flag to control zoom animation

        # Create a camera surface for scaling
        self.camera_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

        #Instantiate classes
        self.background = Background()

        # Create spriteGroups
        self.hero = pygame.sprite.GroupSingle()
        self.bees = pygame.sprite.Group()
        self.platformTiles = pygame.sprite.Group()
        # self.foregroundTiles = pygame.sprite.Group()  # Foreground layer
        self.bg1 = pygame.sprite.Group()        # Background 1
        # self.bg2 = pygame.sprite.Group()        # Background 1
        # self.bg3 = pygame.sprite.Group()        # Background 1
        # self.bg4 = pygame.sprite.Group()        # Background 1

        # LOADING LAYERS
        layer = self.levelData.get_layer_by_name('Platforms')
        for x, y, tileSurface in layer.tiles():
            tile = Tile((x*TILESIZE, y*TILESIZE), tileSurface)
            self.platformTiles.add(tile)

        # layer = self.levelData.get_layer_by_name('Foreground')
        # for x, y, tileSurface in layer.tiles():
        #     tile = Tile((x*TILESIZE, y*TILESIZE), tileSurface)
        #     self.foregroundTiles.add(tile)
# 
        layer = self.levelData.get_layer_by_name('Background1')
        for x, y, tileSurface in layer.tiles():
            tile = Tile((x*TILESIZE, y*TILESIZE), tileSurface)
            self.bg1.add(tile)
# 
        # layer = self.levelData.get_layer_by_name('Background2')
        # for x, y, tileSurface in layer.tiles():
        #     tile = Tile((x*TILESIZE, y*TILESIZE), tileSurface)
        #     self.bg2.add(tile)
# 
        # layer = self.levelData.get_layer_by_name('Background3')
        # for x, y, tileSurface in layer.tiles():
        #     tile = Tile((x*TILESIZE, y*TILESIZE), tileSurface)
        #     self.bg3.add(tile)
# 
        # layer = self.levelData.get_layer_by_name('Background4')
        # for x, y, tileSurface in layer.tiles():
        #     tile = Tile((x*TILESIZE, y*TILESIZE), tileSurface)
        #     self.bg4.add(tile)
        
        self.hero.add(Hero((32,464), faceRight = True))
        self.bees.add(Bee((200,100), moveRight = True))
        self.bees.add(Bee((200,240), moveRight = False))

        self.displaySurface = displaySurface


    def update(self):
        self.hero.update(self)
        self.bees.update(self)

        # Zoom animation logic
        if self.zooming:
            self.zoom_factor -= self.zoom_speed
            if self.zoom_factor <= self.target_zoom:
                self.zoom_factor = self.target_zoom
                self.zooming = False  # Stop zooming when at normal scale

        # get hero position
        hero = self.hero.sprite     # extract single hero instance
        heroX = hero.rect.centerx
        # Get the level width (assuming platforms define the width)
        levelWidth = self.levelData.width * TILESIZE  

        # new offset based on player position
        if heroX > self.scrollThreshold:
            self.cameraOffsetX = heroX - self.scrollThreshold
        # Clamp camera to level boundaries
        self.cameraOffsetX = max(0, min(self.cameraOffsetX, levelWidth - WINDOW_WIDTH))

    def draw(self):
        self.camera_surface.fill((0,0,0)) # clear screen

        # Draw background first
        self.background.draw(self.camera_surface)
        
        for layer in [self.bg1, self.platformTiles, self.bees, self.hero]:
            for sprite in layer:
                adjustedX = sprite.rect.x - self.cameraOffsetX # calculate position
                self.camera_surface.blit(sprite.image, (adjustedX, sprite.rect.y)) # draw at adjusted point

        #ZOOMING FOR START CAMERA
        # Apply zoom effect
        if self.zooming:
            # Scale the camera surface
            zoomed_width = int(WINDOW_WIDTH * self.zoom_factor)
            zoomed_height = int(WINDOW_HEIGHT * self.zoom_factor)
            zoomed_surface = pygame.transform.smoothscale(self.camera_surface, (zoomed_width, zoomed_height))

            # Get hero position in screen coordinates
            hero = self.hero.sprite
            hero_center_x = (hero.rect.centerx - self.cameraOffsetX) * self.zoom_factor
            hero_center_y = hero.rect.centery * self.zoom_factor

            # Compute top-left corner to center the zoom effect on hero
            x_offset = hero_center_x - WINDOW_WIDTH // 2
            y_offset = hero_center_y - WINDOW_HEIGHT // 2

            # Prevent zoom area from going out of bounds
            x_offset = max(0, min(x_offset, zoomed_width - WINDOW_WIDTH))
            y_offset = max(0, min(y_offset, zoomed_height - WINDOW_HEIGHT))

            # Blit zoomed surface onto displaySurface
            self.displaySurface.blit(zoomed_surface, (-x_offset, -y_offset))
        else:
            # Normal rendering once zoom is complete
            self.displaySurface.blit(self.camera_surface, (0, 0))


    def run(self):
        self.update()
        self.draw()