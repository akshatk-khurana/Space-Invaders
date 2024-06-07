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
player = Player(500, 550)

player_group = pygame.sprite.GroupSingle()
player_group.add(player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.grou
    
    if keys[pygame.K_d]:
        player.move('D')

    # Frame updates go here
    player_group.draw(game_screen)

    pygame.display.update() 
    clock.tick(30)