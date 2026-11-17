from game.board import Board

def move_row_left(row):

    tiles = [tile for tile in row if tile != 0]
    new_row = []
    score = 0
    i=0

    while i < len(tiles):
        if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
            new_tile = tiles[i] * 2
            score += new_tile
            new_row.append(new_tile)
            i += 2
        else:
            new_row.append(tiles[i])
            i += 1

    new_row.extend([0] * (len(row) - len(new_row)))
    return new_row, score

def move_left(board):
    new_grid = []
    total_score = 0

    for row in board.grid:
        new_row, score = move_row_left(row)
        new_grid.append(new_row)
        total_score += score

    return Board(board.size, new_grid), total_score

def move_right(board):
    new_grid = []
    total_score = 0

    for row in board.grid:
        reversed_row = row[::-1]
        new_row, score = move_row_left(reversed_row)
        new_grid.append(new_row[::-1])
        total_score += score

    return Board(board.size, new_grid), total_score

def move_up(board):
    new_grid = [list(row) for row in zip(*board.grid)] 
    new_board = Board(board.size, new_grid)
    changed_board, total_score = move_left(new_board)
    changed_board.grid = [list(row) for row in zip(*changed_board.grid)]
    return changed_board, total_score

def move_down(board):
    new_grid = [list(row) for row in zip(*board.grid)]
    new_board = Board(board.size, new_grid)
    changed_board, total_score = move_right(new_board)

    changed_board.grid = [list(row) for row in zip(*changed_board.grid)]
    return changed_board, total_score


def has_moves(board):
    if not board.is_board_full():
        return True

    for i in range(board.size):
        for j in range(board.size):
            current_tile = board.get_tile(i, j)
            if (i + 1 < board.size and current_tile == board.get_tile(i + 1, j)) or (j + 1 < board.size and current_tile == board.get_tile(i, j + 1)):
                return True

    return False