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

projectile_group = pygame.sprite.Group()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    # Update
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        new = player.shoot()
        projectile_group.add(new)

    player_group.update()
    projectile_group.update()

    # Draw
    game_screen.fill(BLACK)
    player_group.draw(game_screen)
    projectile_group.draw(game_screen)

    pygame.display.update() 
    clock.tick(30)