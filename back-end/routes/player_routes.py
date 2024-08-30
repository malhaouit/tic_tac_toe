#!/usr/bin/env python3
"""
Player routes for Tic-Tac-Toe API.

Handles player creation, retrieval, and stat updates through
various API endpoints.
"""
from flask import Blueprint, request, jsonify
from database import get_db
import uuid

# Initialize the player_routes blueprint
bp = Blueprint('player_routes', __name__)


def generate_uuid():
    """
    Generates a unique UUID string.
    """
    return str(uuid.uuid4())


@bp.route('/players', methods=['POST'], strict_slashes=False)
def create_player():
    """
    Creates a new player and inserts them into the database
    """
    data = request.json

    if not data.get("name"):
        return jsonify({"error": "Player name is required"}), 400
    if not isinstance(data.get("name"), str):
        return jsonify({"error": "Player name must be a string"}), 400
    if data.get("theme") and data["theme"] not in ["white", "dark"]:
        return jsonify({"error": "Invalid theme. Choose 'white' or 'dark'."}), 400

    players_collection = get_db()['players']

    # Check if player with the same name already exists
    existing_player = players_collection.find_one({"name": data.get("name")})
    if existing_player:
        existing_player["_id"] = str(existing_player["_id"])
        return jsonify(existing_player), 200

    # Create player document
    player = {
            "id": str(generate_uuid()),
            "name": data.get("name", None),
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "theme": data.get("theme", "white")
            }

    # Insert player into the database
    result = players_collection.insert_one(player)
    player["_id"] = str(result.inserted_id)

    return jsonify(player), 201


@bp.route('/players/<id>', methods=['GET'])
def get_player(id):
    """
    Retrieves a player's details by theire unique ID.
    """
    # Access the database using get_db()
    players_collection = get_db()['players']

    # Find the player by their ID
    player = players_collection.find_one({"id": id})

    if player:
        # Convert the _id field to string for JSON serialization
        if '_id' in player:
            player['_id'] = str(player['_id'])
        return jsonify(player), 200

    # If the player is not found, return a 404 error
    return jsonify({"error": "Player not found"}), 404


@bp.route('/players/<id>/stats', methods=['PUT'], strict_slashes=False)
def update_player_stats(id):
    """
    Updates the player's stats incrementing wins, losses, or draws.
    """
    data = request.json

    for key in data.keys():
        if key not in ["wins", "losses", "draws"]:
            return jsonify({"error": f"Invalid stat key: {key}. Expected 'wins', 'losses', or 'draws'."}), 400
        if not isinstance(data[key], int):
            return jsonify({"error": f"Invalid value for {key}. Integer expected."}), 400
        if data[key] != 1:
            return jsonify({"error": f"Invalid value for {key}. Only increments or decrements of 1 are allowed."}), 400

    # Prepare the update query to increment stats
    update_stats = {"$inc": data}

    # Access the database using get_db()
    players_collection = get_db()['players']

    # Perform the update operation in the database
    result = players_collection.update_one({"id": id}, update_stats)

    if result.matched_count > 0:
        return jsonify({"message": "Player stats updated"}), 200

    # If the player is not found, return a 404 error
    return jsonify({"error": "Player not found"}), 404
