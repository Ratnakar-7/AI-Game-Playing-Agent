
# Havannah GamePlaying AI Agent

## Introduction

This project implements a Game Playing AI agent for the game **Havannah**. The objective of this AI is to make decisions in a time-constrained environment with a large state space, taking into account the actions of the opponent. The AI determines optimal moves based on board states, aiming to meet winning conditions while considering time limitations.

## Havannah: Game Overview

Havannah is a two-player game played on a hexagonal grid, where each player takes turns to place pieces on the board. The game ends when one player completes one of the following structures:
1. **Bridge**: Connects two of the six corner cells of the board.
2. **Fork**: Connects three different edge cells of the board.
3. **Ring**: Forms a closed loop of pieces, surrounding at least one empty cell.

## Winning Criteria

The player who completes any one of the three winning structures first is declared the winner. Alternatively, if a player's time runs out, the opponent wins.


## How to Run

### Start a Game

You can start a game between two players by running:

```bash
python game.py <player1> <player2> [--flag_field flag_value]
```

#### Example Commands

- **Human vs Human (6x6 board with 10-minute time limit):**
  ```bash
  python game.py human human --dim 6 --time 600
  ```

- **AI vs Random Agent (5x5 board with 1000-second time limit):**
  ```bash
  python game.py ai random --dim 5 --time 1000
  ```

- **AI vs AI (custom board layout):**
  ```bash
  python game.py ai ai2 --start_file custom_layout.txt
  ```

### Parameters

| Parameter  | Description | Possible Values | Default |
|------------|-------------|-----------------|---------|
| player1, player2 | Type of player | ["ai", "ai2", "random", "human"] | N/A |
| time | Time budget (in seconds) for each player | Positive integer | 240 |
| dim | Board size | Integer ∈ [4, 10] | 4 |
| mode | GUI or server mode | ["gui", "server"] | "gui" |
| start_file | Custom board layout | File path | None |

## AI Agent Implementation

### Key Features

1. **Initialization**: The AI agent is initialized with its player number and the opponent’s number to distinguish between moves and operates with a timer to manage time constraints.
  
2. **Memoization**: Previously evaluated board states are stored in a table to avoid recalculating the same states, optimizing decision-making.

3. **Minimax Algorithm with Alpha-Beta Pruning**: The AI uses the Minimax algorithm with alpha-beta pruning, which simulates potential game outcomes while pruning irrelevant branches, reducing computational complexity.

4. **Search Depth**: The search depth is limited to a maximum of 2 to maintain a balance between performance and computational cost.

5. **Time Management**: The agent employs a timer to ensure it does not exceed the allotted time. A timeout error is raised if calculations take too long.

6. **Randomness in Moves**: The AI shuffles valid moves with a 0.6 probability, introducing a level of randomness and unpredictability in its strategy.

7. **Evaluation Function**: The evaluation function assesses the current board state by comparing the potential success of the player and the opponent, factoring in future win opportunities.

8. **Strategic Move Selection**: The AI simulates possible moves and evaluates if they lead to victory, prioritizing moves with higher strategic value.

9. **Early Stopping**: The minimax algorithm includes early stopping when better move options have already been explored, increasing the agent’s efficiency.

10. **Optimal Move Selection**: The agent ultimately selects the move with the highest evaluation score, balancing both short-term and long-term strategic benefits.

### Core Function

The core AI logic is implemented in the `ai.py` file, with the function:

```python
def get_move(state):
    """Returns the next move as an (i, j) tuple based on the current board state."""
```

## Evaluation

The performance of the AI agent is evaluated by the following:
- **Win/Loss**: Winning earns 1 point, losing earns 0.
- **Draws**: Partial credit is given based on remaining time relative to the opponent's remaining time.

Agents that win faster receive higher marks.


---

