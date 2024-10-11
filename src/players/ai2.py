
import time
import math
import random
import numpy as np
from typing import Tuple
from helper import get_valid_actions, check_win, fetch_remaining_time, get_neighbours


class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_moves = get_valid_actions(state)

    def expand(self, move, new_state):
        """Expand the node by creating a child with the given move and state."""
        child_node = MCTSNode(new_state, parent=self, move=move)
        self.children.append(child_node)
        return child_node

    def is_fully_expanded(self):
        """Return True if there are no more untried moves."""
        return len(self.untried_moves) == 0

    def best_child(self, exploration_weight=1.2):
        """Select the child node with the highest UCB1 score."""
        choices_weights = [
            (child.wins / child.visits) + exploration_weight * math.sqrt(math.log(self.visits) / child.visits)
            for child in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def backpropagate(self, result):
        """Propagate the result of the simulation up the tree."""
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(result)

    def is_terminal(self):
        """Check if this is a terminal node (game over)."""
        if len(get_valid_actions(self.state)) == 0:
            return True
        if self.move is None:  # Check for root node
            return False
        # Check if this move results in a win for either player
        return check_win(self.state, self.move, 1)[0] or check_win(self.state, self.move, 2)[0]

    def rollout(self, player_number):
        """Simulate the game from this node randomly until it ends."""
        current_state = self.state.copy()
        current_player = player_number

        while True:
            valid_moves = get_valid_actions(current_state)
            if not valid_moves:
                return 0.5  # Draw

            move = self._nearest_neighbor_preference(valid_moves, current_state, self.move)
            current_state[move] = current_player

            win, _ = check_win(current_state, move, current_player)
            if win:
                return 1 if current_player == player_number else 0

            current_player = 3 - current_player  # Switch player

    def _nearest_neighbor_preference(self, valid_moves, state, last_move):
        """Prefer moves that are near the last played move."""
        if last_move is None or random.random() < 0.5:  # 50% random, 50% nearest
            return random.choice(valid_moves)

        neighbors = get_neighbours(state.shape[0], last_move)
        close_moves = [move for move in valid_moves if move in neighbors]
        
        return random.choice(close_moves) if close_moves else random.choice(valid_moves)


class AIPlayer:
    def __init__(self, player_number: int, timer):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = f'Player {player_number}: ai'
        self.timer = timer

    def get_move(self, state: np.array) -> Tuple[int, int]:

        moves = get_valid_actions(state)
        for move in moves:
            new_state = state.copy()
            new_state[move] = 1
            if check_win(new_state,move,1)[0]:
                return move[0],move[1]
            
            new_state[move] = 2
            if check_win(new_state,move,2)[0]:
                return move[0],move[1]
        """Run MCTS to select the best move."""
        root = MCTSNode(state)
        start_time = time.time()
        time_limit = fetch_remaining_time(self.timer, self.player_number) * 0.9  # Leave buffer time

        max_iterations = 1000  # Add a maximum limit for iterations
        iterations = 0
        best_move = None

        # Perform as many MCTS iterations as possible within the time limit
        while time.time() - start_time < time_limit and iterations < max_iterations:
            node = self._select(root)
            if not node.is_terminal():
                node = self._expand(node)
            result = node.rollout(self.player_number)
            node.backpropagate(result)

            iterations += 1

        # Return the move with the highest number of visits or fallback
        if root.children:
            best_move = root.best_child(exploration_weight=0).move
        else:
            # Fallback to a random move if no children were expanded
            valid_moves = get_valid_actions(state)
            best_move = random.choice(valid_moves)

        return best_move

    def _select(self, node):
        """Select the most promising child node using UCB1 until we find a leaf node."""
        while not node.is_terminal():
            if not node.is_fully_expanded():
                return node
            else:
                node = node.best_child()
        return node

    def _expand(self, node):
        """Expand the node by trying one of its untried moves."""
        move = random.choice(node.untried_moves)
        node.untried_moves.remove(move)
        new_state = node.state.copy()
        new_state[move] = self.player_number
        return node.expand(move, new_state)

