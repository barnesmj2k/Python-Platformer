import pygame
from pygame import mixer
from Config import *
from Level import Level


# Init
pygame.init()
clock = pygame.time.Clock()

# Open window
displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("MagicForest")

# Starting the mixer 
mixer.init() 
# Loading the song 
mixer.music.load(MUSIC_PATH +"SeeingYou.mp3") 
# Setting the volume 
mixer.music.set_volume(0.7) 
# Start playing the song 
mixer.music.play() 

# global variable to track first time loading
first_time_loading = True

def restartGame():
    global first_time_loading
    first_time_loading = False
    return Level(displaySurface, first_time_loading) #  reinitialize level

level = Level(displaySurface, first_time_loading)


isGameRunning = True
while isGameRunning:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isGameRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isGameRunning = False
            elif event.key == pygame.K_r:
                level = restartGame()   # restart game on press "R"

    level.run()

    pygame.display.flip()
    clock.tick(60)

# Close pygame
pygame.quit()
