#!/usr/bin/env python3
"""Module for AI player"""
import random

class AIPlayer:
    """Class representing an AI player for Tic-Tac-Toe."""
    def __init__(self):
        """Initializes the AI player with a default username
        and difficulty level.
        """
        self.username = "AI_Player"
        self.difficulty = "easy"  # Default difficulty level

    def set_difficulty(self, difficulty):
        """Sets the difficulty level for the AI player."""
        self.difficulty = difficulty

    def make_move(self, board):
        """Determines the move to make based on the
        selected difficulty level.
        """
        if self.difficulty == "easy":
            return self.random_move(board)
        elif self.difficulty == "medium":
            return self.mixed_move(board)
        elif self.difficulty == "hard":
            return self.minimax_move(board)

    def random_move(self, board):
        """Returns a random valid move."""
        empty_cells = [i for i, cell in enumerate(board) if cell == ' ']
        return random.choice(empty_cells) if empty_cells else None

    def mixed_move(self, board):
        """Mixes between random and Minimax-based moves (50-50 chance)."""
        if random.random() < 0.5:
            # 50% chance of random move
            return self.random_move(board)
        else:
            # 50% chance of Minimax move
            return self.minimax_move(board)

    def minimax_move(self, board):
        """Returns the best move using the Minimax algorithm with
        depth cutoff.
        """
        return get_best_move_with_cutoff(board)

def get_best_move_with_cutoff(board):
    """Finds the best move using the Minimax algorithm
    with depth cutoff for hard mode.
    """
    best_score = float('-inf')
    best_move = None
    depth_cutoff = 5

    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            score = minimax_with_cutoff(board, 0, False, depth_cutoff,
                                        float('-inf'), float('inf'))
            # Restore the board state
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i

    return best_move

def minimax_with_cutoff(board, depth, is_maximizing,
                        depth_cutoff, alpha, beta):
    """Minimax algorithm with a depth cutoff and
    alpha-beta pruning to limit recursion depth.
    """
    winner = check_winner(board)
    if winner == "X":
        return 10 - depth
    elif winner == "O":
        return depth - 10
    elif check_tie(board):
        return 0

    if depth >= depth_cutoff:
        # Use heuristic evaluation at cutoff depth
        return heuristic_evaluation(board)

    if is_maximizing:
        best_score = float('-inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax_with_cutoff(board, depth + 1, False,
                                            depth_cutoff, alpha, beta)
                # Restore the board state
                board[i] = ' '
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax_with_cutoff(board, depth + 1, True,
                                            depth_cutoff, alpha, beta)
                # Restore the board state
                board[i] = ' '
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return best_score

def heuristic_evaluation(board):
    """
    Evaluates the board and returns a score based on potential winning moves,
    blocking moves, and control of strategic positions.
    Positive scores favor the AI (X), and negative scores
    favor the opponent (O).
    """
    scores = {"X": 1, "O": -1}  # X is AI, O is opponent
    score = 0

    # Check all winning combinations
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]

    for combo in winning_combinations:
        line = [board[combo[0]], board[combo[1]], board[combo[2]]]

        # Check for potential winning moves
        if line.count("X") == 2 and line.count(" ") == 1:
            score += 10  # Prioritize winning
        elif line.count("O") == 2 and line.count(" ") == 1:
            score -= 8  # Block opponent's winning

        # Check for control of the board
        if line.count("X") == 1 and line.count(" ") == 2:
            score += 2  # Favor having one X in a potential line
        elif line.count("O") == 1 and line.count(" ") == 2:
            score -= 1  # Avoid letting O have any advantage

    # Center control
    if board[4] == "X":
        score += 5  # Increased weight for center control
    elif board[4] == "O":
        score -= 5

    # Corner control
    for corner in [0, 2, 6, 8]:
        if board[corner] == "X":
            score += 2  # Increased weight for corners
        elif board[corner] == "O":
            score -= 2

    return score

def check_winner(board):
    """Checks if there is a winner."""
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]

    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]
    return None

def check_tie(board):
    """Checks if the board is full and no winner is present."""
    return ' ' not in board
