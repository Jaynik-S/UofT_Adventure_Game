"""UofT Adventure Game - Event Logger
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from game_entities import Item


@dataclass
class Event:
    """
    A node representing one event in an adventure game.

    Instance Attributes:
    - id_num: Integer id of this event's location
    - description: Brief description of this event's location
    - next_command: String command which leads this event to the next event, None if this is the last game event
    - next: Event object representing the next event in the game, or None if this is the last game event
    - prev: Event object representing the previous event in the game, None if this is the first game event
    - inventory: The player's inventory at this event
    - stamina: The player's stamina at this event
    - items_present: The state of items present at each location at this event
    - score: The player's score at this event
    
    Representation Invariants:
    - len(description) > 0
    - stamina >= 0
    - len(inventory) >= 0
    - len(items_present) >= 0
    - all(len(items) >= 0 for items in items_present.values())
    """

    id_num: int
    description: str
    next_command: Optional[str] = None
    next: Optional[Event] = None
    prev: Optional[Event] = None
    inventory: dict[str, Item] = field(default_factory=dict) # ensure each instance has its own copy of the dictionary
    stamina: int = 100
    items_present: dict[int, dict[str, Item]] = field(default_factory=dict)
    score: int = 0

class EventList:
    """
    A linked list of game events.

    Instance Attributes:
        - first: The first event in the list, or None if the list is empty.
        - last: The last event in the list, or None if the list is empty.

    Representation Invariants:
        - (self.first is None and self.last is None) or (self.first is not None and self.last is not None)
    """
    first: Optional[Event]
    last: Optional[Event]

    def __init__(self) -> None:
        """Initialize a new empty event list."""

        self.first = None
        self.last = None

    def display_events(self) -> None:
        """Display all events in chronological order."""
        curr = self.first
        while curr:
            print(f"Location: {curr.id_num}, Command: {curr.next_command}")
            curr = curr.next

    def is_empty(self) -> bool:
        """Return whether this event list is empty."""

        return self.first is None

    def add_event(self, event: Event, command: str = None) -> None:
        """Add the given new event to the end of this event list.
        The given command is the command which was used to reach this new event, or None if this is the first
        event in the game.
        """
        if self.is_empty():
            self.first = event
            self.last = event
        else:
            self.last.next_command = command
            self.last.next = event
            event.prev = self.last
            self.last = event

    def get_id_log(self) -> list[int]:
        """Return a list of all location IDs visited for each event in this list, in sequence."""

        curr = self.first
        id_log = []
        while curr:
            id_log.append(curr.id_num)
            curr = curr.next
        return id_log

    def undo_last_action(self, game: AdventureGame) -> str:
        """Undo the last action and revert the game state."""
        from adventure import AdventureGame  # Import here to avoid circular dependency

        if self.is_empty():
            return "No actions to undo."

        last_event = self.last
        if last_event.prev is None:
            return "No actions to undo."

        # Revert to the previous event
        self.last = last_event.prev
        self.last.next = None

        # Restore the game state
        game.current_location_id = self.last.id_num
        game.inventory = self.last.inventory.copy()
        game.stamina = self.last.stamina
        game.score = self.last.score 

        # Restore the state of items at each location
        for loc_id, items in self.last.items_present.items():
            game._locations[loc_id].items_present = items.copy()

        return f"The following action has been undone: {last_event.next_command}"

    def add_event_to_log(self, game: AdventureGame, command: str = None) -> None:
        """Add the current game state to the event log."""
        from adventure import AdventureGame  # Import here to avoid circular dependency

        location = game.get_location()
        items_present = {loc_id: loc.items_present.copy() for loc_id, loc in game._locations.items()} # Save the state of items at each location
        event = Event(location.id_num, location.brief_description, command, inventory=game.inventory.copy(), stamina=game.stamina, items_present=items_present, score=game.score)
        self.add_event(event, command)


if __name__ == "__main__":
    pass
