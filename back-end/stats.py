#!/usr/bin/env python3
"""Module for statistics"""
from database import get_db
'''
def update_player_stats_after_game(game, result):
    """Updates statistics for players and is after each game"""
    db = get_db()
    game_type = game['game_type']
    players = game['players']

    if game_type == 'pvp':
        if result == 'tie':
            for player_id in players:
                db['players'].update_one(
                    {"id": player_id},
                    {"$inc": {"stats.draws": 1}},
                    upsert=True
                )
        else:
            winner_id = players[0] if result == 'X' else players[1]
            loser_id = players[1] if result == 'X' else players[0]

            db['players'].update_one(
                {"id": winner_id},
                {"$inc": {"stats.wins": 1}},
                upsert=True
            )
            db['players'].update_one(
                {"id": loser_id},
                {"$inc": {"stats.losses": 1}},
                upsert=True
            )

    elif game_type == 'ai':
        player_id = players[0]  # In AI games, there's only one human player
        if result == 'tie':
            db['players'].update_one(
                {"id": player_id},
                {"$inc": {"stats.draws": 1}},
                upsert=True
            )
            db['ai_stats'].update_one(
                {"difficulty": game['difficulty']},
                {"$inc": {"draws": 1}},
                upsert=True
            )
        elif result == 'O':  # Player wins
            db['players'].update_one(
                {"id": player_id},
                {"$inc": {"stats.wins": 1}},
                upsert=True
            )
            db['ai_stats'].update_one(
                {"difficulty": game['difficulty']},
                {"$inc": {"losses": 1}},
                upsert=True
            )
        else:  # AI wins
            db['players'].update_one(
                {"id": player_id},
                {"$inc": {"stats.losses": 1}},
                upsert=True
            )
            db['ai_stats'].update_one(
                {"difficulty": game['difficulty']},
                {"$inc": {"wins": 1}},
                upsert=True
            )
'''

def initialize_player_stats(player_id):
    """Initialises player statistics to 0"""
    db = get_db()
    db['players'].update_one(
        {"id": player_id},
        {"$set": {"stats": {"wins": 0, "losses": 0, "draws": 0}}},
        upsert=True
    )

def get_player_stats(player_id):
    """Statistics for human player"""
    db = get_db()
    player = db['players'].find_one({"id": player_id})
    return player.get('stats', {"wins": 0, "losses": 0, "draws": 0})

def get_ai_stats(difficulty):
    """Gets the statistics for the AI player"""
    db = get_db()
    ai_stats = db['ai_stats'].find_one({"difficulty": difficulty})
    return ai_stats or {"wins": 0, "losses": 0, "draws": 0}
