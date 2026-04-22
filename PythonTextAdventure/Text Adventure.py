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
def validate_input_by_choice(choices, p):
    prompt = p
    attempts = 5
    while True:
        try:
            user_input = input(prompt).lower()

            lower_choices = [c.lower() for c in choices] # converts all choices to lower-case

            # attempts to find the closest match
            matches = difflib.get_close_matches(user_input, lower_choices, n = 1, cutoff = 0.6)
            match = matches[0]

            # Checks to see if the match exists in the available choices
            if match in lower_choices:
                # if the given choice is present in the options, return the associated key value pair
                choice = f"{match.title()}"
                return choice
            
            else:
                # splits the input into words and compares them against the options
                user_input_split = user_input.split()
                for c in lower_choices:
                    choices_split = c.split() # a list of words in the choice option.
                    for u in user_input_split:
                        split_matches = difflib.get_close_matches(u, choices_split, n = 1, cutoff = 0.6)
                        if len(split_matches) > 0:
                            return c.title()

            raise ValueError # raises error only if no match is found by either method

        except Exception:
                anim_print(f"\nThat was not an available option!````",1)
                clear_console()
                print_location_details(current_location, False)



# Removes all present console output and prints the provided prompt
def flush_print(prompt):
    clear_console()
    print_header()
    anim_print(prompt,1)


# Header
def print_header():
    # Prints header line after the console has been cleared
    width = os.get_terminal_size().columns * .8
    print(f"\n=============================== Text Adventure {"=" * int(width)}\n")


# Clears console instantly
def clear_console():
    # prints either in case of os.system deprecation
    if os.name == "nt":
        os.system("cls")
    else:
        print("\033[2J\033[H", end="")


# a function used to animate a print operation to console
def anim_print(prompt, delay_modifier):
    for char in prompt:
        if char == '`': # checks each character for the special ` marker, denoting a longer delay (75x longer by default)
            time.sleep(TEXT_ANIM_DELAY * 75 * delay_modifier)
        else:
            print(char, end = "", flush = True)
            time.sleep(TEXT_ANIM_DELAY * delay_modifier)


# Prints location details by a given location
def print_location_details(location, animate):
    try:
        #builds a string to pass onto a single print option that flushes the console
        string = ""
        desc = adventure["locations"][f"{location}"]["description"]
        choices = adventure["locations"][f"{location}"]["choices"]
        string = f"{location}:\n\n{desc}```\n"
        string += f""
        
        for choice, info in choices.items():
            desc = info["choice_description"]
            dest = info["destination"]
            if "ending" in dest.lower():
                dest = "Unknown"
            string += f"\n{choice:<30}\t| {desc:<100}Leads to: {dest}`"

        # checks if the print should be animated or not
        if animate:
            flush_print(string)
            return choices
        
        # non-animated print
        print_header()
        altered_string = string.replace("`", "")  # alters the string to remove the "`" character
        print(altered_string, end = "", flush = True)
        return None
    
    except Exception as e:
        print(f"Error: {e}")

# intro sequence at the game start
def intro():
    clear_console()
    intro_string = "Text Adventure\n\nAre you ready to begin?\n\nEnter 'Yes' to play: "
    anim_print(intro_string, 1)
    while True:
        try:
            user_input = input().lower()
            matches = difflib.get_close_matches(user_input, ["yes"], n = 1, cutoff = 0.6)
            match = matches[0]
            if match is not None:
                break
        except:
            clear_console()
            anim_print("Incorrect input, resetting...`````", 1)
            clear_console()
            anim_print(intro_string,1)
    
    clear_console()
    print_header()

    # intro paragraph
    anim_print("You awaken beneath a broken Metro entrance. Dust floats through beams of sunlight. " \
    "Your make-shift torch lies on the concrete beside you, ruined by last night's rain. " \
    "The cold from sleeping on bare stone still clings to your bones.``\n\nAs you rise, " \
    "the loss of your bag flashes across your mind, almost as in a vision. You remember how " \
    "little you have now. Most truly was lost from just the past few days``\n\nPress anything to continue...",2)
    input()

def game_ended(choice):
    clear_console()
    print_header()
    string


# Sets beginning parameters
gameover = False
current_location = "Destroyed Metro" # Starting location
TEXT_ANIM_DELAY = .003 # adjusts the speed of the scrolling text output to console 


# Loads adventure JSON file, ends the game if the JSON is not found- as then there is no game anyway :)
try: 
    with open ("GAME-2341_Repo/PythonTextAdventure/adventure_tree.JSON", "r") as file:
        adventure = json.load(file)
except FileNotFoundError:
    print("Error: adventure_tree.JSON file not found!")
    gameover = True

intro()

# Game loop
while gameover == False:
    
    choices = print_location_details(current_location, True)

    choice = validate_input_by_choice(choices,"\n\nChoice: ")

    for c, info in choices.items():
            if c.lower() == choice.lower():
                dest = info["destination"]
                current_location = dest
    
    if "ending" in current_location.lower():
        clear_console()
        print("GAME FINISHED!")
        game_ended(current_location)
        input()







# Game finished
print("Game ended!")