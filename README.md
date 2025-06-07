# Tic-Tac-Toe Game

A classic Tic-Tac-Toe game implemented in Python with both text-based console and graphical interfaces. Play against another human or challenge the AI with different difficulty levels.

![Tic-Tac-Toe Game](https://via.placeholder.com/800x600?text=Tic-Tac-Toe+Game)

## Features

- **Two Game Interfaces**:
  - Text-based console interface (`tic_tac_toe.py`)
  - Graphical interface using PyGame (`tic_tac_toe_gui.py`)

- **Multiple Play Options**:
  - Human vs Human: Play against a friend on the same computer
  - Human vs AI: Challenge the computer with three difficulty levels
    - Easy: Makes random moves
    - Medium: Mix of random and optimal moves (70% optimal, 30% random)
    - Hard: Uses minimax algorithm with alpha-beta pruning for optimal play

- **Clean Interface**:
  - Intuitive controls
  - Visual feedback
  - Game status display

## Requirements

- Python 3.6 or higher
- PyGame (for the graphical version)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/tic-tac-toe-game.git
   cd tic-tac-toe-game
   ```

2. Install PyGame (required for the graphical version):
   ```
   pip install pygame
   ```
   
   Or install from the requirements file:
   ```
   pip install -r requirements.txt
   ```

## How to Play

### Text-Based Version

Run the text-based version:
```
python tic_tac_toe.py
```

- Follow the on-screen prompts to select game mode
- Enter moves in the format "row,col" (e.g., "1,2")
- Press 'q' to quit at any time

### Graphical Version

Run the graphical version:
```
python tic_tac_toe_gui.py
```

- Click on buttons to select game mode
- Click on the board to make moves
- Press 'R' to reset the current game
- Press 'ESC' to return to the main menu

## Game Rules

1. The game is played on a 3x3 grid
2. Player X goes first, followed by Player O
3. Players take turns placing their mark in an empty cell
4. The first player to get three of their marks in a row (horizontally, vertically, or diagonally) wins
5. If all cells are filled and no player has won, the game is a draw

## Implementation Details

### Minimax Algorithm

The AI uses the minimax algorithm with alpha-beta pruning to determine the optimal move:

- Recursively evaluates all possible game states
- Assigns scores to terminal states (win, loss, draw)
- Chooses the move that maximizes the AI's score while minimizing the player's score
- Alpha-beta pruning reduces the number of evaluated states for better performance

### Difficulty Levels

- **Easy**: Makes completely random moves
- **Medium**: 70% chance to make the optimal move, 30% chance to make a random move
- **Hard**: Always makes the optimal move using the full minimax algorithm

## Project Structure

- `tic_tac_toe.py`: Text-based console version
- `tic_tac_toe_gui.py`: Graphical version using PyGame
- `requirements.txt`: List of Python dependencies
- `README.md`: This documentation file

## Future Improvements

- Add sound effects
- Implement game statistics tracking
- Add animations for winning lines
- Create a networked multiplayer option
- Develop additional AI strategies

## License

This project is licensed under the MIT License - see the LICENSE file for details.
