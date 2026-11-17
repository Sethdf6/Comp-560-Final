# chance node for expectimax
# after a move the game drops one tile in a random empty cell
# we do not guess where it lands, we weigh every option

# same odds as add_random_tile in game_state
SPAWN_ODDS = ((2, 0.9), (4, 0.1))


def spawn_outcomes(board):
    # every board the next spawn can produce, as (probability, board)
    empty_cells = board.get_empty_cells()
    if not empty_cells:
        return []

    cell_odds = 1 / len(empty_cells)
    outcomes = []

    for row, col in empty_cells:
        for value, value_odds in SPAWN_ODDS:
            new_board = board.copy()
            new_board.set_tile(row, col, value)
            outcomes.append((cell_odds * value_odds, new_board))

    return outcomes


def chance_value(board, value_fn):
    # expected value of a board that is waiting for its new tile
    # value_fn takes a board and returns a number
    outcomes = spawn_outcomes(board)

    # full board, nothing can spawn
    if not outcomes:
        return value_fn(board)

    return sum(odds * value_fn(new_board) for odds, new_board in outcomes)
