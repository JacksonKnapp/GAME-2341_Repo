# Name: Jackson Knapp
# Date: 5/11/26
# Description:

# imports
import sys
import pygame
import random
import math
import time
from pathlib import Path

# functions

def load_directory(): #function to load data from a directory, handles file not found exception
    try: 
        directory = Path(__file__).parent #stores the current folder of the Main.py file
        return directory
    except FileNotFoundError as e:
        print(f"Error - File not found: {e}") #file not found error for if the directory folder cannot be found
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def generate_tiles():

    global tiles_group

    for r in range(TILES_X):
        for c in range(TILES_Y):
            x = TILES_START_X + (c * (TILE_SIZE + TILE_SPACING))
            y = TILES_START_Y + (r * (TILE_SIZE + TILE_SPACING))

            tile = Tile(x, y, TILE_SIZE)
            tile.set_image(stone)
            tiles_group.add(tile)

# pygame settings/init

DIR = load_directory() #directory

pygame.init()

# Defaults
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Reactor")
tiles_group = pygame.sprite.Group()
running = True

# Tiles
TILE_SIZE = 75
TILE_SPACING = 4
TILES_X = 10
TILES_Y = 10
TILES_START_X = (SCREEN_WIDTH/2) - ((TILES_X * TILE_SIZE)/2) - TILE_SIZE/2 #Calculates the start POS of tile 0 so that the tiles are centered when generated - X row
TILES_START_Y = (SCREEN_HEIGHT/2) - ((TILES_Y * TILE_SIZE)/2) - TILE_SIZE/2 #Calculates the start POS of tile 0 so that the tiles are centered when generated - Y row

# colors
BLACK = (0,0,0)
GRAY = (120, 120, 120)
GREEN = (0, 200, 80)

# images
stone = pygame.image.load(DIR / "stone.png")

# classes

class Tile(pygame.sprite.Sprite):

    def __init__(self, x, y, size): #overrides the Sprite classes' __init__ function
        super().__init__() #initializes parent sprite

        self.size = size
        self.clicked = False

        self.image = pygame.Surface((size, size))
        self.image.fill(GRAY)

        self.rect = self.image.get_rect(topleft=(x, y))

    def set_image(self, new_image): #sets and updates the Tile sprite's image
        self.image = pygame.transform.scale(new_image,(self.size, self.size))
      

    
################### MAIN ##################

generate_tiles()

while running:

    # Handles pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Handles player clicking exit 
            running = False

    screen.fill(BLACK)
    tiles_group.draw(screen)

    pygame.display.flip()

pygame.quit() # Exit main loop and exit program