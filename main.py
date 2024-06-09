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
game.generate_enemies()
# Booleans
timer = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    if pygame.key.get_pressed()[pygame.K_SPACE]:
        if timer == 0:
            new = player.shoot()
            game.projectile_list.add(new)
    
    timer = 4 if timer == 0 else timer - 1

    for projectile in game.projectile_list:
        for enemy in game.enemy_list:
            print(enemy)
            projectile.check_collision(enemy)

    # Update
    game.update_groups()

    # Draw
    game.draw_groups()

    pygame.display.update() 
    clock.tick(60)