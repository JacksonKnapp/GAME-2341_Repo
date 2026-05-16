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
    tile_options = list(TILE_TYPES.keys())

    for r in range(TILES_X):
        for c in range(TILES_Y):
            x = TILES_START_X + (c * (TILE_SIZE + TILE_SPACING))
            y = TILES_START_Y + (r * (TILE_SIZE + TILE_SPACING))

            tile = Tile(x, y, TILE_SIZE)
            tile.type = random.choice(tile_options) #randomly chooses tile type while spawning from a list of options
            tile.set_image(unknown_tile)
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

def get_adjacent_tiles(Tile):

    global TILE_SIZE
    global TILE_SPACING

    pos = Tile.rect.center
    offsets = [(1,0),(0,1),(-1,0),(0,-1)]
    adjacent_tiles = pygame.sprite.Group()

    for x in range(4):
        ox, oy = offsets[x]
        offset = (ox * (TILE_SIZE + TILE_SPACING), oy * (TILE_SIZE + TILE_SPACING))
        for adjacent_tile in tiles_group:
            test_pos = (pos[0] + offset[0], pos[1] + offset[1])
            if adjacent_tile.rect.collidepoint(test_pos):
                debug("Found adjacent tile")
                adjacent_tiles.add(adjacent_tile)

    return adjacent_tiles

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

# Images
unknown_tile = pygame.image.load(DIR / "unknown_tile.png")
stone_tile = pygame.image.load(DIR / "stone_tile.png")
tullium_tile = pygame.image.load(DIR / "tullium_tile.png")
uranium_tile = pygame.image.load(DIR / "uranium_tile.png")
char = pygame.image.load(DIR / "char.png")
ui_img = pygame.image.load(DIR / "ui.png")

# Tiles
TILE_SIZE = 67
TILE_SPACING = 0
TILES_X = 10
TILES_Y = 10
TILES_START_X = ((SCREEN_WIDTH/2) - (((TILES_Y * TILE_SIZE) - (TILES_Y * TILE_SPACING))/2) - TILE_SIZE/2) + TILE_SIZE/1.25 #Calculates the start POS of tile 0 so that the tiles are centered when generated - X row
TILES_START_Y = ((SCREEN_HEIGHT/2) - (((TILES_Y * TILE_SIZE) - (TILES_Y * TILE_SPACING))/2) - TILE_SIZE/2) + 45 #Calculates the start POS of tile 0 so that the tiles are centered when generated - Y row
TILE_TYPES = {"Stone": stone_tile,"Uranium": uranium_tile,"Tullium": tullium_tile} #tile options

# Character
CHAR_SIZE = TILE_SIZE - 30
CHAR_INTERACT_DIST = 35
CHAR_SPEED = 5
CHAR_COOLDOWN_TIME = 2

# Game
DEATH_SPEED = 25

# colors
BLACK = (0,0,0)
GRAY = (120, 120, 120)
GREEN = (0, 200, 80)

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

    def update_image_by_type(self):
        if self.type in list(TILE_TYPES.keys()):
            self.set_image(TILE_TYPES[self.type])

      
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
                    
                    for adjacent_tile in get_adjacent_tiles(tile):
                        if adjacent_tile is not None:
                            adjacent_tile.update_image_by_type()

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
    
    def get_percent(self):
        return (time.time() - self.start_time) / self.duration
    
    def check_timer(self): # updates timer parameters, returns true if running, stops timer automatically
        self.running = time.time() < self.stop_time

        if not self.running: #redundant but may add stuff later
            self.stop()

        return self.running

class ProgressBar(Timer):

    def __init__(self, surface, x=0, y=0, width=50, height=5, duration=0, color=(100,100,100)):
        super().__init__() #initializes parent timer
        
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.duration = duration
        self.color = color
        self.percent = 0

    def update(self, x, y, percent): #updates progress bar percentage an draws it

        # uses the current position of the progress bar if none is given

        if x is None:
            x = self.x

        if y is None:
            y = self.y

        self.x = x
        self.y = y
        self.percent = percent
        self.draw_progress_bar()

    def check_progress(self): #calls the super class Timer's check timer function
        super().check_timer()

    def start(self, duration): #calls the super class Timer's start function
        super().start(duration)

    def stop(self): #calls the super class Timer's stop function
        super().stop()

    def draw_progress_bar(self):
        pygame.draw.rect(self.surface, 
                         ((self.color[0] - 75),(self.color[1] - 75),(self.color[2] - 75)),
                         (self.x - self.width/2, self.y - self.height/2, self.width, self.height)) #background

        fill = int(self.width * self.percent)
        pygame.draw.rect(self.surface, self.color, (self.x - self.width/2, self.y - self.height/2, fill, self.height)) #fill

class UserInterface:

    def __init__(self):
        self.death_progress = ProgressBar(screen,640,22,735,26,DEATH_SPEED,(150,150,150)) #sets death_progress bar settings

    def update_user_interface(self):
        self.draw_user_interface()

    def draw_user_interface(self):
        screen.blit(ui_img, (0,0))

        self.death_progress.update(None, None, 1 - self.death_progress.get_percent())

    def reset_death_progress(self):
        self.death_progress.start(DEATH_SPEED)

################### MAIN ##################

generate_tiles()
character = spawn_character()
character_progress_bar = ProgressBar(screen)
cooldown_timer = Timer()
ui = UserInterface()
ui.reset_death_progress()
   
while running: # Game loop
     
    # Game loop basics
    screen.fill(BLACK)
    tiles_group.draw(screen)
    screen.blit(character.image, character.rect)
    ui.draw_user_interface()

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
    # Checks if the character cooldown timer is active, if so- it updates the character_progress_bar object
    if cooldown_timer.check_timer():
        character_progress_bar.update(character.rect.centerx, character.rect.top - 10, 1 - cooldown_timer.get_percent()) #sets x, y, and percent using variables from the character and the cooldown timer

    pygame.display.flip()

pygame.quit() # Exit main loop and exit program