"""UofT Adventure Game - Simulator
"""
from __future__ import annotations
from proj1_event_logger import Event, EventList
from adventure import AdventureGame
from game_entities import Location, Item


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    _game: AdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str]) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id)

        # Add first event
        curr_location = self._game.get_location()
        self._events.add_event(Event(curr_location.id_num, curr_location.brief_description, None))

        # Generate rest of events based on commands
        self.generate_events(commands, curr_location)

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """Generate all events in this simulation.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        i = 0
        while i < len(commands):
            command = commands[i]
            if command == "go":
                direction = commands[i + 1]
                next_location_id = current_location.available_movements[direction]
                next_location = self._game.get_location(next_location_id)
                self._game.stamina -= 3
                self._events.add_event(Event(next_location.id_num, next_location.brief_description), "go " + direction)
                current_location = next_location
                i += 1

            elif command == "take":
                item_name = commands[i + 1]
                item = current_location.items_present.pop(item_name)
                self._game.inventory[item_name] = item

                self._game.score += item.pickup_points
                self._game.stamina -= item.pickup_stamina_usage

                self._events.add_event(Event(current_location.id_num, f"Took {item_name}"), command + " " + item_name)
                i += 1  

            elif command == "deposit":
                item_name = commands[i + 1]
                item = self._game.inventory.pop(item_name)
                # Special item handling
                if item_name == "lost backpack":
                    self._game.inventory_size = 7

                self._game.score += item.use_points
                self._game.stamina = min(100, self._game.stamina - item.use_stamina_usage)

                self._events.add_event(Event(current_location.id_num, f"Used {item_name}"), command + " " + item_name)
                i += 1

            elif command == "drop":
                item_name = commands[i + 1]
                item = self._game.inventory.pop(item_name)
                current_location.items_present[item_name] = item

                self._game.score -= item.pickup_points

                self._events.add_event(Event(current_location.id_num, f"Dropped {item_name}"), command + " " + item_name)
                i += 1 

            elif command == "undo":
                self._events.undo_last_action(self._game)
                if self._events.last:
                    current_location = self._game.get_location(self._events.last.id_num)
                self._events.add_event(Event(current_location.id_num, "Undid last action"), command)

            elif command == "stamina":
                self._events.add_event(Event(current_location.id_num, f"Current stamina: {self._game.stamina}"), command)

            elif command == "score":
                self._events.add_event(Event(current_location.id_num, f"Current score: {self._game.score}"), command)

            elif command == "inventory":
                inventory_list = ", ".join(self._game.inventory.keys())
                self._events.add_event(Event(current_location.id_num, f"Current inventory: {inventory_list}"), command)

            i += 1

            # Check if the player can create the fixed laptop charger
            required_items = {"soldering iron", "broken laptop charger", "electrical tape", "screwdriver kit"}
            if current_location.id_num == 6 and required_items.issubset(self._game.inventory.keys()):
                for item in required_items:
                    self._game.inventory.pop(item)
                fixed_laptop_charger = Item("fixed laptop charger","","Your special laptop charger that is now fully functional","", 0, 0, 0, 0)

                self._game.inventory["fixed laptop charger"] = fixed_laptop_charger
                self._events.add_event(Event(current_location.id_num, "Fixed your laptop charger!"), "Took fixed laptop charger")

            # Check if the player has won break loop if so
            if self._game.score >= 100 and current_location.id_num == 1 and "fixed laptop charger" in self._game.inventory and self._game.stamina > 0:
                break

            # Check if the player has lost due to stamina depletion break loop if so
            if self._game.stamina <= 0:
                break
        
        # Add an event indicating the game player has either won or lost
        if self._game.score >= 100 and current_location.id_num == 1 and "fixed laptop charger" in self._game.inventory and self._game.stamina > 0:
            self._events.add_event(Event(current_location.id_num, "Congratulations! You have won the game!"), "completed all tasks")

        if self._game.stamina <= 0:
            self._events.add_event(Event(current_location.id_num, "Game Over! You have run out of stamina."), "lost stamina")

        

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> sim = AdventureGameSimulation('game_data.json', 1, ["go", "east"])
        >>> sim.get_id_log()
        [1, 3]

        >>> sim = AdventureGameSimulation('game_data.json', 1, ["go", "east", "go", "east"])
        >>> sim.get_id_log()
        [1, 3, 5]
        """
        return self._events.get_id_log()

    def run(self) -> None:
        """Run the game simulation and log location descriptions."""
        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)
                print('=========')
            current_event = current_event.next


if __name__ == "__main__":

    # Walkthrough of commands needed to win the game
    win_walkthrough = [
    "go", "east", "take", "lucky mug",
    "go", "east", "take", "historical book",
    "go", "north", "take", "free coffee coupon",
    "go", "north", "go", "west", "go", "west",
    "deposit", "historical book", "take", "USB drive",
    "go", "south", "go", "west", "take", "lost backpack",
    "go", "west", "deposit", "lucky mug",
    "go", "east", "go", "east", "take", "soldering iron",
    "go", "south", "take", "broken laptop charger",
    "go", "north", "go", "north", "go", "east",
    "deposit", "free coffee coupon", "go", "east",
    "deposit", "lost backpack", "take", "screwdriver kit",
    "go", "south", "go", "south", "go", "west",
    "deposit", "USB drive", "go", "west",
    "go", "north", "go", "west", "go", "west",
    "take", "electrical tape", "go", "east",
    "go", "north", "go", "south", "go", "east",
    "go", "south"
]
    expected_log = [1, 3, 3, 5, 5, 8, 8, 11, 10, 7, 7, 7, 2, 4, 4, 9, 9, 4, 2, 2, 1, 1, 2, 7, 10, 10, 11, 11, 11, 8, 5, 3, 3, 1, 2, 4, 9, 9, 4, 6, 6, 4, 2, 1, 1]
    assert expected_log == AdventureGameSimulation('project1/game_data.json', 1, win_walkthrough).get_id_log()

    # Walkthrough of commands needed to reach a 'game over' state (due to lost of stamina). 
    # Same as win_walkthrough but did not use special item to restore stamina
    lose_demo = [
    "go", "east", "take", "lucky mug",
    "go", "east", "take", "historical book",
    "go", "north", "take", "free coffee coupon",
    "go", "north", "go", "west", "go", "west",
    "deposit", "historical book", "take", "USB drive",
    "go", "south", "go", "west", "take", "lost backpack",
    "go", "west", "deposit", "lucky mug",
    "go", "east", "go", "east", "take", "soldering iron",
    "go", "south", "take", "broken laptop charger",
    "go", "north", "go", "north", "go", "east",
    "go", "east", # Did not take free coffee coupon (stamina restore item)
    "deposit", "lost backpack", "take", "screwdriver kit",
    "go", "south", "go", "south", "go", "west",
    "deposit", "USB drive", "go", "west",
]
    print(AdventureGameSimulation('project1/game_data.json', 1, lose_demo).get_id_log())
    expected_log = [1, 3, 3, 5, 5, 8, 8, 11, 10, 7, 7, 7, 2, 4, 4, 9, 9, 4, 2, 2, 1, 1, 2, 7, 10, 11, 11, 11, 8, 5, 3, 3, 1, 1]
    assert expected_log == AdventureGameSimulation('project1/game_data.json', 1, lose_demo).get_id_log()

    # Walkthrough involving visiting locations, picking up items, and checking the inventory (special: increasing inventory size)
    inventory_demo = [
        "take", "broken laptop charger",
        "go", "north", "take", "soldering iron",
        "go", "west", "take", "lost backpack",
        "go", "west", "take", "electrical tape",
        "go", "east", "go", "east", "go", "north",
        "take", "USB drive", "go", "east", "inventory", # 5 items in inventory
        "go", "east", "deposit", "lost backpack",
        "take", "screwdriver kit", "go", "south",
        "take", "free coffee coupon", "go", "south",
        "take", "historical book", "inventory" # 7 items in inventory
    ]
    expected_log = [1, 1, 2, 2, 4, 4, 9, 9, 4, 2, 7, 7, 10, 10, 11, 11, 11, 8, 8, 5, 5, 5]

    
    assert expected_log == AdventureGameSimulation('project1/game_data.json', 1, inventory_demo).get_id_log()

    # Walkthrough involving checking the score (have fixed laptop charger but not enough score to win)
    scores_demo = [
    "take", "broken laptop charger",
    "go", "east", "go", "east",
    "go", "north", "go", "north",
    "take", "screwdriver kit", "go", "west",
    "go", "west", "go", "south",
    "take", "soldering iron", "go", "west",
    "go", "west", "take", "electrical tape",
    "go", "east", "go", "north",
    "go", "south", "go", "east",
    "go", "south", "inventory", "score"
]
    expected_log = [1, 1, 3, 5, 8, 11, 11, 10, 7, 2, 2, 4, 9, 9, 4, 6, 6, 4, 2, 1, 1, 1]   
    assert expected_log == AdventureGameSimulation('project1/game_data.json', 1, scores_demo).get_id_log()
    

    # Run a simulation to see the output
    sim = AdventureGameSimulation('project1/game_data.json', 1, win_walkthrough)
    sim.run()