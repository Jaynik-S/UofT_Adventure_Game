"""UofT Adventure Game - Game Entities
"""
from dataclasses import dataclass, field

@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: name of this item
        - description: description of what this item is
        - quest_description: description of the quest this item is associated with
        - quest_complete_description: description of the quest after completion
        - pickup_points: the points the player gets for picking up this item
        - use_points: the points the player gets for using this item
        - pickup_stamina_usage: the stamina used by the player to pick up this item
        - use_stamina_usage: the stamina used by the player to use this item

    Representation Invariants:
        - len(name) > 0
        - len(description) > 0 or len(quest_description) > 0 or len(quest_complete_description) > 0
        - pickup_stamina_usage >= 0 and use_stamina_usage >= 0
        - pickup_points >= 0 and use_points >= 0
    """

    name: str
    description: str
    quest_description: str
    quest_complete_description: str
    pickup_points: int
    use_points: int
    pickup_stamina_usage: int
    use_stamina_usage: int

@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: integer id for this location
        - name: name of this location
        - brief_description: brief description of this location
        - long_description: full description of this location including commands available, items present
        - available_movements: a mapping of available commands at this location to the location executing that command would lead to
        - take_actions: a list of available items to pickup at this location
        - use_actions: a list of items to use at this location 
        - visited: a boolean indicating if the player has visited this location
        - items_present: a mapping of items present at this location
        - items_use: a mapping of items to use at this location

    Representation Invariants:
        - id_num >= 0
        - len(brief_description) > 0
        - len(long_description) > 0
        - len(available_movements) > 0
        - all(len(command) > 0 for command in available_movements)
    """

    id_num: int
    name: str
    brief_description: str
    long_description: str
    available_movements: dict[str, int]
    take_actions: list[str]
    use_actions: list[str]
    visited: bool = False
    items_present: dict[str, Item] = field(default_factory=dict) # ensure each instance has its own copy of the dictionary
    items_use: dict[str, Item] = field(default_factory=dict)


if __name__ == "__main__":
    pass
