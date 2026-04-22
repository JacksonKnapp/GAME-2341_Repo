
import random
import json

# A function to validate input and make sure that an option that is chosen is valid
def validate_input(options_result_dict, prompt):
    attempts = 5
    while True:
        try:
            user_input = input(prompt)
            if user_input in options_result_dict:
                # if the given choice is present in the options, return the associated key value pair
                choice = options_result_dict.get(user_input)
                return choice
            else:
                raise ValueError
        except ValueError:
            if attempts <= 0:
                len(options_result_dict)
                # a random choice is made and returned
                choice = random.choice(list(options_result_dict.values()))
                return choice
            else:
                attempts -= 1
                print (f"That was not an available option! {attempts} attempts remaining until one is chosen for you!")

# Removes all present console output and prints the provided prompt
def flush_print(prompt):
    print(prompt, end = "   ", flush = True)

# Prints location details by a given location
def print_location_details(location):
    try:
        #builds a string to pass onto a single print option that flushes the console
        string = ""
        desc = adventure["locations"][f"{location}"]["description"]
        choices = adventure["locations"][f"{location}"]["choices"]
        string = f"{location}:\n\n{desc}\n"
        
        for choice, info in choices.items():
            desc = info["choice_description"]
            dest = info["destination"]
            string += f"\n{choice}\t| {desc}\t\tLeads to: {dest}"
        flush_print(string)
        return choices
    except Exception as e:
        print("Error: {e}")

gameover = False

# Loads adventure JSON file
try: 
    with open ("GAME-2341_Repo/PythonTextAdventure/adventure_tree.JSON", "r") as file:
        adventure = json.load(file)
except FileNotFoundError:
    print("Error: adventure_tree.JSON file not found!")
    gameover = True

# Sets beginning parameters
current_location = "Start"
print("\n\n\t============ Text Adventure ===========\n\n")

# Game loop
while gameover == False:
    
    choices = print_location_details(current_location)

    choice = validate_input(choices,"\n\nChoice: ")






# Game finished
print("Game ended!")