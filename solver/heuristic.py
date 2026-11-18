# heuristic for the leaves of the search
# takes a board, returns a number, higher is better

# how much one empty cell is worth next to the snake score
EMPTY_WEIGHT = 0.1

_weights_cache = {}


def snake_weights(size):
    # weights fall along a snake path that starts in the top left corner
    # row 0 goes left to right, row 1 right to left, and so on
    if size not in _weights_cache:
        weights = [[0] * size for _ in range(size)]
        rank = size * size - 1

        for row in range(size):
            cols = range(size) if row % 2 == 0 else range(size - 1, -1, -1)
            for col in cols:
                weights[row][col] = 2 ** rank
                rank -= 1

        _weights_cache[size] = weights

    return _weights_cache[size]


def snake_score(board):
    # big tiles should sit early on the snake path, in order
    weights = snake_weights(board.size)
    total = 0

    for row in range(board.size):
        for col in range(board.size):
            total += board.grid[row][col] * weights[row][col]

    # scale so the best cell has weight 1
    return total / weights[0][0]


def evaluate(board):
    # snake order keeps the board tidy, empty cells keep it alive
    empty = len(board.get_empty_cells())
    return snake_score(board) * (1 + EMPTY_WEIGHT * empty)
