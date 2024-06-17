"""This is the main file for running this Space Invaders game.

This file initialises the pygame module and defines some necessary variables. 
It contains a while loop to run the game logic contained within the classes 
imported from the 'classes' file. 
"""

import pygame
import sys
from settings import *
from classes import *

pygame.init()

# This will be used later to decide frame-rate
clock = pygame.time.Clock()

# Allow for intervals between player and enemy shooting
timer = 0

# Used to initiate and store an instance of the Game class
game = None
start = True
  
while True:
    # Check whether the game has been initialised
    if start:
        # If not, define the needed variables
        game = Game()
        player = Player(500, 540)
        game.player_group.add(player)
        start = False

    # Close the game window, if the user clicks 'X' on the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
    
    # Check if the game is over
    if game.is_game_over():
        game.on_game_over()

        # Give the player to restart the game by clicking a button
        if game.btn_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                start = True       
    else:
        # If there are no enemies left, generate them
        if len(game.enemy_list.sprites()) == 0:
            game.level += 1
            game.generate_enemies()

        # Update, draw and display the game
        game.check_collisions()
        game.update_groups(timer)
        game.draw_groups()

    # Increase timer and frames
    timer = 100 if timer == 0 else timer + 1 
    clock.tick(30)