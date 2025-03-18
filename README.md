# UofT Adventure Game

## How to Run the Game  

1. **Clone the repository**:  
   ```sh
   git clone <repository-url>
   cd <repository-folder>
   ```  

2. **Run the game**:  
   Open a terminal (Command Prompt, PowerShell, or an external terminal) and enter:  
   ```sh
   python adventure.py
   ```  

3. **Optimize your experience**:  
   - Maximize the console window and adjust the font size for better readability.  
   - The game offers an optional typewriter effect for gradual text display. If enabled, you can customize the speed to suit your reading pace.

## Brief Game Storyline

After oversleeping before a critical assignment deadline, you discover your laptop is dead and its unique charger is destroyed. To save your semester, you must race across campus to find tools and find a location to repair your charger. Along the way, help others by returning lost items or solving problems to earn 100 points this will reflect your "predicted grade" on your assignment and determine if you’ll save your semester.

Manage your dwindling stamina and a small backpack, forcing tough choices about what to carry. If you run out of energy before repairing your charger, your assignment and semester are DOOMED. Success hinges on balancing exploration, kindness, and strategy: fix the charger, hit 100 points, and rush back to your dorm to submit your work. Good luck!

## Game Map

| -1  | **6** | **7**  | **10** | **11** |
|-----|-------|--------|--------|--------|
| **9**  | **4** | **2**  | -1    | **8**  |
| -1  | -1    | **1**  | **3**  | **5**  |

## Legend

| Symbol | Description                         |
|--------|-------------------------------------|
| -1     | Empty Space                         |
| **1**  | Woodsworth College Residence        |
| **2**  | Mechanical Engineering Machine Shop |
| **3**  | Convocation Hall                    |
| **4**  | King’s College Circle               |
| **5**  | Robarts Library                     |
| **6**  | Sandford Fleming Laboratory         |
| **7**  | Royal Ontario Museum (ROM)          |
| **8**  | Hart House                          |
| **9**  | Athletic Centre (AC)                |
| **10** | Sidney Smith Cafe                   |
| **11** | UofT Bookstore                      |

**Starting location** is: **Woodsworth College Residence (1)**



## Item Quests/Puzzles

### Main Quest (obtain fixed laptop charger item) [no point reward (0)]

| Item                  | Start Location          | End Location            |
|-----------------------|-------------------------|-------------------------|
| Broken Laptop Charger | WW Residence [1]        | Stanford Fleming Lab [5]|
| Soldering Iron        | Mech. Eng. Shop [2]     | Stanford Fleming Lab [5]|
| Electrical Tape       | Athletic Centre [9]     | Stanford Fleming Lab [5]|
| Screwdriver Kit       | UofT Bookstore [11]     | Stanford Fleming Lab [5]|

### Point Quests [large points reward (40)]

| Item           | Start Location | End Location       |
|----------------|----------------|--------------------|
| Lucky Mug      | Con. Hall [3]  | Athletic Centre [9]|
| Historical Book| Robarts [5]    | ROM [7]            |
| USB drive      | ROM [7]        | Con. Hall [3]      |

### Special Quests (in-game enhancements) [minor point reward (10)]

| Item                  | Start Location | End Location       |
|-----------------------|----------------|--------------------|
| Free Coffee Coupon    | Hart House [8] | Sid. Smith Cafe [10]|
| Lost Backpack         | King CC [5]    | UofT Bookstore [11]|

## Game Commands/Functions

- **Go**: after selecting this command you will be prompted to select which [direction] to go (based on map).
- **Look**: a message displaying the long description of the current location
- **Inventory**: a table displaying all item names and the description of the quest associated with each the item (max of 5 items without deposit of special item)
- **Score**: a message displaying the current score 
  - Player starts with 0 score and a minimum of 100 score needed to complete the game
  - Player's earn score by picking up and depositing items at their designated locations 
  - NOTE: When a player drops an item the score gained from picking up the item is removed
- **Undo**: restores the game state to the previous move (location, inventory, stamina, points) and displays most recent command that was undone    
- **Log**: a message displaying list of all the events (locations visited, commands chosen) in order 
- **Stamina**: a message displaying the current stamina (starts at 100 score needed to complete the game)
  - Player starts with 100 stamina and if a players ends up with 0 stamina the game ends
  - Player's lose stamina when travelling to a location, picking up and using items
    - Using the "go" command (travelling to a location): uses 3 stamina
    - Using the "take" command (pick up an item): uses 4 stamina
    - Using the "deposit" command (using up an item): uses 2 stamina
  - The only way to restore stamina is by depositing the free coffee coupon at the correct location
- **Help**: a menu displaying all commands and their function 
- **Quit**: the game ends and the user is displayed a quit message

### If applicable:

- **Deposit**: after selecting this command you will be prompted to select which [item] to use (based on items to use at current location and items in inventory)
  - The item is removed from the player's inventory
  - The player's score will increase based on the pickup points of said item
  - The player's stamina will decrease based on stamina usage of using said item
  - Special Item (Free Coffee Coupon): The player's stamina is instantly restored to 100
  - Special Item (Lost Backpack): The player's inventory size is increased from 5 to 7
- **Take**: after selecting this command you will be prompted to select which [item] to take (based on items available at current location)
  - The item is removed from available items at current location
  - The item is then added to the player's inventory
  - The player's score will increase based on the pickup points of said item
  - The player's stamina will decrease based on stamina usage of picking up said item
- **Drop**: after selecting this command you will be prompted to select which [item] to drop (based on items in inventory)
  - The item is removed from the players inventory
  - The item is then added to the available items at current location
  - The score gained from picking up the item is removed
  - The stamina lost from picking up the item is not restored

## Technical Implementation

1. **Core Game Architecture**
   - **Main Game Loop**: Implemented in `adventure.py` with nested while loops - outer loop manages game state, inner loop processes player input. Uses `validate_choice()` from `game_helpers.py` for input validation.
   - **Main Command Loop**: The main loop processes primary game commands (e.g., movement, item interactions) and updates the game state accordingly. It ensures that the game state is consistently updated based on player actions, excluding informational commands like inventory, score, and log, which are handled separately.
   - **Event Logging System**: Implemented in `proj1_event_logger.py`, this system records all main game actions (e.g., movement, item interactions) to facilitate the undo functionality. Informational commands are not logged to maintain focus on state-changing events.
   - **State Management**: All game state (location, inventory, score, stamina) stored in `AdventureGame` instance attributes. Modified through 15+ conditional branches in the main loop.

2. **Python OOP Techniques**  
   - **Classes and Inheritance**: The game uses classes to represent game entities such as `AdventureGame`, `Location`, and `Item`. These classes encapsulate related data and behavior, promoting modularity and code reuse.  
   - **Encapsulation**: Instance attributes are used to store the state of the game, and methods are provided to manipulate this state. This ensures that the internal state of the game is only modified through well-defined interfaces.  
   - **Data Classes**: The `dataclass` decorator is used for `Item` and `Location` classes to automatically generate special methods like `__init__()`, `__repr__()`, and `__eq__()`, reducing boilerplate code.  
   - **Type Hints**: Type hints are used throughout the code to specify the expected types of variables, function parameters, and return values. This improves code readability and helps with static type checking.  
   - **Static Methods**: The `AdventureGame._load_game_data` method is defined as a static method because it does not depend on any instance-specific data. This makes it clear that the method can be called without an instance of the class.  
   - **Representation Invariants**: Representation invariants are used to ensure that the game state remains consistent. These invariants are documented in the class docstrings and enforced through careful coding practices.  

3. **JSON Integration**  
   - **Data Loading**: `game_data.json` is parsed with `json.load()`, containing 11 locations and 9 items with 8 attributes each.  
   - **Extensibility**: New locations/items can be added without code changes by modifying the JSON file.  
   - **Special Cases**: A fixed laptop charger is created dynamically (lines 278-284 in `adventure.py`) rather than through the JSON file.  


