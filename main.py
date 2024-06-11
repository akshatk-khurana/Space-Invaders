import pygame
import sys
from settings import *
from classes import *

# Set up game screen
pygame.init()
clock = pygame.time.Clock()

# Instantiate Game and Player classes
game = Game()
player = Player(500, 550)
game.player_group.add(player)

timer = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
    
    if len(game.enemy_list.sprites()) == 0:
        game.generate_enemies()
    
    game.check_collisions()
    
    # Update & Draw
    game.update_groups(timer)
    game.draw_groups()

    timer = 100 if timer == 0 else timer + 1 
    pygame.display.update()
    clock.tick(60)