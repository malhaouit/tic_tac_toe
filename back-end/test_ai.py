#!/usr/bin/env python3

from ai_player import AIPlayer

def print_board(board):
    """Prints the board in a readable format."""
    for i in range(0, 9, 3):
        print(f"{board[i]} | {board[i+1]} | {board[i+2]}")
        if i < 6:
            print("---------")

def get_user_move(board):
    """Prompts the user for their move and returns it."""
    while True:
        try:
            move = int(input("Enter your move (0-8): "))
            if 0 <= move <= 8:
                if board[move] == ' ':
                    return move
                else:
                    print("Cell already occupied. Try again.")
            else:
                print("Invalid move. Please enter a number between 0 and 8.")
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 8.")

def main():
    """Main function to test the AI."""
    print("Welcome to Tic-Tac-Toe!")
    difficulty = input("Choose difficulty (easy, medium, hard): ").strip().lower()
    
    ai_player = AIPlayer()
    ai_player.set_difficulty(difficulty)
    board = [' '] * 9
    player_turn = True  # Player starts first
    
    while True:
        print_board(board)
        
        if player_turn:
            move = get_user_move(board)
            board[move] = 'O'
        else:
            print("AI is making a move...")
            move = ai_player.make_move(board)
            if move is not None:
                board[move] = 'X'
            else:
                print("AI couldn't make a move. Game over.")
                break
        
        # Check for game end conditions
        winner = check_winner(board)
        if winner:
            print_board(board)
            if winner == 'X':
                print("AI wins!")
            else:
                print("You win!")
            break
        
        if check_tie(board):
            print_board(board)
            print("It's a tie!")
            break
        
        player_turn = not player_turn

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
    return ' ' not in board and check_winner(board) is None

if __name__ == "__main__":
    main()