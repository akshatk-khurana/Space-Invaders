"""This file contains all the classes used in the game.

All these classes are instantiated in the main.py file and serve as
templates for key game entities like the player, different kinds of 
enemies, and the por

"""

from settings import *
import pygame
import random
from abc import ABC, abstractmethod
from pygame.sprite import Sprite, Group, GroupSingle

class Player(Sprite):
    """Simulate the player in the game

    Attributes:
        __health: An integer containing player heatlh
        image: Stores the loaded sprite for the player ship
        rect: A pygame rect object to store position 
    """

    def __init__(self, x, y):
        """Initializes the instance, with the give x and y 
        coordinates.

        Args:
          x: An integer for the x position.
          y: An integer for the y position.
        """

        super().__init__()
        self.__health = PLAYER_HEALTH
        self.image = pygame.image.load(ASSETS_PATH + "spaceship.png")
        self.rect = self.image.get_rect(midbottom=(x, y))

    def set_health(self, amount):
        self.__health = amount
    
    def get_health(self):
        return self.__health
    
    def shoot(self) -> None:
        """Create and return a Projecile object

        Returns:
            A projectile object instatiated with the 
            player's positon and the damage it gives.
        """
        return Projectile(PLAYER_PROJECTILE_DAMAGE, 
                                self.rect.center[0], 
                                self.rect.center[1] - 25,
                                str(self))

    def move(self):
        """Take input from the user to make the player
        move in the chosen direction.
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.rect.x - PLAYER_SPEED >= 0:
                self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.rect.x + PLAYER_SPEED <= SCREEN_WIDTH-self.rect.width:
                self.rect.x += PLAYER_SPEED
    
    def update(self):
        self.move()

    def __str__(self) -> str:
        return "Player"

class Projectile(Sprite):
    """Create a template for projectiles in the game

    Attributes:
        fired_by: A string containing the name of the entity 
        that instantiated the class.
        image: Stores the loaded sprite for the projectile.
        rect: A pygame rect object to store position.
    """

    def __init__(self, damage, x, y, entity) -> None:
        """Initialise custom and pygame attributes.

        Args:
            damage: An integer containing the damage to be given.
            that instantiated the class.
            x: An integer for the x position.
            y: An integer for the y position.
            entity: A string containing the name of the entity.
        """
        
        super().__init__()

        self.fired_by = entity
        self.damage = damage

        self.image = None
        if self.fired_by == "Player":
            self.image = pygame.image.load(ASSETS_PATH + "player_projectile.png")
        elif self.fired_by == "Enemy":
            self.image = pygame.image.load(ASSETS_PATH + "enemy_projectile.png")

        self.rect = self.image.get_rect(midbottom=(x, y))
    
    def check_collision(self, entity):
        """Check whether the projectile has collided with
        another entity and execute appropriate game logic.

        Args:
            entity: A player or enemy object to check collision with.
        """

        # Store a record of the collision and a score if an enemy is shot
        info = {"collided": False, "score": 0}

        if self.rect.colliderect(entity.rect):
            info["collided"] = True
            if str(entity) != "Projectile":
                # Enables polymorphism for enemy and player classes
                entity.set_health(entity.get_health()-self.damage)

            if str(entity) == "Enemy":
                # Polymorphism again, regardless of enemy class
                if entity.get_health() == 0:
                    info["score"] = POINTS[entity.rarity]
                    entity.kill()

            self.kill()
        return info
    
    def move(self):
        """To allow the projectiles to move based off settings.py"""

        if self.fired_by == "Player":
            self.rect.y -= PROJECTILE_SPEED
        elif self.fired_by == "Enemy":
            self.rect.y += PROJECTILE_SPEED
        if self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()

    def update(self):
        self.move()
    
    def __str__(self) -> str:
        return "Projectile"

class Game():
    def __init__(self) -> None:
        """Initialise needed game variables and display components.

        Also set up pygame display and fonts.
        """
        self.__score = 0
        self.font = pygame.font.SysFont(None, 50)
        self.big_font = pygame.font.SysFont(None, 100)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")

        self.score_text = self.font.render(str(self.__score), True, WHITE)
        self.score_text_rect = self.score_text.get_rect()
        self.score_text_rect.center = (25, SCREEN_HEIGHT-25)
        
        self.health_text = self.font.render("0", True, WHITE)
        self.health_text_rect = self.health_text.get_rect()
        self.health_text_rect.center = (SCREEN_WIDTH-40, SCREEN_HEIGHT-25)

        self.enemy_list = Group()
        self.projectile_list = Group()
        self.player_group = GroupSingle()

        self.level = 0
    
    def generate_enemies(self):
        
        offset = 50
        self.enemy_list.add(Ultra_Rare_Enemy(45, 60))

        for i in range(offset+100, 200+offset, 50):
            self.generate_waves(Rare_Enemy, 100, i, 50, 10)
        
        for i in range(offset+225, offset+375, 50):
            self.generate_waves(Common_Enemy, 50, i, 50, 19)

    def generate_waves(self, enemy, x, y, gap, amount):
        for i in range(amount):
            self.enemy_list.add(enemy(x, y))
            x += gap

    def is_game_over(self):
        return (self.player_group.sprites()[0].get_health() <= 0)

    def on_game_over(self):
        self.screen.fill(BLACK)

        go_text = self.big_font.render("Game Over", True, RED)
        go_text_rect = go_text.get_rect()
        go_text_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-80)

        final_text = self.font.render(f"Final Score: ", True, WHITE)
        final_rect = final_text.get_rect()
        final_rect.center = (SCREEN_WIDTH//2-40, SCREEN_HEIGHT//2-20)
        self.score_text_rect.center = (SCREEN_WIDTH//2+100, final_rect.center[1])

        play_again_btn = pygame.image.load(ASSETS_PATH+"button.png")
        self.btn_rect = play_again_btn.get_rect()
        self.btn_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+60)

        play_again_txt = self.font.render(f"Play Again", True, WHITE)
        txt_rect = play_again_txt.get_rect()
        txt_rect.center = self.btn_rect.center

        self.screen.blit(go_text, go_text_rect)
        self.screen.blit(final_text, final_rect)
        self.screen.blit(self.score_text, self.score_text_rect)
        self.screen.blit(play_again_btn, self.btn_rect)
        self.screen.blit(play_again_txt, txt_rect)
        
        pygame.display.update()

    def update_groups(self, time):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and time % 10 == 0:
            new = self.player_group.sprites()[0].shoot()
            self.projectile_list.add(new)

        enemies = list(self.enemy_list.sprites())
        if time % (int(50/self.level)) == 0:
            chosen = random.choice(enemies)
            projectiles = chosen.shoot()
            for projectile in projectiles:
                self.projectile_list.add(projectile)

        self.health_text = self.font.render(str(self.player_group.sprites()[0].get_health()), 
                                            True, 
                                            WHITE)

        self.player_group.update()
        self.projectile_list.update()
        self.enemy_list.update()

    def draw_groups(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.score_text, self.score_text_rect)
        self.screen.blit(self.health_text, self.health_text_rect)

        self.player_group.draw(self.screen)
        self.projectile_list.draw(self.screen)
        self.enemy_list.draw(self.screen)
        pygame.display.update()

    def update_score(self, amount):
        self.__score += amount
        self.score_text = self.font.render(str(self.__score), True, WHITE)

    def check_collisions(self):
        for projectile in self.projectile_list:
            if projectile.fired_by == "Player":
                for enemy in self.enemy_list:
                    collision = projectile.check_collision(enemy)
                    if collision["collided"] == True:
                        self.update_score(collision["score"])

            elif projectile.fired_by == "Enemy":
                projectile.check_collision(self.player_group.sprites()[0])
                for player_projectile in self.projectile_list:
                    if player_projectile.fired_by == "Player":
                        projectile.check_collision(player_projectile)

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

    def __str__(self) -> str:
        return "Enemy"

class Common_Enemy(Enemy, Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        Enemy.__init__(self)

        self.set_health(CE_HEALTH)

        self.rarity = "Common"

        self.image = pygame.image.load(ASSETS_PATH + "common_enemy.png")
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.up = False
        self.moved = 0

    def move(self):
        if self.up == False:
            self.rect.y += CE_SPEED
            self.moved += CE_SPEED
        elif self.up == True:
            self.rect.y -= CE_SPEED
            self.moved -= CE_SPEED
        
        if self.moved == 0 or self.moved == 50:
            self.up = not (self.up)
    
    def shoot(self):
        return [Projectile(CE_PROJECTILE_DAMAGE, 
                                self.rect.center[0], 
                                self.rect.center[1] - 25,
                                str(self))]
    
class Rare_Enemy(Enemy, Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        Enemy.__init__(self)

        self.set_health(RE_HEALTH)
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
        first = Projectile(RE_PROJECTILE_DAMAGE, 
                                self.rect.center[0], 
                                self.rect.center[1] - 25,
                                str(self))
        second = Projectile(RE_PROJECTILE_DAMAGE, 
                                self.rect.center[0], 
                                self.rect.center[1] + 25,
                                str(self))
        return [first, second]
    
class Ultra_Rare_Enemy(Enemy, Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        Enemy.__init__(self)

        self.set_health(URE_HEALTH)
        self.rarity = "Ultra Rare"

        self.image = pygame.image.load(ASSETS_PATH + "ultra_rare_enemy.png")
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.direction = "R"

    def move(self):
        if self.direction == "R":
            self.rect.x += random.randint(0, 10)
        elif self.direction == "L":
            self.rect.x -= random.randint(0, 10)
        
        if self.rect.x >= SCREEN_WIDTH:
            self.direction = "L"
        elif self.rect.x <= 0:
            self.direction = "R"

    def shoot(self):
        projectile_list = []
        for pos in range(self.rect.x-25, self.rect.x+26, 25):
            projectile_list.append(Projectile(URE_PROJECTILE_DAMAGE, 
                                          pos, 
                                          self.rect.center[1] - 25, 
                                          str(self)))
        return projectile_list