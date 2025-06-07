#!/usr/bin/env python3

import os
import random
import time
from typing import List, Tuple, Optional, Dict, Union

class TicTacToe:
    def __init__(self):
        # Initialize empty 3x3 board
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # X always starts
        self.game_over = False
        self.winner = None
        self.moves_count = 0
        self.ai_enabled = False
        self.ai_difficulty = "medium"  # easy, medium, hard
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.moves_count = 0
    
    def print_board(self):
        """Print the current state of the board."""
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
        
        print("\n  Tic-Tac-Toe\n")
        print("    1   2   3 ")
        print("  ┌───┬───┬───┐")
        
        for i in range(3):
            print(f"{i+1} │", end=" ")
            for j in range(3):
                print(f"{self.board[i][j]} │", end=" ")
            print("\n  ├───┼───┼───┤" if i < 2 else "\n  └───┴───┴───┘")
        
        if self.game_over:
            if self.winner:
                print(f"\nGame Over! {self.winner} wins!")
            else:
                print("\nGame Over! It's a draw!")
        else:
            print(f"\nPlayer {self.current_player}'s turn")
            
            if self.ai_enabled and self.current_player == 'O':
                print("AI is thinking...")
    
    def make_move(self, row: int, col: int) -> bool:
        """
        Attempt to make a move at the specified position.
        
        Args:
            row: Row index (0-2)
            col: Column index (0-2)
            
        Returns:
            bool: True if the move was successful, False otherwise
        """
        # Check if the game is already over
        if self.game_over:
            return False
        
        # Check if the cell is empty
        if self.board[row][col] != ' ':
            return False
        
        # Make the move
        self.board[row][col] = self.current_player
        self.moves_count += 1
        
        # Check for win or draw
        if self.check_win():
            self.game_over = True
            self.winner = self.current_player
        elif self.moves_count == 9:  # All cells filled
            self.game_over = True
        else:
            # Switch player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        
        return True
    
    def check_win(self) -> bool:
        """
        Check if the current player has won.
        
        Returns:
            bool: True if the current player has won, False otherwise
        """
        player = self.current_player
        
        # Check rows
        for row in self.board:
            if row.count(player) == 3:
                return True
        
        # Check columns
        for col in range(3):
            if [self.board[row][col] for row in range(3)].count(player) == 3:
                return True
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return True
        
        return False
    
    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """
        Get a list of empty cells on the board.
        
        Returns:
            List[Tuple[int, int]]: List of (row, col) tuples for empty cells
        """
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    empty_cells.append((i, j))
        return empty_cells
    
    def is_board_full(self) -> bool:
        """
        Check if the board is full.
        
        Returns:
            bool: True if the board is full, False otherwise
        """
        return self.moves_count == 9
    
    def minimax(self, depth: int, is_maximizing: bool, alpha: float = float('-inf'), beta: float = float('inf')) -> Dict[str, Union[int, Tuple[int, int]]]:
        """
        Minimax algorithm with alpha-beta pruning for AI decision making.
        
        Args:
            depth: Current depth in the game tree
            is_maximizing: True if maximizing player, False if minimizing
            alpha: Alpha value for alpha-beta pruning
            beta: Beta value for alpha-beta pruning
            
        Returns:
            Dict with 'score' and optionally 'move' keys
        """
        # Terminal states
        if self.winner == 'O':  # AI wins
            return {'score': 10 - depth}
        elif self.winner == 'X':  # Human wins
            return {'score': depth - 10}
        elif self.is_board_full():  # Draw
            return {'score': 0}
        
        # Limit search depth based on difficulty
        max_depth = {'easy': 1, 'medium': 3, 'hard': 9}
        if depth >= max_depth.get(self.ai_difficulty, 3):
            return {'score': 0}  # Neutral score at max depth
        
        best_move = None
        
        if is_maximizing:  # AI's turn (O)
            best_score = float('-inf')
            player_before = self.current_player
            self.current_player = 'O'
            
            for cell in self.get_empty_cells():
                row, col = cell
                
                # Make the move
                self.board[row][col] = 'O'
                self.moves_count += 1
                
                # Check for win
                if self.check_win():
                    self.winner = 'O'
                
                # Recursive call
                result = self.minimax(depth + 1, False, alpha, beta)
                score = result['score']
                
                # Undo the move
                self.board[row][col] = ' '
                self.moves_count -= 1
                self.winner = None
                
                # Update best score
                if score > best_score:
                    best_score = score
                    best_move = cell
                
                # Alpha-beta pruning
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            
            self.current_player = player_before
            return {'score': best_score, 'move': best_move}
        
        else:  # Human's turn (X)
            best_score = float('inf')
            player_before = self.current_player
            self.current_player = 'X'
            
            for cell in self.get_empty_cells():
                row, col = cell
                
                # Make the move
                self.board[row][col] = 'X'
                self.moves_count += 1
                
                # Check for win
                if self.check_win():
                    self.winner = 'X'
                
                # Recursive call
                result = self.minimax(depth + 1, True, alpha, beta)
                score = result['score']
                
                # Undo the move
                self.board[row][col] = ' '
                self.moves_count -= 1
                self.winner = None
                
                # Update best score
                if score < best_score:
                    best_score = score
                    best_move = cell
                
                # Alpha-beta pruning
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            
            self.current_player = player_before
            return {'score': best_score, 'move': best_move}
    
    def ai_move_easy(self):
        """Make a random move for easy AI difficulty."""
        empty_cells = self.get_empty_cells()
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.make_move(row, col)
    
    def ai_move_medium(self):
        """
        Make a move for medium AI difficulty.
        Has a chance to make the optimal move or a random move.
        """
        # 70% chance to make the optimal move, 30% chance to make a random move
        if random.random() < 0.7:
            self.ai_move_hard()
        else:
            self.ai_move_easy()
    
    def ai_move_hard(self):
        """Make the optimal move using minimax algorithm."""
        result = self.minimax(0, True)
        if 'move' in result and result['move']:
            row, col = result['move']
            self.make_move(row, col)
    
    def ai_move(self):
        """Make an AI move based on the current difficulty setting."""
        # Add a small delay to make it seem like the AI is "thinking"
        time.sleep(0.5)
        
        if self.ai_difficulty == "easy":
            self.ai_move_easy()
        elif self.ai_difficulty == "medium":
            self.ai_move_medium()
        else:  # hard
            self.ai_move_hard()

def get_player_move(game: TicTacToe) -> bool:
    """
    Get a move from the human player.
    
    Args:
        game: The TicTacToe game instance
        
    Returns:
        bool: True if a valid move was made, False otherwise
    """
    try:
        move = input("Enter your move (row,col) or 'q' to quit: ")
        
        if move.lower() == 'q':
            return False
        
        # Parse input
        parts = move.split(',')
        if len(parts) != 2:
            print("Invalid input format. Use 'row,col' (e.g., '1,2')")
            time.sleep(1)
            return True
        
        try:
            row = int(parts[0].strip()) - 1  # Convert to 0-based index
            col = int(parts[1].strip()) - 1  # Convert to 0-based index
            
            if not (0 <= row < 3 and 0 <= col < 3):
                print("Row and column must be between 1 and 3")
                time.sleep(1)
                return True
            
            if not game.make_move(row, col):
                print("Invalid move. Cell already occupied.")
                time.sleep(1)
                return True
            
            return True
            
        except ValueError:
            print("Row and column must be numbers")
            time.sleep(1)
            return True
            
    except KeyboardInterrupt:
        return False

def play_game():
    """Main game loop."""
    game = TicTacToe()
    
    # Game setup
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== Tic-Tac-Toe ===\n")
    print("1. Human vs Human")
    print("2. Human vs AI (Easy)")
    print("3. Human vs AI (Medium)")
    print("4. Human vs AI (Hard)")
    print("5. Quit")
    
    choice = input("\nSelect game mode: ")
    
    if choice == '1':
        game.ai_enabled = False
    elif choice == '2':
        game.ai_enabled = True
        game.ai_difficulty = "easy"
    elif choice == '3':
        game.ai_enabled = True
        game.ai_difficulty = "medium"
    elif choice == '4':
        game.ai_enabled = True
        game.ai_difficulty = "hard"
    elif choice == '5':
        return
    else:
        print("Invalid choice. Defaulting to Human vs Human.")
        game.ai_enabled = False
        time.sleep(1)
    
    # Main game loop
    while True:
        game.print_board()
        
        if game.game_over:
            play_again = input("\nPlay again? (y/n): ")
            if play_again.lower() != 'y':
                break
            game.reset_game()
            continue
        
        if game.ai_enabled and game.current_player == 'O':
            game.ai_move()
        else:
            if not get_player_move(game):
                break
    
    print("\nThanks for playing!")

if __name__ == "__main__":
    play_game()
