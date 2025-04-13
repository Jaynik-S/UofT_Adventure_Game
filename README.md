# UofT Adventure Game

An adventure game set at the University of Toronto!

## ✨ Features

- **Text Adventure Engine**:
  - Object-oriented design using Python dataclasses
  - JSON-based game data configuration for easy content modification
  - Event logging system implemented as a linked list for game state tracking
  - Command parsing with validation for user input handling
  - Undo functionality through state snapshots and restoration

- **Game Mechanics**:
  - Resource management (stamina, inventory capacity)
  - Quest system with item-based puzzles
  - Score tracking with dynamic win conditions
  - Special item interactions that modify game rules

- **Dual Interface**:
  - Terminal version with colored text and optional typewriter effect
  - Flask-powered web application with responsive design
  - Session-based state management in web version
  - Interactive UI with dynamic content updates

## 🎮 How to Play

### Web Version

1. **Install**: Ensure you have Flask installed (`pip install flask`)
2. **Run**: Execute `python app.py` in your terminal
3. **Play**: Open your browser and navigate to `http://localhost:5000`

### Terminal Version

1. **Install**: Clone the repository to your local machine
2. **Run**: Execute `python adventure.py` in your terminal
3. **Optional**: Customize typewriter text effect when prompted

## 📖 Game Overview

**Story**: You wake up to find your laptop dead and its unique charger broken. With an important assignment due soon, you must race against time to collect items across campus, fix your charger, and help others along the way.

**Goal**: Repair your laptop charger, earn 100 points, and return to your dorm before running out of stamina.

## 📍 Locations

| Symbol | Description                         |
|--------|-------------------------------------|
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


## 🧩 Item Quests/Puzzles

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

## 🕹️ Game Commands

- **Go [direction]**: Move to another location
- **Take [item]**: Pick up an item
- **Deposit [item]**: Use an item at a specific location
- **Drop [item]**: Remove an item from inventory
- **Inventory**: View your collected items
- **Score**: Check your current score
- **Stamina**: Check your remaining energy
- **Help**: Display all available commands
- **Undo**: Reverse your last action
- **Log**: View history of actions
- **Quit**: End the game

## 🗒️ Details

The game is built using Python with:
- Object-oriented design with dataclasses
- JSON for game data configuration
- Event logging system for game state management
- Flask web framework for the browser-based version
- Responsive web interface with typewriter text effects



