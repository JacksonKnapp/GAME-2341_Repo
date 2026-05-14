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

    types = ["Stone","Uranium","Tullium"] #tile options
    global tiles_group

    for r in range(TILES_X):
        for c in range(TILES_Y):
            x = TILES_START_X + (c * (TILE_SIZE + TILE_SPACING))
            y = TILES_START_Y + (r * (TILE_SIZE + TILE_SPACING))

            tile = Tile(x, y, TILE_SIZE)
            tile.type = random.choice(types) #randomly chooses tile type while spawning from a list of options
            tile.set_image(stone)
            tiles_group.add(tile)

def spawn_character():

    global character

    x = 100
    y = SCREEN_HEIGHT/2

    local_char = Character(x, y, CHAR_SIZE)
    local_char.set_image(char)
    return local_char

def detect_sprite_overlap(sprite_group, test_location):

    sprites = sprite_group.sprites()

    found_sprites = pygame.sprite.Group()
    
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
font = pygame.font.SysFont("consolas", 14)
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

# Character
CHAR_SIZE = TILE_SIZE - 30
CHAR_INTERACT_DIST = 35
CHAR_SPEED = 3
CHAR_COOLDOWN_TIME = 2

# colors
BLACK = (0,0,0)
GRAY = (120, 120, 120)
GREEN = (0, 200, 80)

# images
stone = pygame.image.load(DIR / "stone.png")
char = pygame.image.load(DIR / "char.png")

# classes

class Tile(pygame.sprite.Sprite):

    def __init__(self, x, y, size): #Constructor overrides Sprite class's constructor
        super().__init__() #initializes parent sprite

        self.size = size
        self.clicked = False

        self.image = pygame.Surface((size, size))
        self.image.fill(GRAY)

        self.rect = self.image.get_rect(topleft=(x, y))

        self.type = "Default"

    def set_image(self, new_image): #sets and updates the Tile sprite's image
        self.image = pygame.transform.scale(new_image,(self.size, self.size))
      
class Character(pygame.sprite.Sprite):

    last_key = None
    global tiles_group
     
    def __init__(self, x, y, size): #Constructor overrides Sprite class's constructor
        super().__init__() #initializes parent sprite

        self.size = size
        self.clicked = False

        self.image = pygame.Surface((size, size))
        self.image.fill(GRAY)

        self.rect = self.image.get_rect(topleft=(x, y))

    def set_image(self, new_image): #sets and updates the Character sprite's image
        self.image = pygame.transform.scale(new_image,(self.size, self.size))

    def move(self, tiles):
        keys = pygame.key.get_pressed() #gathers pressed keys

        x = 0
        y = 0

        if keys[pygame.K_a] and self.rect.left > 0: #left
            x = -CHAR_SPEED
            self.last_key = pygame.K_a
        if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH: #right
            x = CHAR_SPEED
            self.last_key = pygame.K_d
        if keys[pygame.K_w] and self.rect.top > 0: #up
            y = -CHAR_SPEED
            self.last_key = pygame.K_w
        if keys[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT: #down
            y = CHAR_SPEED
            self.last_key = pygame.K_s


        # Updates sprite position and checks if the sprites are colliding, moves back if so.
        self.rect.x += x
        if pygame.sprite.spritecollide(self, tiles, False):
            self.rect.x -= x
        
        self.rect.y += y
        if pygame.sprite.spritecollide(self, tiles, False):
            self.rect.y -= y

    def detect_tile(self):

        loc = None

        #offsets

        if self.last_key == pygame.K_a: #left
            loc = self.rect.centerx - CHAR_INTERACT_DIST, self.rect.centery
        if self.last_key == pygame.K_d: #right
            loc = self.rect.centerx + CHAR_INTERACT_DIST, self.rect.centery
        if self.last_key == pygame.K_w: #up
            loc = self.rect.centerx, self.rect.centery - CHAR_INTERACT_DIST
        if self.last_key == pygame.K_s: #down
            loc = self.rect.centerx, self.rect.centery + CHAR_INTERACT_DIST

        if loc is not None:
            pygame.draw.circle(screen, (255,0,0), loc, 5)
            tiles = detect_sprite_overlap(tiles_group,loc)
            return tiles
        
        return None
    
    def interact(self):
        keys = pygame.key.get_pressed() #gathers pressed keys

        if keys[pygame.K_SPACE]:
            tiles = self.detect_tile()
            if tiles is not None and not cooldown_timer.is_running():
                for tile in tiles:
                    debug((f"Destroying Tile...  Type: {tile.type}"), 5)
                    
                    tile.kill()
                    cooldown_timer.start(CHAR_COOLDOWN_TIME)

class Timer:

    def __init__(self, duration=3): #Constructor
        self.duration = duration
        self.start_time = 0
        self.stop_time = 0
        self.running = False

    def start(self, duration=3):
        self.start_time = time.time()
        self.duration = duration
        self.stop_time = self.start_time + self.duration
        self.running = True

    def stop(self):
        self.running = False #kinda useless

    def is_running(self):
        return self.running
    
    def check_timer(self): # updates timer parameters, returns true if running, stops timer automatically
        self.running = time.time() < self.stop_time

        if not self.running: #redundant but may add stuff later
            self.stop()

        return self.running

class ProgressBar(Timer):

    def __init__(self, surface, x, y, width=50, height=5, duration=0, color=(100,100,100)):
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.duration = duration
        self.color = color
        self.percent = 0

    def update(self, percent): #updates progress bar percentage an draws it
        self.percent = percent
        self.draw_progress_bar()

    def check_progress(self): #calls the super class Timer's check timer function
        super.check_timer(self)

    def start(self, duration): #calls the super class Timer's start function
        super.start(self, duration)

    def stop(self): #calls the super class Timer's stop function
        super.stop(self)

    def draw_progress_bar(self):
        pygame.draw.rect(self.surface, self.color - 75, (self.x, self.y, self.width, self.height)) #background

        fill = int(self.width * self.percent)
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height)) #fill

################### MAIN ##################

generate_tiles()
character = spawn_character()
cooldown_timer = Timer()

while running: # Game loop
     
    # Game loop basics
    screen.fill(BLACK)
    tiles_group.draw(screen)
    screen.blit(character.image, character.rect)

    # Handles debug messages
    for index, debug_message in enumerate(debug_messages):
        if time.time() < debug_message["expire_time"]:
            surface = font.render(debug_message["text"], True, (255,255,255))
            screen.blit(surface, (debug_message["x"], debug_message["y"] + (25 * index)))
        else:
            debug_messages.remove(debug_message)

    # Handles pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Handles player clicking exit 
            running = False

    # Character
    character.move(tiles_group)
    character.interact()
    cooldown_timer.check_timer()

    pygame.display.flip()

pygame.quit() # Exit main loop and exit program