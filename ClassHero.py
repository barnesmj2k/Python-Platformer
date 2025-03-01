import pygame
from Config import *
from ClassSpriteSheet import SpriteSheet

runSprites = [
    (24,16,40,52),
    (104,16,40,52),
    (184,16,40,52),
    (264,16,40,52),
    (344,16,40,52),
    (424,16,40,52),
    (504,16,40,52),
    (584,16,40,52)
]

idleSprites = [
    (12,12,44,52),
    (76,12,44,52),
    (140,12,44,52),
    (204,12,44,52)
]

attackSprites = [
    (4,0,92,80),
    (100,0,92,80),
    (196,0,92,80),
    (294,0,92,80),
    (388,0,92,80),
    (484,0,92,80),
    (676,0,92,80)
]

deathSprites = [
    (0,0,64,56),
    (80,0,64,56),
    (160,0,64,56),
    (240,0,64,56),
    (320,0,64,56),
    (400,0,64,56),
    (480,0,64,56),
    (560,0,64,56)
]

class Hero(pygame.sprite.Sprite):
    def __init__(self, position, faceRight):
        super().__init__()

        #Load spritesheets
        idleSpriteSheet = SpriteSheet(GHOST_SPRITESHEET_PATH + "Character/Idle/Idle-Sheet.png", idleSprites)
        runSpriteSheet = SpriteSheet(GHOST_SPRITESHEET_PATH + "Character/Run/Run-Sheet.png", runSprites)
        attackSpriteSheet = SpriteSheet(GHOST_SPRITESHEET_PATH + "Character/Attack-01/Attack-01-Sheet.png", attackSprites)
        deathSpriteSheet = SpriteSheet(SPRITESHEET_PATH + "Character/Dead/Dead-Sheet.png", deathSprites)

        self.spriteSheets = {
            'IDLE' : idleSpriteSheet,
            'RUN' : runSpriteSheet,
            'JUMP' : runSpriteSheet,
            'ATTACK' : attackSpriteSheet,
            'DIE' : deathSpriteSheet
        }

        

        #character movemente and direction
        self.animationIndex = 0
        self.facingRight = faceRight
        self.currentState = 'IDLE'
        self.xDir = 0
        self.yDir = 0
        self.speed = SPEED_HERO
        self.xPos = position[0]
        self.yPos = position[1]
        # jump physics
        self.yVelocity = 0  # Controls the vertical movement
        self.gravity = 0.8  # Strength of gravity
        self.jumpStrength = -15  # Adjust for smoother jump
        self.onGround = False  # Track if player is on ground

        self.image = self.spriteSheets['IDLE'].getSprites(flipped = not self.facingRight)[0]
        self.rect = self.image.get_rect(center=(self.xPos, self.yPos))


    def update(self, level):

        self.previousState = self.currentState
        self.xDir = 0
        self.yDir = 0

        # KEYBOARD INPUT, key status
        if self.currentState != 'ATTACK' and self.currentState != 'DIE':
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.currentState = 'ATTACK'
            elif keys[pygame.K_UP] and self.onGround:   #jump only if on the ground
                self.yVelocity = self.jumpStrength  # apply jump force
                self.onGround = False   # player in air
                self.currentState = 'JUMP'
            elif keys[pygame.K_LEFT]:
                self.xDir = -1
                self.facingRight = False
                self.currentState = 'RUN'
            elif keys[pygame.K_RIGHT]:
                self.xDir = 1
                self.facingRight = True
                self.currentState = 'RUN'
            
            else:
                self.currentState = 'IDLE'

        #selcet spritesheet for setting animation based on current state
        self.selectAnimation()

        if self.previousState != self.currentState:
            self.animationIndex = 0

        self.image = self.currentAnimation[int(self.animationIndex)]

        if self.currentState == 'IDLE':
            new_size = (30, 54)
        elif self.currentState == 'RUN':
            new_size = (30, 54)
        elif self.currentState == 'JUMP':
            new_size = (30, 54)
        elif self.currentState == 'ATTACK':
            new_size = (88, 64)
        elif self.currentState == 'DIE':
            new_size = (30, 54)

        # Update rect size and then keep its center consistent
        self.rect.size = new_size
        self.rect.center = (self.xPos, self.yPos)


        # Play animation until end of current animation is reached
        self.animationIndex += self.animationSpeed
        if self.animationIndex >= len(self.currentAnimation):
            if self.currentState == 'DIE':
                self.animationIndex = len(self.currentAnimation) - 1
            else:
                self.animationIndex = 0
                self.currentState = 'IDLE'

        self.moveHorizontal(level)
        self.moveVertical(level)

        self.checkEnemyCollisions(level.bees)
            
#    def draw(self, displaySurface): # DRAW FUNCTION REMOVED BECAUSE OF PYGAME SPRITE CLASS
#        displaySurface.blit(self.image, self.rect)

    def selectAnimation(self):
        self.animationSpeed = ANIMSPEED_HERO_DEFAULT
        if self.currentState == 'IDLE':
            self.animationSpeed = ANIMSPEED_HERO_IDLE

        spriteSheet = self.spriteSheets[self.currentState]    
        self.currentAnimation = spriteSheet.getSprites(flipped = not self.facingRight)

    def moveHorizontal(self, level):
        self.rect.centerx += self.xDir * self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > LEVEL_WIDTH:
            self.rect.right = LEVEL_WIDTH
        
        for platform in level.platformTiles:
            if self.rect.colliderect(platform.rect):
                if self.xDir > 0:                   # Moving right
                    self.rect.right = platform.rect.left
                elif self.xDir < 0:                 # Moving left
                    self.rect.left = platform.rect.right

        self.xPos = self.rect.centerx

    def moveVertical(self, level):
        if not self.onGround:
            self.yVelocity += self.gravity          # gravity pulls character down
        self.yPos += self.yVelocity                 # move by velocity
        self.rect.centery = self.yPos

        self.onGround = False                       # assume false

        # check for platform collision
        for platform in level.platformTiles:
            if self.rect.colliderect(platform.rect):

                if self.yVelocity > 0:                   # Falling and hitting platform
                    self.rect.bottom = platform.rect.top
                    self.yVelocity = 0                   # Stop falling
                    self.onGround = True            # Player is on ground

                elif self.yVelocity < 0:                 # jumping and hitting ceiling
                    self.rect.top = platform.rect.bottom
                    self.yVelocity = 0                   # stop upward moevement


        self.yPos = self.rect.centery

    def die(self):
        if self.currentState != 'DIE':
            self.currentState = 'DIE'
            self.animationIndex = 0

    def checkEnemyCollisions(self, enemies):
        collidedSprites = pygame.sprite.spritecollide(self, enemies, False)
        for enemy in collidedSprites:
            if self.currentState == 'ATTACK':
                if self.facingRight == True:
                    if enemy.rect.left < self.rect.right - 30:
                        enemy.die()
                elif enemy.rect.right > self.rect.left + 30:
                    enemy.die()
            elif enemy.currentState != 'DYING':
                if self.rect.left < enemy.rect.left:
                    if self.rect.right > enemy.rect.left + 16:
                        self.die()
                elif self.rect.right > enemy.rect.right:
                    if self.rect.left < enemy.rect.right - 16:
                        self.die()
