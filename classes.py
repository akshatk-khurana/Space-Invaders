from abc import ABC, abstractmethod
from settings import *
import pygame

from pygame.sprite import Sprite

class Enemy(ABC):
    def __init__(self, x, y) -> None:
        self.__health = ENEMY_HEALTH
        self.position = (x, y)
        self.rarity = None
        self.name = "Enemy"

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def shoot(self):
        pass

    def take_damage(self, amount):
        self.health -= amount

    def __repr__(self) -> str:
        return self.name

class Common_Enemy(Enemy, Sprite):
    def __init__(self):
        super().__init__()
        self.__name = "Common Enemy"
        self.rarity = "Common"

    def move(self):
        pass
    
    def shoot(self):
        pass

class Rare_Enemy(Enemy, Sprite):
    def __init__(self):
        super().__init__()
        self.__name = "Rare Enemy"
        self.rarity = "Rare"

    def move(self):
        pass
    
    def shoot(self):
        pass

class Ultra_Rare_Enemy(Enemy, Sprite):
    def __init__(self):
        super().__init__()
        self.__name = "Ultra Rare Enemy"
        self.rarity = "Rare"
    
    def move(self):
        pass

    def shoot(self):
        pass

class Player(Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.__health = PLAYER_HEALTH
        self._position = (x, y)
        self.image = pygame.image.load("spaceship.png")
        self.rect = self.image.get_rect(midbottom=(x, y))
    
    def shoot(self):
        pass

    def move(self, direction):
        if direction == "A":
            self.rect.x -= 10
        elif direction == "B":
            self.rect.x += 10
    
    def update(self, direction):
        self.move(direction)

class Projectile(Sprite):
    def __init__(self, damage, position) -> None:
        self.damage = damage
        self.position = position
    
    def check_collision(self, enemy):
        pass

class Game():
    def __init__(self) -> None:
        self.__score = 0
        self.level = 0
        self.__enemy_list = []
        self.__projectile_list = []
    
    def generate_enemies(self):
        pass

    def is_game_over(self):
        return False

    def on_game_over(self):
        pass

    def update_score(self, amount):
        pass