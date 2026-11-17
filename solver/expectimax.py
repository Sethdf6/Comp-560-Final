"""Expectimax search for the next 2048 move."""

from game.game_mechanics import move_down, move_left, move_right, move_up
from solver.chance import chance_value


MOVES = (
    ("left", move_left),
    ("right", move_right),
    ("up", move_up),
    ("down", move_down),
)


def _max_node(board, depth, evaluate):
    if depth == 0:
        return None, evaluate(board)

    best_direction = None
    best_value = float("-inf")
    for direction, move in MOVES:
        moved, gained = move(board)
        if moved.grid == board.grid:
            continue

        # One depth level represents one player move followed by its random spawn.
        value = gained + chance_value(
            moved, lambda spawned: _max_node(spawned, depth - 1, evaluate)[1]
        )
        if value > best_value:
            best_direction, best_value = direction, value

    if best_direction is None:
        return None, evaluate(board)
    return best_direction, best_value


def best_move(board, evaluate, depth=2):
    """Choose the legal move with the highest expected value, or None at game over.

    Depth counts player moves, including the move returned by this function.
    ``evaluate`` scores leaf and terminal boards; the caller supplies the heuristic.
    """
    if not isinstance(depth, int) or depth < 1:
        raise ValueError("depth must be a positive integer")
    return _max_node(board, depth, evaluate)[0]
