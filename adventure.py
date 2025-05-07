"""UofT Adventure Game - Game Manager
"""
from __future__ import annotations
import json
from typing import Optional

from game_entities import Location, Item
from game_helpers import game_begin_msg, help_msg, validate_choice, col_r, col_g, col_b, col_y, tw_print
from event_logger import EventList

class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - current_location_id: The current location ID of the player in the game.
        - inventory: A mapping of the items name to the actual item in the player's inventory.
        - ongoing: A boolean indicating whether the game is ongoing or not.
        - stamina: The player's stamina level, if stamina reaches 0 the game ends.
        - score: The player's score in the game.
        - inventory_size: The maximum number of items the player can carry.

    Representation Invariants:
        - 0 <= stamina <= 100
        - score >= 0
        - current_location_id in self._locations
        - all(item.start_position and item.target_position in self._locations for item in self._items)
        - _location != {}
        - _items != []
        - inventory_size > 0
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int 
    inventory: dict[str, Item]
    ongoing: bool
    stamina: int
    score: int 
    inventory_size: int

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """
        # Load game data from the JSON file
        self._locations, self._items = self._load_game_data(game_data_file)

        # Set initial game state
        self.current_location_id = initial_location_id
        self.inventory = {}
        self.ongoing = True
        self.stamina = 100 
        self.score = 0
        self.inventory_size = 5
        
        # Add items to their respective locations
        self.add_items_to_locations()

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        # Open and read the JSON file
        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        # Parse locations from the JSON data
        locations = {}
        for loc_data in data['locations']:  
            location_obj = Location(loc_data['id'], loc_data['name'], loc_data['brief_description'], loc_data['long_description'],
                    loc_data['available_movements'], loc_data['take_actions'], loc_data['use_actions'])
            locations[loc_data['id']] = location_obj

        # Parse items from the JSON data
        items = []
        for item_data in data['items']:
            item_obj = Item(item_data['name'], item_data['description'], item_data["quest_description"], item_data["quest_completed_description"],
                    item_data['pickup_points'], item_data['use_points'], item_data['pickup_stamina_usage'], item_data['use_stamina_usage'])
            items.append(item_obj)

        return locations, items

    def add_items_to_locations(self) -> None:
        """Add items to their respective locations."""
        # Create a dictionary of items for quick lookup
        item_dict = {item.name: item for item in self._items}
        
        # Assign items to their respective locations based on take and use actions
        for location in self._locations.values():
            location.items_present = {name: item_dict[name] for name in location.take_actions if name in item_dict}
            location.items_use = {name: item_dict[name] for name in location.use_actions if name in item_dict}
                    

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        if loc_id is None:
            return self._locations[self.current_location_id]
        else:
            return self._locations[loc_id]

if __name__ == "__main__":
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)

    # Initialize the game log and game instance
    game_log = EventList() 
    game = AdventureGame('game_data.json', 1)  
    base_menu = ["go", "look", "inventory", "score", "undo", "log", "stamina", "help", "quit"]
    choice = None
    game_begin_msg()

    # Main game loop
    while game.ongoing and game.stamina > 0:
        # Display location information
        location = game.get_location()
        game_log.add_event_to_log(game, choice)
        
        if location.visited:
            tw_print('\n========\n')
            tw_print(f"{col_y(location.id_num)}: {col_g(location.name.upper())}")
            tw_print(location.brief_description + "\n")
        else:
            tw_print('\n========\n')
            tw_print(f"{col_y(location.id_num)}: {col_g(location.name.upper())}")
            tw_print(location.long_description + "\n")
            location.visited = True
        
        
        # Check if the player has met any of the winning conditions
        if game.score >= 100 and game.current_location_id == 1 and "fixed laptop charger" in game.inventory:
            game.ongoing = False
            tw_print(col_g("Congratulations! You have fixed your laptop charger and have plenty of time to complete your assignment, and I have a feeling after all your hard work you get the score you desire."))
            break
        elif game.score >= 100:
            tw_print(col_g("You have enough points to get your desired score, but your laptop charger is still broken. There might be some items you need to find to fix it."))
        elif "fixed laptop charger" in game.inventory:
            tw_print(col_g("You have the fixed laptop charger, but you need more points to get your desired score."))
        elif game.score >= 100 and "fixed laptop charger" in game.inventory:
            tw_print(f"{col_g('You have everything required to complete your assignment. Return to')} {col_y(game.get_location(1).name)} {col_g('to submit your assignment finish your journey.')}")
        
        # Check if the player can create the fixed laptop charger
        required_items = {"soldering iron", "broken laptop charger", "electrical tape", "screwdriver kit"}
        if game.current_location_id == 6 and required_items.issubset({item for item in game.inventory}):
            for item in required_items:
                game.inventory.pop(item)
            fixed_laptop_charger = Item("fixed laptop charger","","Your special laptop charger that is now fully functional","", 0, 0, 0, 0)

            game.inventory["fixed laptop charger"] = fixed_laptop_charger
            tw_print("You have successfully fixed your laptop charger!")
        elif required_items.issubset({item for item in game.inventory}): 
            tw_print("You have all the items needed to fix your laptop charger, but you need to be at the correct location to complete the game. A lab might be a good place to fix your laptop charger.")

        turn_taken = False # only loops if main action command is used (go, undo, take, deposit, drop)

        while not turn_taken:
            menu = base_menu.copy()
            
            # Check if there are items to deposit at this location
            if any(item_name in game.inventory for item_name in location.items_use):
                menu.append("deposit")
                tw_print(f"*This seems like a good spot to deposit: {col_y(', '.join(location.items_use.keys()))}*")

            # Check if the player can take more items
            if location.items_present and len(game.inventory) >= game.inventory_size:
                tw_print(f"*You can't take any more items. You must drop an item to take another.*")
            elif location.items_present:
                menu.append("take")
                tw_print(f"*Available items to take: {col_y(', '.join(location.items_present.keys()))}*")

            # Check if the player can drop items
            if game.inventory != {}:
                menu.append("drop")

            tw_print("\nWhat do you want to do? Choose from: " + ", ".join(menu))

            # Get the player's choice and validate it
            choice = input("\nEnter action: ").lower().strip()
            choice = validate_choice(choice, location, menu)

            tw_print("========")
            tw_print("You decided to: " + choice)

            # Process the player's choice
            if choice == "go":
                for action in location.available_movements:
                    tw_print("- " + action)
                choice = input("\nEnter action: ").lower().strip()
                choice = validate_choice(choice, location)
                game.stamina -= 3 # reduce stamina for traveling to location
                result = location.available_movements[choice]
                game.current_location_id = result
                turn_taken = True
                    
            elif choice == "look":
                tw_print(f"{location.id_num}: {location.name.upper()}")
                tw_print(location.long_description + "\n")

            elif choice == "inventory":
                if game.inventory == {}: 
                    tw_print(col_r("Your inventory is empty."))
                else:
                    for name in game.inventory:
                        tw_print(f'{col_b(name)}: {game.inventory[name].quest_description}')

            elif choice == "score":
                tw_print(f"{col_g('Your progress shows you are on track to achieve a score of')} {col_y(game.score)}.")
            
            elif choice == "undo":
                message = game_log.undo_last_action(game)
                tw_print(message)
                turn_taken = True
            
            elif choice == "log":
                game_log.display_events()

            elif choice == "stamina":
                tw_print(f"{col_g('You feel')} {col_y(game.stamina)}% {col_g('energized. Be mindful of your energy as you move!')}")
            
            elif choice == "help":
                help_msg()
            
            elif choice == "take":
                tw_print(col_b("Available items: "))
                for name, item in location.items_present.items():
                    tw_print(f"{col_b(name)}: {item.description}")
                item_name = input("\nEnter the name of the item you want to take: ").strip()
                item_name = validate_choice(item_name, location, valid_choices=list(location.items_present.keys()))
                # Add the item to the player's inventory
                item = location.items_present.pop(item_name)
                game.inventory[item_name] = item
                tw_print(f"You have taken a {item_name}.\n {item.quest_description}\n")
                # Update the player's score and stamina
                game.score += item.pickup_points
                game.stamina -= item.pickup_stamina_usage
                tw_print(f"Your progress shows you're on track to achieve a score of {game.score}.")
                tw_print(f"You feel {game.stamina}% energized. Be mindful of your energy as you move!")
                turn_taken = True

            elif choice == "deposit":
                tw_print(col_b("Items to deposit: "))
                for name, item in location.items_use.items():
                    tw_print(f"{col_b(name)}: {item.description}")
                item_name = input("\nEnter the name of the item you want to deposit: ").strip()
                item_name = validate_choice(item_name, location, valid_choices=[item_name for item_name in location.items_use if item_name in game.inventory])
                # Deposit the item at the location
                if item_name in location.items_use:
                    item = game.inventory[item_name]
                    del game.inventory[item_name]
                    tw_print(f"You have deposited the {item_name}.\n")
                    game.score += item.use_points
                    # Take account for special item (restores stamina to full)
                    game.stamina = min(100, game.stamina - item.use_stamina_usage)
                    tw_print(item.quest_complete_description)
                    # Take account for special item (increases inventory size)
                    if item_name == "lost backpack":
                        game.inventory_size = 7
                    tw_print(f"Your progress shows you're on track to achieve a score of {game.score}.")
                    tw_print(f"You feel {game.stamina}% energized. Be mindful of your energy as you move!")
                    turn_taken = True
            
            elif choice == "drop":
                tw_print(col_b("Items in your inventory: "))
                for name, item in game.inventory.items():
                    tw_print(f"{col_b(name)}: {item.description}")
                item_name = input("\nEnter the name of the item you want to drop: ").strip()
                item_name = validate_choice(item_name, location, valid_choices=list(game.inventory.keys()))
                # Drop the item at the location
                item = game.inventory.pop(item_name)
                game.score -= item.pickup_points # Remove points gained from taking item
                location.items_present[item_name] = item
                tw_print(f"You have dropped the {item_name}.")
                turn_taken = True
            
            else:
                game.ongoing = False

    # Check if the game ended due to stamina depletion
    if game.stamina <= 0:
        tw_print("You feel completely exhausted and can no longer continue. You'll need to try again.")
        
    # Check if the game ended due to player quitting
    elif game.ongoing:
        tw_print("You have decided to give up and not complete your assignment. Better luck next time!")
