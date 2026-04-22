# Name: Jackson Knapp
# Date: 4/21/26
# Description:

# Notes: 
#   the character ` is used in constructed output strings to denote a longer delay in the anim_print() function
#
#


import random
import json
import difflib # used to find comparable words
import os
import time # used for animated text

# A function to validate input and make sure that an option that is chosen is valid
def validate_input(choices, prompt):
    attempts = 5
    while True:
        try:
            user_input = input(prompt).lower()
            lower_choices = [c.lower() for c in choices]
            matches = difflib.get_close_matches(user_input, lower_choices, n = 1, cutoff = 0.6)
            match = matches[0]
            if match in lower_choices:
                # if the given choice is present in the options, return the associated key value pair
                choice = f"{match.title()}"
                return choice
            else:
                raise ValueError
        except Exception:
            if attempts <= 0:
                len(choices)
                # a random choice is made and returned
                choice = random.choice(list(choices.values()))
                return choice
            else:
                attempts -= 1
                anim_print(f"That was not an available option! {attempts} attempts remaining until one is chosen for you!")



# Removes all present console output and prints the provided prompt
def flush_print(prompt):
    # prints either in case of os.system deprecation
    if os.name == "nt":
        os.system("cls")
    else:
        print("\033[2J\033[H", end="")

    # Prints header line after the console has been cleared
    width = os.get_terminal_size().columns * .8
    print(f"\n=============================== Text Adventure {"=" * int(width)}\n")
    anim_print(prompt)

# a function used to animate a print operation to console
def anim_print(prompt):
    for char in prompt:
        if char == '`': # checks each character for the special ` marker, denoting a longer delay (75x longer)
            time.sleep(TEXT_ANIM_DELAY * 75)
        else:
            print(char, end = "", flush = True)
            time.sleep(TEXT_ANIM_DELAY)


# Prints location details by a given location
def print_location_details(location):
    try:
        #builds a string to pass onto a single print option that flushes the console
        string = ""
        desc = adventure["locations"][f"{location}"]["description"]
        choices = adventure["locations"][f"{location}"]["choices"]
        string = f"{location}:\n\n{desc}```\n"
        
        for choice, info in choices.items():
            desc = info["choice_description"]
            dest = info["destination"]
            string += f"\n{choice}\t| {desc}\t\tLeads to: {dest}`"
        flush_print(string)
        return choices
    except Exception as e:
        print(f"Error: {e}")



# Sets beginning parameters
gameover = False
current_location = "Destroyed Metro" # Starting location
TEXT_ANIM_DELAY = .003 # adjusts the speed of the scrolling text output to console


# Loads adventure JSON file
try: 
    with open ("GAME-2341_Repo/PythonTextAdventure/adventure_tree.JSON", "r") as file:
        adventure = json.load(file)
except FileNotFoundError:
    print("Error: adventure_tree.JSON file not found!")
    gameover = True



# Game loop
while gameover == False:
    
    choices = print_location_details(current_location)

    choice = validate_input(choices,"\n\nChoice: ")
    current_location = choice






# Game finished
print("Game ended!")