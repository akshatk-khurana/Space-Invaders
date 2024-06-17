from abc import ABC, abstractmethod
import random
import pygame
from pygame.sprite import Sprite

class Enemy(ABC):
    def __init__(self) -> None:
        self.rarity = None
        self.__health = NotImplemented

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def shoot(self):
        pass

    def set_health(self, amount):
        self.__health = amount
    
    def get_health(self):
        return self.__health

    def update(self):
        self.move()

    def __repr__(self) -> str:
        return "Enemy"

class Common_Enemy(Enemy, Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        Enemy.__init__(self)

        self.set_health(COMMON_ENEMY_HEALTH)

        self.rarity = "Common"

        self.image = pygame.image.load(ASSETS_PATH + "common_enemy.png")
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.up = False
        self.moved = 0

    def move(self):
        if self.up == False:
            self.rect.y += 1
            self.moved += 1
        elif self.up == True:
            self.rect.y -= 1
            self.moved -= 1
        
        if self.moved == 0 or self.moved == 50:
            self.up = not (self.up)
    
    def shoot(self):
        new = Projectile(CE_PROJECTILE_DAMAGE, 
                                self.rect.center[0], 
                                self.rect.center[1] - 25)
        new.fired_by = "Enemy"
        return new
class Rare_Enemy(Enemy, Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        Enemy.__init__(self)

        self.set_health(RARE_ENEMY_HEALTH)
        self.rarity = "Rare"

        self.image = pygame.image.load(ASSETS_PATH + "rare_enemy.png")
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.max = 300
        self.moved = 0
        self.direction = "R"

    def move(self):
        if self.direction == "R":
            if self.moved < self.max:
                self.rect.x += 2
                self.moved += 2
            else:
                self.direction = "L"

        elif self.direction == "L":
            if self.moved > 0:
                self.rect.x -= 2
                self.moved -= 2
            else:
                self.direction = "R"
    
    def shoot(self):
        new = Projectile(RE_PROJECTILE_DAMAGE, 
                                self.rect.center[0], 
                                self.rect.center[1] - 25)
        new.fired_by = "Enemy"
        return new
    
class Ultra_Rare_Enemy(Enemy, Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        Enemy.__init__(self)

        self.set_health(ULTRA_RARE_ENEMY_HEALTH)
        self.rarity = "Ultra Rare"

        self.image = pygame.image.load(ASSETS_PATH + "ultra_rare_enemy.png")
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.direction = "R"

    def move(self):
        if self.direction == "R":
            self.rect.x += random.randint(0, 4)
        elif self.direction == "L":
            self.rect.x -= random.randint(0, 4)
        
        if self.rect.x >= SCREEN_WIDTH:
            self.direction = "L"
        elif self.rect.x <= 0:
            self.direction = "R"

    def shoot(self):
        new = Projectile(URE_PROJECTILE_DAMAGE, 
                                self.rect.center[0], 
                                self.rect.center[1] - 25)
        return new

    def update(self):
        Enemy.update(self)