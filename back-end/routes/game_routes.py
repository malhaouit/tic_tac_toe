#!/usr/bin/env python3
"""
Game routes for the Tic-Tac-Toe API.

Handles the creation, retrieval, and updating of game-related data
through various API endpoints.
"""
from flask import Blueprint, request, jsonify
from database import get_db
import uuid

# Initialize the game_routes blueprint
bp = Blueprint('game_routes', __name__)

def generate_uuid():
    """
    Generates a unique UUID string.
    """
    return str(uuid.uuid4())


@bp.route('/games', methods=['POST'], strict_slashes=False)
def create_game():
    """
    Creates a new game and inserts it into the database.
    """
    data = request.json
    first_player_id = data.get("first_player_id")
    second_player_id = data.get("second_player_id")

    # Logging the incoming data
    print("Received game creation request with data:", data)

    # Validate the player IDs
    if not first_player_id or not second_player_id:
        print("Error: Missing player IDs")
        return jsonify({"error": "Player IDs are required"}), 400

    # Create game document with default values
    game = {
        "id": generate_uuid(),
        "first_player_id": first_player_id,
        "second_player_id": second_player_id,
        "decision": 0,  # Default to draw
        "difficulty": 1,  # Default to easy
        "board": [""] * 9,  # Empty board
        "completed": False
    }

    # Insert the new game into the 'games' collection
    games_collection = get_db()['games']
    result = games_collection.insert_one(game)
    game["_id"] = str(result.inserted_id)

    # Return the newly created game data as JSON
    print("Game created successfully with ID:", game["id"])
    return jsonify(game), 201


@bp.route('/games/<id>/move', methods=['PUT'], strict_slashes=False)
def make_move(id):
    """
    Handles making a move in the Tic-Tac-Toe game.
    Updates the game state and checks for a winner.
    """
    data = request.json
    index = data.get('index')
    player = data.get('player')

    if index is None or player not in ['X', 'O']:
        return jsonify({"error": "Invalid move data."}), 400

    game = get_db()['games'].find_one({"id": id})

    if not game:
        return jsonify({"error": "Game not found."}), 404

    # Update the board
    board = game.get('board', [''] * 9)
    if board[index] != '':
        return jsonify({"error": "Cell already occupied."}), 400

    board[index] = player
    get_db()['games'].update_one({"id": id}, {"$set": {"board": board}})

    # Check for winner
    winner = check_winner(board)
    if winner:
        # Update game completion status
        get_db()['games'].update_one({"id": id}, {"$set": {"completed": True, "decision": winner}})

        # Update player stats based on the winner
        update_player_stats_after_game(game, winner)

        return jsonify({"winner": winner, "board": board}), 200

    return jsonify({"board": board}), 200

def update_player_stats_after_game(game, winner):
    """
    Updates the stats of the players involved in a game based on the outcome.
    """
    first_player_id = game.get("first_player_id")
    second_player_id = game.get("second_player_id")

    if winner == 'X':
        # First player wins, second player loses
        get_db()['players'].update_one({"id": first_player_id}, {"$inc": {"wins": 1}})
        get_db()['players'].update_one({"id": second_player_id}, {"$inc": {"losses": 1}})
    elif winner == 'O':
        # Second player wins, first player loses
        get_db()['players'].update_one({"id": second_player_id}, {"$inc": {"wins": 1}})
        get_db()['players'].update_one({"id": first_player_id}, {"$inc": {"losses": 1}})
    else:
        # It's a draw
        get_db()['players'].update_one({"id": first_player_id}, {"$inc": {"draws": 1}})
        get_db()['players'].update_one({"id": second_player_id}, {"$inc": {"draws": 1}})

def check_winner(board):
    """
    Checks if there is a winner on the board.
    """
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]

    for combination in winning_combinations:
        if board[combination[0]] and board[combination[0]] == board[combination[1]] == board[combination[2]]:
            return board[combination[0]]
    return None
