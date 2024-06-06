import pygame
import sys
from settings import *
from classes import *

# Set up pygame
pygame.init()
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

game = Game()



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
    
    # Frame updates go here

    pygame.display.update() 
    clock.tick(30)