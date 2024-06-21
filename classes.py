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
    """Simulate the player in the game.

    Attributes:
        __health: An integer containing player heatlh.
        image: Stores the loaded sprite for the player ship.
        rect: A pygame rect object to store position.
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
        """Set the encapsulated health attribute.

        Args:
            amount: An integer representing the value
            to set the health attribute to.
        """
        self.__health = amount
    
    def get_health(self):
        """Access the encapsulated health attribute.

        Returns:
            An integer representing the current player health.
        """
        return self.__health
    
    def shoot(self) -> None:
        """Create and initialise a Projecile object.

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
        move in the direction chosen by the user input.
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.rect.x - PLAYER_SPEED >= 0:
                self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.rect.x + PLAYER_SPEED <= SCREEN_WIDTH-self.rect.width:
                self.rect.x += PLAYER_SPEED
    
    def update(self):
        """The Pygame Sprite class' default 
        method to update this sprite on the screen.
        """
        self.move()

    def __str__(self) -> str:
        """Determine the string returned when str() is
        called on an object of this class.
        """
        return "Player"

class Projectile(Sprite):
    """Create a template for projectiles in the game.

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
            entity: A player, projectile or enemy object to 
            check collision with.

        Returns:
            A dict with a 'collided' key to say whether or not
            a collision took place and a 'score' key that needs 
            to be updated in the Game class if necessary.
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
        """Allow the projectiles to move based off movement settings
        defined inside of settings.py"""

        if self.fired_by == "Player":
            self.rect.y -= PROJECTILE_SPEED
        elif self.fired_by == "Enemy":
            self.rect.y += PROJECTILE_SPEED
        if self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()

    def update(self):
        """The Pygame Sprite class' default 
        method to update this sprite on the screen.
        """
        self.move()
    
    def __str__(self) -> str:
        """Determine the string returned when str() is
        called on an object of this class.
        """
        return "Projectile"

class Game():
    def __init__(self) -> None:
        """Initialise needed game variables as attributes, including the score
        and level.

        Also set up pygame display components (text, captions and sprites)
        and fonts to be used for text elements.

        Attributes:
            __score: An integer containing the current score.
            level: An integer describing player progression.

            Note: All the other attributes are Pygame Font, Rect 
            and Surface objects used to create the display.
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
        """Use the generate_waves function to generate enemies 
        in different lines, based off rarity.
        """

        # Start away from the top of the screen
        offset = 50

        self.enemy_list.add(Ultra_Rare_Enemy(45, 60))

        for i in range(offset+100, 200+offset, 50):
            self.generate_waves(Rare_Enemy, 100, i, 50, 10)
        
        for i in range(offset+225, offset+375, 50):
            self.generate_waves(Common_Enemy, 50, i, 50, 19)

    def generate_waves(self, enemy, x, y, gap, amount):
        """Modularise the repetitive task of generating enemies
        in a straight horizontal line.

        Args:
            enemy: A subclass of the Enemy class.
            x: An integer for the starting x coordinate.
            y: An integer for the starting y coordinate.
            gap: An integer representing the gap between
            each enemy in the wave.
            amount: An integer for the amount of enemies
            to generate in the wave.
        """
        for i in range(amount):
            self.enemy_list.add(enemy(x, y))
            x += gap

    def is_game_over(self):
        """Check if the game is over.
        
        Returns:
            A boolean value which checks whether the 
            player's health is equal to or less than 0.
        """
        return (self.player_group.sprites()[0].get_health() <= 0)

    def on_game_over(self):
        """Carry out procedures once the game is deemed 
        to be finished. 
        
        This includes adding game over text, a play again 
        button and the final score, as well as making them
        visible on the game display.
        """
        
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
        """Check and allow for both player and 
        enemy shooting, and keep updating the health text.

        Args: 
            time: An integer that describes the current value
            of the timer running in the main loop to add delay.
        """

        keys = pygame.key.get_pressed()

        # Slow down player shooting to avoid them 
        # being too overpowered
        if keys[pygame.K_SPACE] and time % 10 == 0:
            new = self.player_group.sprites()[0].shoot()
            self.projectile_list.add(new)

        enemies = list(self.enemy_list.sprites())

        # Increase the frequency of enemies shooting
        # as the player progresses in the game
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
        """Draw the updated pygame sprite groups onto 
        the user display and update score and health text.
        """

        self.screen.fill(BLACK)
        self.screen.blit(self.score_text, self.score_text_rect)
        self.screen.blit(self.health_text, self.health_text_rect)

        self.player_group.draw(self.screen)
        self.projectile_list.draw(self.screen)
        self.enemy_list.draw(self.screen)
        pygame.display.update()

    def update_score(self, amount):
        """Change the score attribute and the text
        shown on screen.

        Args:
            amount: An integer to change the score by.
        """
        self.__score += amount
        self.score_text = self.font.render(str(self.__score), True, WHITE)

    def check_collisions(self):
        """Check for any collisions happening in the game
        and perform certain actions depending on them.
        """

        for projectile in self.projectile_list:

            # Execute different procedures based off
            # the type of projectile
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
        """Initialise the abstract base class for an enemy.
        
        Attributes:
            rarity: Set to none, but to be assigned to a string
            by subclasses of this abstract class.
            __health: Set to NotImplemented, but also to be assigned
            by subclasses, varying by rarity.
        """

        self.rarity = None
        self.__health = NotImplemented

    @abstractmethod
    def move(self):
        """Allow the enemy to move in a specific manner.
        To be implemented by subclasses.
        """
        pass

    @abstractmethod
    def shoot(self):
        """Add shooting capabilities to the enemy.
        To be implemented by subclasses.
        """
        pass

    def set_health(self, amount):
        """Set the encapsulated health attribute.
        
        Args:
            amount: An integer describing the value
            to set the health attribute to.
        """
        self.__health = amount
    
    def get_health(self):
        """ Access the encapsulated health attribute.
        
        Returns:
            An integer representing the health 
            of an enemy of this class.
        """
        return self.__health

    def update(self):
        """Overide the move method in the Sprite
        class which will also be inherited from
        in subclasses.
        """
        self.move()

    def __str__(self) -> str:
        """Determine the string returned when str() is
        called on an object of this class.
        """
        return "Enemy"

class Common_Enemy(Enemy, Sprite):
    """Create a template for common enemies in the game.

    Attributes:
        rarity: Set to a string describing enemy rarity.
        __health: Set to CE_HEALTH (from settings.py).
        up: A boolean representing the direction of motion.
        moved: An integer containing the distance that the 
        object has moved so far.
        image: Stores the loaded sprite for the enemy.
        rect: A pygame rect object to store position.
    """

    def __init__(self, x, y):
        """Initialise and inherit necessary attributes and 
        methods from Sprite and Enemy classes. Define new ones
        specific to this class as well.
        
        Args:
            x: An integer for the x position.
            y: An integer for the y position.
        """

        Sprite.__init__(self)
        Enemy.__init__(self)

        self.set_health(CE_HEALTH)

        self.rarity = "Common"

        self.image = pygame.image.load(ASSETS_PATH + "common_enemy.png")
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.up = False
        self.moved = 0

    def move(self):
        """Implement the Enemy abstract class' move()
        method to allow for an up and down movement
        pattern.
        """

        if self.up == False:
            self.rect.y += CE_SPEED
            self.moved += CE_SPEED
        elif self.up == True:
            self.rect.y -= CE_SPEED
            self.moved -= CE_SPEED
        
        if self.moved == 0 or self.moved == 50:
            self.up = not (self.up)
    
    def shoot(self):
        """Implement the original method from 
        the abstract Enemy class.
        """
        return [Projectile(CE_PROJECTILE_DAMAGE, 
                                self.rect.center[0], 
                                self.rect.center[1] - 25,
                                str(self))]
    
class Rare_Enemy(Enemy, Sprite):
    """Create a template for rare enemies in the game.

    Attributes:
        rarity: Set to a string describing enemy rarity.
        __health: Set to RE_HEALTH (from settings.py).
        direction: A string representing the direction of motion.
        moved: An integer containing the distance that the 
        object has moved so far.
        max: An integer representing the maximum amount to move.
        image: Stores the loaded sprite for the enemy.
        rect: A pygame rect object to store position.
    """

    def __init__(self, x, y):
        """Initialise and inherit necessary attributes and 
        methods from Sprite and Enemy classes. Define new ones
        specific to this class as well.
        
        Args:
            x: An integer for the x position.
            y: An integer for the y position.
        """

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
        """Implement the Enemy abstract class' move()
        method to allow for a side-to-side movement
        pattern without going off the screen.
        """

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
        """Implement the original method from 
        the abstract Enemy class and add two projectiles
        every time shoot() is called.
        """
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
    """Create a template for rare enemies in the game.

    Attributes:
        rarity: Set to a string describing enemy rarity.
        __health: Set to RE_HEALTH (from settings.py).
        direction: A string representing the direction of motion.
        image: Stores the loaded sprite for the enemy.
        rect: A pygame rect object to store position.
    """

    def __init__(self, x, y):
        """Initialise and inherit necessary attributes and 
        methods from Sprite and Enemy classes. Define new ones
        specific to this class as well.
        
        Args:
            x: An integer for the x position.
            y: An integer for the y position.
        """
        
        Sprite.__init__(self)
        Enemy.__init__(self)

        self.set_health(URE_HEALTH)
        self.rarity = "Ultra Rare"

        self.image = pygame.image.load(ASSETS_PATH + "ultra_rare_enemy.png")
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.direction = "R"

    def move(self):
        """Implement the Enemy abstract class' move()
        method to allow for a more randomnized side-to-side 
        movement pattern where the enemy can travel off screen.
        """

        if self.direction == "R":
            self.rect.x += random.randint(0, 20)
        elif self.direction == "L":
            self.rect.x -= random.randint(0, 20)
        
        if self.rect.x >= SCREEN_WIDTH:
            self.direction = "L"
        elif self.rect.x <= 0:
            self.direction = "R"

    def shoot(self):
        """Implement the original method from 
        the abstract Enemy class and shoot three 
        projectiles at a time.
        """

        projectile_list = []
        for pos in range(self.rect.x-25, self.rect.x+26, 25):
            projectile_list.append(Projectile(URE_PROJECTILE_DAMAGE, 
                                          pos, 
                                          self.rect.center[1] - 25, 
                                          str(self)))
        return projectile_list