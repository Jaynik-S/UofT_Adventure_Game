from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import json
from adventure import AdventureGame
from game_entities import Location, Item
from proj1_event_logger import EventList, Event

app = Flask(__name__)
app.secret_key = 'uoft_adventure_game_secret_key'  # For session management
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize the global game log
game_log = EventList()

@app.route('/')
def index():
    """Display the game introduction page"""
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    """Initialize a new game and redirect to the game page"""
    # Clear any existing session data
    session.clear()
    
    # Initialize the game
    game = AdventureGame('game_data.json', 1)
    
    # Save game state in session
    save_game_state(game)
    
    # Initialize the game log
    global game_log
    game_log = EventList()
    current_location = game.get_location()
    # Capture complete initial state with all items
    game_log.add_event(Event(
        current_location.id_num, 
        current_location.brief_description, 
        None,
        inventory=game.inventory.copy(),
        stamina=game.stamina,
        items_present={loc_id: loc.items_present.copy() for loc_id, loc in game._locations.items()},
        score=game.score
    ))
    
    
    # Set typewriter effect preference
    session['typewriter_effect'] = request.form.get('typewriter_effect', 'no') == 'yes'
    if session['typewriter_effect']:
        try:
            session['char_delay'] = float(request.form.get('char_delay', '0.0225'))
        except ValueError:
            session['char_delay'] = 0.0225
    else:
        session['char_delay'] = 0
    
    # Set first visit flag for the initial location
    session['visited'] = {str(1): False}
    
    return redirect(url_for('game'))

@app.route('/game')
def game():
    """Display the main game page"""
    if 'current_location_id' not in session:
        return redirect(url_for('index'))
    
    # Load game state from session
    game = load_game_state()
    
    # Get current location
    location = game.get_location()
    location_id = str(location.id_num)
    
    # Check if location has been visited before
    if location_id not in session['visited']:
        session['visited'][location_id] = False
    
    # Determine which description to show
    if session['visited'][location_id]:
        description = location.brief_description
    else:
        description = location.long_description
        session['visited'][location_id] = True
        session.modified = True
    
    # Get available moves
    available_moves = location.available_movements
    
    # Get items at the current location
    items_present = get_items_at_location(game)
    
    # Check for available actions
    can_take = location.items_present and len(game.inventory) < game.inventory_size
    can_deposit = any(item_name in game.inventory for item_name in location.items_use)
    can_drop = bool(game.inventory)
    
    # Check if the player can craft the laptop charger
    can_craft_charger = check_can_craft_charger(game)
    
    # Check win conditions
    win_condition = (game.score >= 100 and game.current_location_id == 1 
                     and "fixed laptop charger" in game.inventory and game.stamina > 0)
    
    # Check lose condition
    lose_condition = game.stamina <= 0
    
    # Check partial win conditions for hints
    has_enough_points = game.score >= 100
    has_charger = "fixed laptop charger" in game.inventory
    
    # Get items that can be used at current location
    usable_items = [item_name for item_name in location.items_use if item_name in game.inventory]
    
    return render_template(
        'game.html',
        location=location,
        description=description,
        available_moves=available_moves,
        items_present=items_present,
        inventory=game.inventory,
        inventory_size=game.inventory_size,
        score=game.score,
        stamina=game.stamina,
        can_take=can_take,
        can_deposit=can_deposit,
        can_drop=can_drop,
        usable_items=usable_items,
        win_condition=win_condition,
        lose_condition=lose_condition,
        has_enough_points=has_enough_points,
        has_charger=has_charger,
        can_craft_charger=can_craft_charger,
        typewriter_effect=session['typewriter_effect'],
        char_delay=session['char_delay']
    )

@app.route('/action', methods=['POST'])
def action():
    """Handle player actions"""
    if 'current_location_id' not in session:
        return redirect(url_for('index'))
    
    action = request.form.get('action')
    
    # Load game state from session
    game = load_game_state()
    
    # Process the action
    if action == 'go':
        direction = request.form.get('direction')
        handle_go_action(game, direction)
        # Save the event to the log with complete command information
        game_log.add_event_to_log(game, f"{action} {direction}")
    elif action == 'take':
        item_name = request.form.get('item')
        handle_take_action(game, item_name)
        # Save the event to the log with complete command information
        game_log.add_event_to_log(game, f"{action} {item_name}")
    elif action == 'deposit':
        item_name = request.form.get('item')
        handle_deposit_action(game, item_name)
        # Save the event to the log with complete command information
        game_log.add_event_to_log(game, f"{action} {item_name}")
    elif action == 'drop':
        item_name = request.form.get('item')
        handle_drop_action(game, item_name)
        # Save the event to the log with complete command information
        game_log.add_event_to_log(game, f"{action} {item_name}")
    elif action == 'craft':
        handle_craft_action(game)
        # Save the event to the log
        game_log.add_event_to_log(game, "craft fixed laptop charger")
    elif action == 'undo':
        handle_undo_action(game)
        # Don't add a new event for undo - this would interfere with state management
    
    # Save updated game state
    save_game_state(game)
    
    return redirect(url_for('game'))

@app.route('/log')
def view_log():
    """Display the game event log"""
    if 'current_location_id' not in session:
        return redirect(url_for('index'))
    
    # Get events from game log
    events = []
    current_event = game_log.first
    
    while current_event:
        events.append({
            'description': current_event.description,
            'command': current_event.next_command
        })
        current_event = current_event.next
    
    return render_template('log.html', events=events)

@app.route('/help')
def help_page():
    """Display the help page"""
    return render_template('help.html')

def save_game_state(game):
    """Save the game state to the session"""
    session['current_location_id'] = game.current_location_id
    session['inventory'] = {name: vars(item) for name, item in game.inventory.items()}
    session['ongoing'] = game.ongoing
    session['stamina'] = game.stamina
    session['score'] = game.score
    session['inventory_size'] = game.inventory_size
    
    # Save locations state (including items present)
    session['locations'] = {}
    for loc_id, loc in game._locations.items():
        session['locations'][str(loc_id)] = {
            'items_present': {name: vars(item) for name, item in loc.items_present.items()},
            'visited': loc.visited
        }

def load_game_state():
    """Load the game state from the session"""
    game = AdventureGame('game_data.json', session['current_location_id'])
    game.current_location_id = session['current_location_id']
    game.inventory = {name: Item(**item_data) for name, item_data in session['inventory'].items()}
    game.ongoing = session['ongoing']
    game.stamina = session['stamina']
    game.score = session['score']
    game.inventory_size = session['inventory_size']
    
    # Restore locations state
    for loc_id_str, loc_data in session['locations'].items():
        loc_id = int(loc_id_str)
        if loc_id in game._locations:
            game._locations[loc_id].items_present = {
                name: Item(**item_data) for name, item_data in loc_data['items_present'].items()
            }
            game._locations[loc_id].visited = loc_data['visited']
    
    return game

def get_items_at_location(game):
    """Get items available at the current location"""
    location = game.get_location()
    return location.items_present

def check_can_craft_charger(game):
    """Check if the player can craft the fixed laptop charger"""
    required_items = {"soldering iron", "broken laptop charger", "electrical tape", "screwdriver kit"}
    return (game.current_location_id == 6 and 
            required_items.issubset({item for item in game.inventory}))

def handle_go_action(game, direction):
    """Handle the go action"""
    location = game.get_location()
    if direction in location.available_movements:
        game.stamina -= 3  # reduce stamina for traveling
        game.current_location_id = location.available_movements[direction]

def handle_take_action(game, item_name):
    """Handle the take action"""
    location = game.get_location()
    if item_name in location.items_present and len(game.inventory) < game.inventory_size:
        item = location.items_present.pop(item_name)
        game.inventory[item_name] = item
        game.score += item.pickup_points
        game.stamina -= item.pickup_stamina_usage

def handle_deposit_action(game, item_name):
    """Handle the deposit action"""
    location = game.get_location()
    if item_name in location.items_use and item_name in game.inventory:
        item = game.inventory.pop(item_name)
        game.score += item.use_points
        game.stamina = min(100, game.stamina - item.use_stamina_usage)
        
        # Handle special items
        if item_name == "lost backpack":
            game.inventory_size = 7

def handle_drop_action(game, item_name):
    """Handle the drop action"""
    location = game.get_location()
    if item_name in game.inventory:
        item = game.inventory.pop(item_name)
        location.items_present[item_name] = item
        game.score -= item.pickup_points  # Remove points gained from taking item

def handle_craft_action(game):
    """Handle the crafting of the fixed laptop charger"""
    required_items = {"soldering iron", "broken laptop charger", "electrical tape", "screwdriver kit"}
    if game.current_location_id == 6 and required_items.issubset({item for item in game.inventory}):
        # Remove the required items
        for item in required_items:
            game.inventory.pop(item)
        
        # Add the fixed laptop charger
        fixed_laptop_charger = Item(
            "fixed laptop charger", 
            "", 
            "Your special laptop charger that is now fully functional",
            "",
            0, 0, 0, 0
        )
        game.inventory["fixed laptop charger"] = fixed_laptop_charger

def handle_undo_action(game):
    """Handle the undo action"""
    # Just call undo_last_action without adding another event
    # This is consistent with the terminal version implementation
    message = game_log.undo_last_action(game)
    return message

if __name__ == '__main__':
    app.run(debug=True)
