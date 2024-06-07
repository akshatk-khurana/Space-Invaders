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
        self.__position = (x, y)
        self.image = pygame.image.load("spaceship.png")
        self.rect = self.image.get_rect(midbottom=(x, y))
    
    def shoot(self) -> None:
        projectile = Projectile(PROJECTILE_DAMAGE, 
                                self.__position[0], 
                                self.__position[1] - 75)
        return projectile

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= 10
            self.__position = (self.rect.x, self.__position[1])
        
        if keys[pygame.K_d]:
            self.rect.x += 10
    
    def update(self):
        self.move()

class Projectile(Sprite):
    def __init__(self, damage, x, y) -> None:
        super().__init__()

        self.damage = damage
        self.position = (x, y)

        self.image = pygame.image.load("projectile.png")
        self.rect = self.image.get_rect(midbottom=(x, y))
    
    def check_collision(self, enemy):
        pass

    def update(self):
        self.rect.y -= PROJECTILE_SPEED

class Game():
    def __init__(self) -> None:
        self.__score = 0
        self.level = 0
        self.enemy_list = []
        self.projectile_list = []
    
    def generate_enemies(self):
        pass

    def is_game_over(self):
        return False

    def on_game_over(self):
        pass

    def update_score(self, amount):
        pass