import random
from game.board import Board
from game.game_mechanics import *

class GameState:
    def __init__(self, size=4):
        self.board = Board(size)
        self.score = 0
        self.game_over = False
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty_cells = self.board.get_empty_cells()
        if not empty_cells:
            return
        row,col = random.choice(empty_cells)
        value = 2 if random.random() < 0.9 else 4
        self.board.set_tile(row, col, value)

    def move(self, direction):
        if self.game_over:
            return False

        if direction == 'left':
            new_board, score = move_left(self.board)
        elif direction == 'right':
            new_board, score = move_right(self.board)
        elif direction == 'up':
            new_board, score = move_up(self.board)
        elif direction == 'down':
            new_board, score = move_down(self.board)
        else:
            return False

        if new_board.grid == self.board.grid:
            return False

        self.board = new_board
        self.score += score
        self.add_random_tile()

        self.game_over = not has_moves(self.board)

        return True