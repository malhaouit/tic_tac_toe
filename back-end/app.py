#!/usr/bin/env python3
"""
The entry point for running the Flask application.
"""
from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room
from routes import player_routes, game_routes
from database import initialize_db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_pyfile('config.py')

socketio = SocketIO(app)

app.register_blueprint(player_routes.bp)
app.register_blueprint(game_routes.bp)

socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")

@app.before_request
def before_request():
    initialize_db()

@socketio.on('join_game')
def on_join_game(data):
    room = data['game_id']
    join_room(room)
    emit('player_joined', {'message': 'A player has joined the game.'}, room=room)

@socketio.on('make_move')
def on_make_move(data):
    game_id = data['game_id']
    index = data['index']
    player = data['player']

    # Validate and make the move
    game = get_db()['games'].find_one({"id": game_id})
    if not game:
        emit('error', {'error': 'Game not found.'})
        return

    board = game.get('board', [''] * 9)
    if board[index] != '':
        emit('error', {'error': 'Cell already occupied.'})
        return

    board[index] = player
    get_db()['games'].update_one({"id": game_id}, {"$set": {"board": board}})

    winner = check_winner(board)
    if winner:
        get_db()['games'].update_one({"id": game_id}, {"$set": {"completed": True, "decision": winner}})
        update_player_stats_after_game(game, winner)
        emit('game_update', {'board': board, 'winner': winner}, room=game_id)
    else:
        emit('game_update', {'board': board}, room=game_id)

if __name__ == '__main__':
    socketio.run(app, debug=True)
