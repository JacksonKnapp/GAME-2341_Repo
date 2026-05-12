# Name: Jackson Knapp
# Date: 5/11/26
# Description:

#imports
import sys
import pygame
import random
import math
import time
from pathlib import Path

#global pygame settings
width = 1280
height = 720
size = (width, height)
screen = pygame.display.set_mode(size)

#functions

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

def get_directory_data(path): #gets directory data via path, handles generic exception
    try:
        data = load_directory() / path
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None