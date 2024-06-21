"""This file houses all the 'settings' that can tweak certain aspects in the game.

It reduces the need to hardcode values, and makes it quite easy to make changes
to specific numerical values within the game logic.

For general usage and definition of new variables:

CE equates to Common Enemy
RE equates to Rare Enemy 
URE equates to Ultra Rare Enemy
"""

# Values relating to entities
CE_HEALTH = 1
RE_HEALTH = 2
URE_HEALTH = 16
PLAYER_HEALTH = 16

PLAYER_SPEED = 10
CE_SPEED = 1
RE_SPEED = 2

POINTS = {"Common": 10,
          "Rare": 20,
          "Ultra Rare": 50}

CE_PROJECTILE_DAMAGE = 2
RE_PROJECTILE_DAMAGE = 4
URE_PROJECTILE_DAMAGE = 8
PLAYER_PROJECTILE_DAMAGE = 1
PROJECTILE_SPEED = 12

# Colours used for UI
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Miscellaneous
ASSETS_PATH = "Assets/"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600