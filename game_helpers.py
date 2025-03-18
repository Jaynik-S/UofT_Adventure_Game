"""UofT Adventure Game - Helper Functions
"""
from game_entities import Location
import time

char_delay = 0

def game_begin_msg() -> None:
    """
    Display the introductory game message and set up the typewriter effect based on user input.
    """
    global char_delay
    char_delay = 0.0225
    tw_print("Before we begin, do you want to enable this typewriter effect ('yes' or 'no')?")
    typewriter_effect = input().strip().lower()
    if typewriter_effect == 'yes':
        try:
            char_delay = float(input("Enter the character delay in seconds (fast: 0.01, recommended: 0.0225): ").strip())
        except ValueError:
            char_delay = 0.0225
    else:
        char_delay = 0

    tw_print("\nYou wake up with a start in your dorm room, heart racing.")
    tw_print("What was supposed to be a quick 15-minute power nap has turned into a 5-hour slumber.")
    tw_print("Groggily, you glance at the clock—time is slipping away, and your final assignment is due soon.")
    tw_print("You need a perfect score to secure the grade you've been aiming for all semester.\n")

    tw_print("Still half-asleep, you reach for your laptop, only to discover it's completely dead.")
    tw_print(col_r("Panic sets in as you spot your special one-of-a-kind laptop charger lying on the floor... utterly destroyed."))
    tw_print("The wires are frayed, and the casing is shattered. Without it, your assignment might as well be doomed.\n")

    tw_print("Determined, you muster every ounce of resolve. Somewhere on campus are the tools and items you need to repair the charger.")
    tw_print("But it won't be easy. As you navigate the campus and interact with others, your good deeds and problem-solving skills will determine how close you come to success.")
    tw_print("Your predicted score will improve with each good deed, and you'll need to achieve a perfect 100 score to save your semester.\n")

    tw_print("Be careful, though—your energy starts at 100 but will drain as you travel from location to location and pick up or deposit items.")
    tw_print(col_r("If your energy runs out, it's game over.") + " Luckily, there are items hidden across campus that can bring you back to full energy—if you can find them.\n")

    tw_print("To make things trickier, your backpack is quite small and can only carry five items at once.")
    tw_print("You'll need to think strategically about what to carry and what to leave behind.")
    tw_print("But perhaps there's a way to get a bigger backpack if you look in the right places.\n")

    tw_print("The clock is ticking. Your friend is counting on you.")
    tw_print(col_g("Can you fix your charger, finish your assignment, and save the day?"))
    tw_print("The journey begins now—your choices, your actions, and your timing will decide your fate.")

    help_msg()

def help_msg() -> None:
    """
    Display the help message with available commands and their descriptions.
    """
    tw_print('\n========\n')
    tw_print("You can use the following commands:\n")
    tw_print(col_b("go [direction]") + " - to move to a different location (north, south, east, west)")
    tw_print(col_b("look") + " - to look around the current location")
    tw_print(col_b("inventory") + " - to display the items in your inventory")
    tw_print(col_b("undo") + " - reverse the most recent command and any associated changes to the game")
    tw_print(col_b("log") + " - list of all the events (locations visited, commands chosen) in order")
    tw_print(col_b("score") + " - to display your current score")
    tw_print(col_b("stamina") + " - to display your current stamina")
    tw_print(col_b("quit") + " - to quit the game")
    tw_print(col_b("help") + " - to display this message\n")
    tw_print("In addition, you can use the following commands at certain locations based on inventory:")
    tw_print(col_b("take") + " - to take an item from the current location")
    tw_print(col_b("deposit") + " - to deposit an item from your inventory at the current location")
    tw_print(col_b("drop") + " - to drop an item from your inventory at the current location")
    

def validate_choice(choice: str, loc: Location, menu: list[str] = [], valid_choices: list[str] = []) -> str:
    """
    Validate the user's choice against a list of valid choices or menu options.

    :param choice: The user's input choice.
    :param loc: The current location object.
    :param menu: A list of menu options.
    :param valid_choices: A list of valid choices.
    :return: The validated choice.
    """
    if valid_choices:
        while choice not in valid_choices:
            tw_print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()
    elif menu:
        while choice not in menu:
            tw_print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()
    else:
        while choice not in loc.available_movements:
            tw_print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()
    return choice

def col_r(text: str) -> str:
    """
    Return the text wrapped in red ANSI color codes.

    :param text: The text to color.
    :return: The colored text.
    """
    return f"\033[91m{text}\033[0m"

def col_g(text: str) -> str:
    """
    Return the text wrapped in green ANSI color codes.

    :param text: The text to color.
    :return: The colored text.
    """
    return f"\033[92m{text}\033[0m"

def col_b(text: str) -> str:
    """
    Return the text wrapped in blue ANSI color codes.

    :param text: The text to color.
    :return: The colored text.
    """
    return f"\033[94m{text}\033[0m"

def col_y(text: str) -> str:
    """
    Return the text wrapped in yellow ANSI color codes.

    :param text: The text to color.
    :return: The colored text.
    """
    return f"\033[93m{text}\033[0m"

def tw_print(text: str) -> None:
    """
    Print text character by character with a delay.

    :param text: The full text to display.
    """
    global char_delay
    if (char_delay == 0):
        print(text)
    else:
        for char in text:
            print(char, end='', flush=True)
            time.sleep(char_delay)
        print()
    
if __name__ == "__main__":
    pass
