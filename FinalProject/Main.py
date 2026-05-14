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

def debug(text, duration=0, x_pos=10, y_pos=10):

    debug_expire_time = time.time() + duration

    try:
        debug_messages.append({
            "text": str(text),
            "expire_time": debug_expire_time,
            "x": x_pos,
            "y": y_pos 
        })
    except Exception as e:
        print(f"Error: {e}")

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

def spawn_character():

    global character

    x = 100
    y = SCREEN_HEIGHT/2

    local_char = Character(x, y, TILE_SIZE - 20)
    local_char.set_image(char)
    return local_char

def detect_sprite_overlap(sprite_group, test_location):

    sprites = pygame.sprite.Group
    sprites = sprite_group

    found_sprites = pygame.sprite.Group
    
    for sprite in sprites:
        if sprite.rect.collidepoint(test_location):
            found_sprites.add(sprite)

    return found_sprites

# pygame settings/init

DIR = load_directory() #directory

pygame.init()

# Defaults
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
font = pygame.font.Font(None, 24)
pygame.display.set_caption("Reactor")
tiles_group = pygame.sprite.Group()
debug_messages = []

running = True # game loop variable

# Tiles
TILE_SIZE = 65
TILE_SPACING = 4
TILES_X = 10
TILES_Y = 10
TILES_START_X = (SCREEN_WIDTH/2) - (((TILES_Y * TILE_SIZE) - (TILES_Y * TILE_SPACING))/2) - TILE_SIZE/2 #Calculates the start POS of tile 0 so that the tiles are centered when generated - X row
TILES_START_Y = (SCREEN_HEIGHT/2) - (((TILES_Y * TILE_SIZE) - (TILES_Y * TILE_SPACING))/2) - TILE_SIZE/2 #Calculates the start POS of tile 0 so that the tiles are centered when generated - Y row

# colors
BLACK = (0,0,0)
GRAY = (120, 120, 120)
GREEN = (0, 200, 80)

# images
stone = pygame.image.load(DIR / "stone.png")
char = pygame.image.load(DIR / "char.png")

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
      
class Character(pygame.sprite.Sprite):

    last_key = None
    global tiles_group
     
    def __init__(self, x, y, size): #overrides the Sprite classes' __init__ function
        super().__init__() #initializes parent sprite

        self.size = size
        self.clicked = False

        self.image = pygame.Surface((size, size))
        self.image.fill(GRAY)

        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed = 5 #initializes character movement speed and variable

    def set_image(self, new_image): #sets and updates the Character sprite's image
        self.image = pygame.transform.scale(new_image,(self.size, self.size))

    def move(self, tiles):
        keys = pygame.key.get_pressed() #gathers pressed keys

        x = 0
        y = 0

        if keys[pygame.K_a] and self.rect.left > 0: #left
            x = -self.speed
            self.last_key = pygame.K_a
        if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH: #right
            x = self.speed
            self.last_key = pygame.K_d
        if keys[pygame.K_w] and self.rect.top > 0: #up
            y = -self.speed
            self.last_key = pygame.K_w
        if keys[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT: #down
            y = self.speed
            self.last_key = pygame.K_s


        # Updates sprite position and checks if the sprites are colliding, moves back if so.
        self.rect.x += x
        if pygame.sprite.spritecollide(self, tiles, False):
            self.rect.x -= x
        
        self.rect.y += y
        if pygame.sprite.spritecollide(self, tiles, False):
            self.rect.y -= y

    def detect_tile(self):

        debug("Detecting Tile", 5)

        loc = None

        if self.last_key == pygame.K_a:
            loc = self.rect.centerx - 50
            print("last key a")
        if self.last_key == pygame.K_d:
            print("last key d")
            loc = self.rect.centerx - 50
        if self.last_key == pygame.K_w:
            print("last key w")
            loc = self.rect.centery - 50
        if self.last_key == pygame.K_s:
            print("last key s")
            loc = self.rect.centery + 50

        if loc is not None:
            tiles = detect_sprite_overlap(tiles_group,loc)
            return tiles
        
        return None
    
    def interact(self):
        keys = pygame.key.get_pressed() #gathers pressed keys

        if keys[pygame.K_SPACE]:
            tiles = self.detect_tile()
            if tiles is not None:
                for tile in tiles:
                    tile.kill()
    
################### MAIN ##################

generate_tiles()
character = spawn_character()

while running:

    # Handles debug messages
    for debug in debug_messages:
        if time.time() < debug["expire_time"]:
            surface = font.render(debug["text"], True, (255,255,255))
            screen.blit(surface, (debug["x"], debug["y"]))
        else:
            debug_messages.remove(debug)


    # Handles pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Handles player clicking exit 
            running = False

    screen.fill(BLACK)
    tiles_group.draw(screen)
    screen.blit(character.image, character.rect)
    character.move(tiles_group)
    character.interact()

    pygame.display.flip()

pygame.quit() # Exit main loop and exit program