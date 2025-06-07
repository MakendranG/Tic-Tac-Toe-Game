#!/usr/bin/env python3

import pygame
import sys
import time
import random
from typing import List, Tuple, Optional, Dict, Union

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
BOARD_SIZE = 450
CELL_SIZE = BOARD_SIZE // 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Clock to control game speed
clock = pygame.time.Clock()

# Fonts
font_small = pygame.font.Font(None, 24)
font_medium = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 72)

class Button:
    def __init__(self, x, y, width, height, text, color=BLUE, hover_color=DARK_GRAY, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border
        
        text_surface = font_medium.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

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
        self.board_rect = pygame.Rect(
            (SCREEN_WIDTH - BOARD_SIZE) // 2,
            (SCREEN_HEIGHT - BOARD_SIZE) // 2,
            BOARD_SIZE,
            BOARD_SIZE
        )
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.moves_count = 0
    
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
        if self.ai_difficulty == "easy":
            self.ai_move_easy()
        elif self.ai_difficulty == "medium":
            self.ai_move_medium()
        else:  # hard
            self.ai_move_hard()
    
    def handle_click(self, mouse_pos):
        """
        Handle mouse click on the board.
        
        Args:
            mouse_pos: (x, y) position of the mouse click
        
        Returns:
            bool: True if a move was made, False otherwise
        """
        if self.game_over:
            return False
            
        # Check if click is within the board
        if not self.board_rect.collidepoint(mouse_pos):
            return False
            
        # Calculate which cell was clicked
        x, y = mouse_pos
        col = (x - self.board_rect.x) // CELL_SIZE
        row = (y - self.board_rect.y) // CELL_SIZE
        
        # Make the move
        return self.make_move(row, col)
    
    def draw(self, surface):
        """Draw the game board and pieces."""
        # Draw board background
        pygame.draw.rect(surface, WHITE, self.board_rect)
        pygame.draw.rect(surface, BLACK, self.board_rect, 3)
        
        # Draw grid lines
        for i in range(1, 3):
            # Vertical lines
            pygame.draw.line(
                surface, BLACK,
                (self.board_rect.x + i * CELL_SIZE, self.board_rect.y),
                (self.board_rect.x + i * CELL_SIZE, self.board_rect.y + BOARD_SIZE),
                3
            )
            # Horizontal lines
            pygame.draw.line(
                surface, BLACK,
                (self.board_rect.x, self.board_rect.y + i * CELL_SIZE),
                (self.board_rect.x + BOARD_SIZE, self.board_rect.y + i * CELL_SIZE),
                3
            )
        
        # Draw X's and O's
        for row in range(3):
            for col in range(3):
                cell_content = self.board[row][col]
                if cell_content != ' ':
                    cell_rect = pygame.Rect(
                        self.board_rect.x + col * CELL_SIZE,
                        self.board_rect.y + row * CELL_SIZE,
                        CELL_SIZE, CELL_SIZE
                    )
                    
                    if cell_content == 'X':
                        # Draw X
                        padding = CELL_SIZE * 0.2
                        pygame.draw.line(
                            surface, BLUE,
                            (cell_rect.x + padding, cell_rect.y + padding),
                            (cell_rect.x + CELL_SIZE - padding, cell_rect.y + CELL_SIZE - padding),
                            8
                        )
                        pygame.draw.line(
                            surface, BLUE,
                            (cell_rect.x + CELL_SIZE - padding, cell_rect.y + padding),
                            (cell_rect.x + padding, cell_rect.y + CELL_SIZE - padding),
                            8
                        )
                    else:  # O
                        # Draw O
                        center = (cell_rect.x + CELL_SIZE // 2, cell_rect.y + CELL_SIZE // 2)
                        radius = CELL_SIZE // 2 - CELL_SIZE * 0.2
                        pygame.draw.circle(surface, RED, center, radius, 8)
        
        # Draw game status
        status_rect = pygame.Rect(0, 50, SCREEN_WIDTH, 50)
        
        if self.game_over:
            if self.winner:
                status_text = f"Player {self.winner} wins!"
                status_color = BLUE if self.winner == 'X' else RED
            else:
                status_text = "It's a draw!"
                status_color = BLACK
        else:
            if self.ai_enabled and self.current_player == 'O':
                status_text = "AI's turn (O)"
            else:
                status_text = f"Player {self.current_player}'s turn"
            status_color = BLUE if self.current_player == 'X' else RED
        
        status_surface = font_medium.render(status_text, True, status_color)
        status_rect = status_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        surface.blit(status_surface, status_rect)

class GameMenu:
    def __init__(self):
        self.buttons = []
        self.create_buttons()
        
    def create_buttons(self):
        button_width = 250
        button_height = 50
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        
        # Game mode buttons
        self.human_vs_human_button = Button(center_x, 150, button_width, button_height, "Human vs Human", GREEN)
        self.human_vs_ai_easy_button = Button(center_x, 220, button_width, button_height, "Human vs AI (Easy)", BLUE)
        self.human_vs_ai_medium_button = Button(center_x, 290, button_width, button_height, "Human vs AI (Medium)", BLUE)
        self.human_vs_ai_hard_button = Button(center_x, 360, button_width, button_height, "Human vs AI (Hard)", RED)
        self.quit_button = Button(center_x, 430, button_width, button_height, "Quit", DARK_GRAY)
        
        self.buttons = [
            self.human_vs_human_button,
            self.human_vs_ai_easy_button,
            self.human_vs_ai_medium_button,
            self.human_vs_ai_hard_button,
            self.quit_button
        ]
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        for button in self.buttons:
            button.check_hover(mouse_pos)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.human_vs_human_button.is_clicked(mouse_pos, True):
                    return {"action": "start_game", "ai_enabled": False}
                elif self.human_vs_ai_easy_button.is_clicked(mouse_pos, True):
                    return {"action": "start_game", "ai_enabled": True, "difficulty": "easy"}
                elif self.human_vs_ai_medium_button.is_clicked(mouse_pos, True):
                    return {"action": "start_game", "ai_enabled": True, "difficulty": "medium"}
                elif self.human_vs_ai_hard_button.is_clicked(mouse_pos, True):
                    return {"action": "start_game", "ai_enabled": True, "difficulty": "hard"}
                elif self.quit_button.is_clicked(mouse_pos, True):
                    return {"action": "quit"}
        
        return {"action": "none"}
    
    def draw(self, surface):
        # Draw background
        surface.fill(LIGHT_GRAY)
        
        # Draw title
        title_text = font_large.render("Tic-Tac-Toe", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title_text, title_rect)
        
        # Draw all buttons
        for button in self.buttons:
            button.draw(surface)

def main():
    # Game states
    MENU = 0
    PLAYING = 1
    
    current_state = MENU
    menu = GameMenu()
    game = TicTacToe()
    
    # For AI thinking delay
    ai_thinking = False
    ai_move_time = 0
    
    # Main game loop
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if current_state == PLAYING:
                        current_state = MENU
                    else:
                        running = False
                elif event.key == pygame.K_r and current_state == PLAYING:
                    # Reset game
                    game.reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if current_state == PLAYING and not ai_thinking:
                    if game.game_over:
                        # If game is over, clicking anywhere resets
                        game.reset_game()
                    else:
                        # Handle player move
                        if game.current_player == 'X' or not game.ai_enabled:
                            game.handle_click(pygame.mouse.get_pos())
                            
                            # If AI's turn after player move
                            if game.ai_enabled and game.current_player == 'O' and not game.game_over:
                                ai_thinking = True
                                ai_move_time = pygame.time.get_ticks() + 500  # Add delay for AI move
        
        # Handle game states
        if current_state == MENU:
            result = menu.handle_events(events)
            
            if result["action"] == "start_game":
                game.reset_game()
                game.ai_enabled = result["ai_enabled"]
                if game.ai_enabled:
                    game.ai_difficulty = result["difficulty"]
                current_state = PLAYING
            elif result["action"] == "quit":
                running = False
            
            menu.draw(screen)
            
        elif current_state == PLAYING:
            # Handle AI move with delay
            if ai_thinking and pygame.time.get_ticks() >= ai_move_time:
                game.ai_move()
                ai_thinking = False
            
            # Draw game
            screen.fill(LIGHT_GRAY)
            game.draw(screen)
            
            # Draw back button
            back_text = font_small.render("Press ESC for Menu | R to Reset", True, BLACK)
            back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
            screen.blit(back_text, back_rect)
            
            # Draw game over message and reset prompt
            if game.game_over:
                if game.winner:
                    color = BLUE if game.winner == 'X' else RED
                    message = f"Player {game.winner} wins!"
                else:
                    color = BLACK
                    message = "It's a draw!"
                
                # Draw semi-transparent overlay
                overlay = pygame.Surface((SCREEN_WIDTH, 100), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, 200))
                screen.blit(overlay, (0, SCREEN_HEIGHT - 150))
                
                result_text = font_medium.render(message, True, color)
                result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 130))
                screen.blit(result_text, result_rect)
                
                reset_text = font_small.render("Click anywhere or press R to play again", True, BLACK)
                reset_rect = reset_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
                screen.blit(reset_text, reset_rect)
        
        # Update the display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
