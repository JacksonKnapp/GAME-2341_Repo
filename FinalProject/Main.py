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
        if sprite.rect.collidepoint(test_location) and sprite.collision is True:
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

def ease_out(anim_time): #animation curve
    alpha = min(anim_time,1)
    curve = 1 -(1 - alpha) ** 2
    return curve

def overshoot(anim_time):
    alpha = min(anim_time,1)
    curve = (1 + 4 * alpha) * ((1 - alpha) ** 2)
    return curve
    

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
animations = []
tool_tip = None

running = True # game loop variable

# Images
unknown_tile = pygame.image.load(DIR / "unknown_tile.png")
stone_tile = pygame.image.load(DIR / "stone_tile.png")
tullium_tile = pygame.image.load(DIR / "tullium_tile.png")
uranium_tile = pygame.image.load(DIR / "uranium_tile.png")
char = pygame.image.load(DIR / "char.png")
ui_img = pygame.image.load(DIR / "ui.png")
tullium = pygame.image.load(DIR / "tullium.png")
uranium = pygame.image.load(DIR / "uranium.png")

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
        self.base_size = self.size
        self.clicked = False

        self.image = pygame.Surface((size, size))
        self.image.fill(GRAY)

        self.rect = self.image.get_rect(topleft=(x, y))

        self.type = "Default"
        self.animation_state = None
        self.anim_time = 0
        self.collision = True


    def set_image(self, new_image): #sets and updates the Tile sprite's image
        self.original_image = new_image
        self.image = pygame.transform.scale(self.original_image,(self.size, self.size))
        self.rect = self.image.get_rect(center=self.rect.center)

    def update_image_by_type(self):
        if self.type in list(TILE_TYPES.keys()):
            self.set_image(TILE_TYPES[self.type])

    def animate(self, animation=None):

        if animation is not None:
            self.animation_state = animation
            animations.append(self)
            animating = False
        else:
            animating = True

        match self.animation_state:
            case "deflate":
                self.anim_time += 0.1
                self.size = self.base_size * ease_out(self.anim_time)
            case "overshoot":
                self.anim_time += 0.1
                self.size = self.base_size * overshoot(self.anim_time)

        if animating:
            debug(self.size)
            if (int(self.size * 2))/2 == 0 and self in animations:
                animations.remove(self)
                self.kill() #removes tile once animation is complete

        center = self.rect.center
        self.image = pygame.transform.smoothscale(self.original_image,(int(self.size), int(self.size)))
        self.rect = self.image.get_rect(center = center)
      
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


        collideable_tiles = [tile for tile in tiles if tile.collision] #transforms tiles_group into a list of tiles that are collideable

        # Updates sprite position and checks if the sprites are colliding, moves back if so.
        self.rect.x += x
        if pygame.sprite.spritecollide(self, collideable_tiles, False):
            self.rect.x -= x
        
        self.rect.y += y
        if pygame.sprite.spritecollide(self, collideable_tiles, False):
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

                    tile.animate("overshoot")
                    tile.collision=False
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
        self.construct_reactor_button = Button(1055, 625, 160, 50, "Construct Reactor", font, "You need 10 Uranium to construct a reactor")
        self.relocate_button = Button(1055, 530, 160, 50, "Relocate", font, "You need 5 Uranium to relocate")
        self.recycle_tullium_button = Button(1055, 475, 160, 50, "Recycle Tullium", font, "You need 10 Tullium to recycle")
        self.construct_reactor_button.enabled = False

    def update_user_interface(self):
        self.draw_user_interface()

    def draw_user_interface(self):
        screen.blit(ui_img, (0,0))

        self.death_progress.update(None, None, 1 - self.death_progress.get_percent())
        self.construct_reactor_button.draw(screen)
        self.relocate_button.draw(screen)
        self.recycle_tullium_button.draw(screen)

        if tool_tip:
            tool_tip.draw(screen)

    def reset_death_progress(self):
        self.death_progress.start(DEATH_SPEED)

class Button:
     
    def __init__(self, x, y, width, height, text, font, tooltip_text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.tooltip_text = tooltip_text
        self.font = font
        self.color = (80, 80, 80)
        self.hover_color = (120, 120, 120)
        self.text_color = (255, 255, 255)
        self.disabled_color = (255, 120, 120)
        self.disabled_hover_color = (200, 60, 60)
        self.enabled = True
        self.ToolTip_object = None

    def draw(self, surface):

        mouse_pos = pygame.mouse.get_pos()
        global tool_tip

        if self.rect.collidepoint(mouse_pos):
            if self.enabled:
                color = self.hover_color
                if self.ToolTip_object:
                    del self.ToolTip_object
            else:
                color = self.disabled_hover_color
                if not self.ToolTip_object:
                    x, y = pygame.mouse.get_pos()
                    self.ToolTip_object = ToolTip(x, y, 450, 50, self.tooltip_text, font)
                else:
                    tool_tip = self.ToolTip_object
        else:
            if self.ToolTip_object:
                    self.ToolTip_object = None
                    tool_tip = None
            if self.enabled:
                color = self.color
                
            else:
                color = self.disabled_color

        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rest.collidepoint(event.pos)
        )

class ToolTip:

    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = (60, 60, 60)
        self.text_color = (255, 255, 255)

    def draw(self, surface):
        x, y = pygame.mouse.get_pos()
        y -= 25 
        mouse_pos = (x,y)

        self.rect.bottomright = mouse_pos

        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    
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


    # Handles animnation events
    for target in animations[:]:
        target.animate()

    # Character
    character.move(tiles_group)
    character.interact()
    # Checks if the character cooldown timer is active, if so- it updates the character_progress_bar object
    if cooldown_timer.check_timer():
        character_progress_bar.update(character.rect.centerx, character.rect.top - 10, 1 - cooldown_timer.get_percent()) #sets x, y, and percent using variables from the character and the cooldown timer

    pygame.display.flip()

pygame.quit() # Exit main loop and exit program