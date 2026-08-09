# Tic-Tac-Toe AI

An implementation of the classic Tic-Tac-Toe game in Python featuring an unbeatable AI opponent powered by the **Minimax** algorithm.

## Features

* Human vs AI gameplay
* Unbeatable AI using the Minimax with Alpha-Beta Pruning
* Terminal-based interface
* Move validation
* Win, loss, and draw detection
* Object-oriented design

## Project Structure

```text
.
├── Board.py      # Board representation and game logic
├── AI_Mover.py         # Minimax implementation
├── main.py       # Game loop
└── README.md
```

## Requirements

* Python 3.14+

No third-party libraries are required.

## Running the Project

```bash
git clone https://github.com/gulu375/CODSOFT_TASK2
cd CODSOFT_TASK2
python main.py
```

## How It Works

The game uses the **Minimax** algorithm to evaluate every possible game state and select the optimal move. Assuming perfect play from both players, the AI will never lose.

## License

This project is intended for educational purposes.
