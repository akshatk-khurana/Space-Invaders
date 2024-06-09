from abc import ABC, abstractmethod
from settings import *
import pygame
import random
from pygame.sprite import Sprite, Group, GroupSingle

class Enemy(ABC):
    def __init__(self) -> None:
        self.health = 0
        self.speed = 0
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
        print(self.health)

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

class Rare_Enemy(Sprite, Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self)
        Sprite.__init__(self)

        self.health = RARE_ENEMY_HEALTH
        self.name = "Rare Enemy"
        self.rarity = "Rare"

        self.image = pygame.image.load("rare_enemy.png")
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.direction = "R"

    def move(self):
        if self.direction == "R":
            if self.rect.x < SCREEN_WIDTH:
                self.rect.x += 5
            else:
                self.direction = "L"

        elif self.direction == "L":
            if self.rect.x > 0:
                self.rect.x -= 5
            else:
                self.direction = "R"
    
    def shoot(self):
        pass

    def update(self):
        if (self.health == 0):
            self.kill()
        self.move()

    def __repr__(self) -> str:
        return Enemy.__repr__(self)
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
        self.image = pygame.image.load("spaceship.png")
        self.rect = self.image.get_rect(midbottom=(x, y))
    
    def shoot(self) -> None:
        projectile = Projectile(PROJECTILE_DAMAGE, 
                                self.rect.center[0], 
                                self.rect.center[1] - 25)
        return projectile

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.rect.x - 10 >= 0:
                self.rect.x -= 10
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.rect.x + 10 <= SCREEN_WIDTH-self.rect.width:
                self.rect.x += 10
    
    def update(self):
        self.move()

class Projectile(Sprite):
    def __init__(self, damage, x, y) -> None:
        super().__init__()

        self.damage = damage

        self.image = pygame.image.load("projectile.png")
        self.rect = self.image.get_rect(midbottom=(x, y))
    
    def check_collision(self, enemy):
        if self.rect.colliderect(enemy.rect):
            enemy.take_damage(self.damage)
            self.kill()

    def update(self):
        self.rect.y -= PROJECTILE_SPEED
        if self.rect.y < 0:
            self.kill()

class Game():
    def __init__(self) -> None:
        self.__score = 0
        self.level = 0

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")

        self.enemy_list = Group()
        self.projectile_list = Group()
        self.player_group = GroupSingle()
    
    def generate_enemies(self):
        pos = 50
        for i in range(10):
            new = Rare_Enemy(pos, 50)
            self.enemy_list.add(new)
            pos += 70

    def is_game_over(self):
        return False

    def on_game_over(self):
        pass

    def update_score(self, amount):
        self.__score += amount

    def update_groups(self):
        self.player_group.update()
        self.projectile_list.update()
        self.enemy_list.update()

    def draw_groups(self):
        self.screen.fill(BLACK)
        self.player_group.draw(self.screen)
        self.projectile_list.draw(self.screen)
        self.enemy_list.draw(self.screen)