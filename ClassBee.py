import pygame
from Config import *
from ClassSpriteSheet import SpriteSheet

beeSprites = [
    (16,0,48,48),
    (80,0,48,48),
    (144,0,48,48),
    (208,0,48,48)
]

class Bee(pygame.sprite.Sprite):
    def __init__(self, position, moveRight):
        super().__init__()
        # Load spritesheets
        self.flySpriteSheet = SpriteSheet(SPRITESHEET_PATH + "/Mob/Small bee/Fly/Fly-Sheet.png", beeSprites)
        self.hitSpriteSheet = SpriteSheet(SPRITESHEET_PATH + "/Mob/Small bee/Hit/Hit-Sheet.png", beeSprites)
        self.attackSpriteSheet = SpriteSheet(SPRITESHEET_PATH + "/Mob/Small bee/Attack/Attack-Sheet.png", beeSprites)
        
        self.image = self.flySpriteSheet.getSprites(moveRight)[0]
        self.rect = self.image.get_rect(bottomleft = position)
        self.movingRight = moveRight
        self.yDir = 0
        self.animationIndex = 0
        self.currentState = 'FLY'

    def update(self, level):
        # Update position
        if self.movingRight == False:
            self.rect.x -= SPEED_BEE
        else:
            self.rect.x += SPEED_BEE

        # When flying outside the window, just turn around
        if self.rect.left < 0:
            self.movingRight = True
        if self.rect.right > WINDOW_WIDTH:
            self.movingRight = False

        if self.currentState == 'DYING':
            self.yDir += GRAVITY
            self.rect.y += self.yDir
            if self.rect.top > WINDOW_HEIGHT:
                self.kill() 

        # trigger attack
        heroRect = level.hero.sprite.rect  # to decide if attack, we need to know player position
        heroX = heroRect.centerx    # to decide if attack, we need to know player position
        if self.currentState == 'FLY':
            if heroRect.top < self.rect.bottom <= heroRect.bottom: # same height as player
                if self.movingRight == True:
                    if self.rect.left < heroX and self.rect.right > heroX - 50:  # if bee is in range, attack
                        self.currentState = 'ATTACK'
                        self.animationIndex = 0
                else:
                    if self.rect.right > heroX and self.rect.left < heroX + 50:
                        self.currentState = 'ATTACK'
                        self.animationIndex = 0
        elif self.currentState == 'ATTACK':  # bee is already attacking
            if self.movingRight == True:
                if self.rect.left >= heroX or self.rect.right < heroX - 50: # if Bee is outside attack range, fly
                    self.currentState = 'FLY'
                    self.animationIndex = 0
            else:
                if self.rect.right <= heroX or self.rect.left > heroX + 50:
                    self.currentState = 'FLY'
                    self.animationIndex = 0
        
        # Select animation for the current action
        self.selectAnimation()

        # Animate Sprite
        self.animationIndex += self.animationSpeed
        if self.animationIndex >= len(self.currentAnimation):
            if self.currentState == 'ATTACK' or self.currentState == 'DYING': 
                self.animationIndex = len(self.currentAnimation) -1 #show last sprite until no longer in attack state
            else:
                self.currentState = 'FLY'
                self.animationIndex = 0

        self.image = self.currentAnimation[int(self.animationIndex)]
        
#    def draw(self, displaySurface):   # DRAW FUNCTION REMOVED BECAUSE OF PYGAME SPRITE CLASS
#        displaySurface.blit(self.image, self.rect)

    def selectAnimation(self):
        self.animationSpeed = ANIMSPEED_BEE
        if self.currentState == 'FLY':
            self.currentAnimation = self.flySpriteSheet.getSprites(flipped = self.movingRight)
        elif self.currentState == 'ATTACK':
            self.animationSpeed = ANIMSPEED_BEE_ATTACK
            self.currentAnimation = self.attackSpriteSheet.getSprites(flipped = self.movingRight)
        else:
            self.currentAnimation = self.hitSpriteSheet.getSprites(flipped = self.movingRight)

    def die(self):
        if self.currentState != 'DYING':
            self.animationIndex = 0
            self.currentState = 'DYING'