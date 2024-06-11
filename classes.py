from abc import ABC, abstractmethod
from settings import *
import pygame
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

    def update(self):
        self.move()

    def __repr__(self) -> str:
        return self.name

class Common_Enemy(Enemy, Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        Enemy.__init__(self)

        self.health = COMMON_ENEMY_HEALTH
        self.name = "Common Enemy"
        self.rarity = "Common"

        self.image = pygame.image.load(ASSETS_PATH + "common_enemy.png")
        self.rect = self.image.get_rect(midbottom=(x, y))

    def move(self):
        pass
    
    def shoot(self):
        pass

class Rare_Enemy(Sprite, Enemy):
    def __init__(self, x, y):
        Sprite.__init__(self)
        Enemy.__init__(self)

        self.health = RARE_ENEMY_HEALTH
        self.name = "Rare Enemy"
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
        pass

    def update(self):
        Enemy.update(self)

class Ultra_Rare_Enemy(Enemy, Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        Enemy.__init__(self)

        self.health = ULTRA_RARE_ENEMY_HEALTH
        self.name = "Ultra Rare Enemy"
        self.rarity = "Ultra Rare"

        self.image = pygame.image.load(ASSETS_PATH + "ultra_rare_enemy.png")
        self.rect = self.image.get_rect(midbottom=(x, y))

    def move(self):
        if self.rect.x > SCREEN_WIDTH:
            self.kill()
        else:
            self.rect.x += 0.5

    def shoot(self):
        pass

class Player(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.__health = PLAYER_HEALTH
        self.image = pygame.image.load(ASSETS_PATH + "spaceship.png")
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

        self.image = pygame.image.load(ASSETS_PATH + "projectile.png")
        self.rect = self.image.get_rect(midbottom=(x, y))
    
    def check_collision(self, enemy):
        if self.rect.colliderect(enemy.rect):
            enemy.take_damage(self.damage)
            if enemy.health == 0:
                rarity = enemy.rarity
                enemy.kill()
                return POINTS[rarity]
            self.kill()
        return 0

    def move(self):
        self.rect.y -= PROJECTILE_SPEED

    def update(self):
        self.move()
        if self.rect.y < 0:
            self.kill()

class Game():
    def __init__(self) -> None:
        self.__score = 0
        self.level = 0
        self.font = pygame.font.SysFont(None, 50)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")

        self.text = self.font.render(str(self.__score), True, WHITE)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (25, SCREEN_HEIGHT-25)

        self.enemy_list = Group()
        self.projectile_list = Group()
        self.player_group = GroupSingle()

    def generate_waves(self, enemy, x, y, gap, amount):
        for i in range(amount):
            new = enemy(x, y)
            self.enemy_list.add(new)
            x += gap

    def generate_enemies(self):
        for i in range(100, 300, 50):
            self.generate_waves(Rare_Enemy, 50, i, 50, 10)

        for i in range(350, 450, 50):
            self.generate_waves(Common_Enemy, 50, i, 50, 10)

    def is_game_over(self):
        pass

    def on_game_over(self):
        pass

    def update_groups(self, time):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and time % 10 == 0:
            new = self.player_group.sprites()[0].shoot()
            self.projectile_list.add(new)

        self.player_group.update()
        self.projectile_list.update()
        self.enemy_list.update()

    def draw_groups(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.text, self.text_rect)

        self.player_group.draw(self.screen)
        self.projectile_list.draw(self.screen)
        self.enemy_list.draw(self.screen)

    def update_score(self, amount):
        self.__score += amount
        self.text = self.font.render(str(self.__score), True, WHITE)

    def check_collisions(self):
        for projectile in self.projectile_list:
            for enemy in self.enemy_list:
                self.update_score(projectile.check_collision(enemy))