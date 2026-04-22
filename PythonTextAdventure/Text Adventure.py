
import random

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
                attempts -= 5
                print (f"That was not an available option! {attempts} attempts remaining until one is chosen for you!")
                