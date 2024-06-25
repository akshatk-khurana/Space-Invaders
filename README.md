# Space Invaders, but with a twist

## Description
A relatively simple Space Invaders-based game that allows the player to eliminate oncoming enemies
of different rarities and abilities. It is made using Python's Pygame library and places a heavy 
empahsis on utilising classes within its implementation and leveraging the object-oriented programming paradigm.

## Features
This game contains various aspects of game play and functionalities, including:
- Three different kinds of enemies - Common, Rare and Ultra Rare - each with their own shooting styles
and movement patterns. 
    - Common enemies (blue) move in an up down motion and only shoot 1 projectile at a time. 
    - Rare enemies (green) move in from side to side and shoot 2 projectiles at once. 
    - Ultra rare enemies (red) move side to side across the screen in an erotic motion and shoot three
    evenly space projectiles at once.
- A spaceship for the player, who can move side to side (not off the screen) and shoot with good, but not overpowering pace.
- The game score is displayed in the bottom left corner and the health of the player is shown on the bottom right corner.
- A game over screen is displayed once the player is out of health and this screen contains the player's final score and a Play Again button, if the player wants to play the game again.
- While the enemy generation stays the same over the course of the game, as the player eliminates each wave of enemies, the frequency of enemies shooting increases (i.e they start shooting more often).

## Controls
The controls for this remake are outlined below;
- space for shooting
- left arrow/a to move left
- right arrow/d to move right

## Settings.py
The **settings.py** file is used to contain various numerical values that are better not being hardcoded into the **classes.py** so anyone running the game can 'customise' aspects including:
- The starting player health and the health for each of the enemy types.
- The speed of the player, commony enemies, rare enemies and the projectiles.
- The points awarded for eliminating each kind of enemy.
- The damage given by projectiles produced by each of kind of enemy.
- Colours and other miscellaneous settings, including the size of the game window and a path to the assets folder. These are not to be changed as they will interfere with the functionality of the game.

## Usage
Prior to running the game do the following:
- make sure Pygame is installed, if not, run ```pip install pygame``` in the terminal/command line
- ensure that **classes.py** and **settings.py** are in the same directory as main.py, as well as the **Assets** folder, which contains all the sprite images.
- edit any settings you deem necessary in **settings.py** to customise your playing experience 

Finally, to start the game, run ```python main.py``` in the directory of the project.
