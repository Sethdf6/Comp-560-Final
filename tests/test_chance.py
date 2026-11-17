import random
import unittest

from game.board import Board
from game.game_state import GameState
from solver.chance import spawn_outcomes, chance_value


def tile_sum(board):
    return sum(sum(row) for row in board.grid)


def make_board(grid):
    return Board(len(grid), grid)


class TestSpawnOutcomes(unittest.TestCase):
    def setUp(self):
        self.board = make_board([
            [2, 0, 4, 8],
            [0, 16, 0, 2],
            [4, 2, 32, 0],
            [0, 8, 2, 0],
        ])

    def test_two_outcomes_per_empty_cell(self):
        outcomes = spawn_outcomes(self.board)
        self.assertEqual(len(outcomes), 2 * len(self.board.get_empty_cells()))

    def test_odds_sum_to_one(self):
        total = sum(odds for odds, _ in spawn_outcomes(self.board))
        self.assertAlmostEqual(total, 1.0)

    def test_each_outcome_adds_one_tile(self):
        empty_cells = set(self.board.get_empty_cells())
        seen = set()

        for odds, new_board in spawn_outcomes(self.board):
            changed = [
                (i, j)
                for i in range(self.board.size)
                for j in range(self.board.size)
                if new_board.grid[i][j] != self.board.grid[i][j]
            ]
            self.assertEqual(len(changed), 1)

            row, col = changed[0]
            value = new_board.grid[row][col]
            self.assertIn((row, col), empty_cells)
            self.assertIn(value, (2, 4))

            expected = (0.9 if value == 2 else 0.1) / len(empty_cells)
            self.assertAlmostEqual(odds, expected)
            seen.add((row, col, value))

        # no option is missing or repeated
        self.assertEqual(len(seen), 2 * len(empty_cells))

    def test_original_board_is_untouched(self):
        before = [row.copy() for row in self.board.grid]
        spawn_outcomes(self.board)
        self.assertEqual(self.board.grid, before)

    def test_full_board_has_no_outcomes(self):
        full = make_board([[2, 4], [8, 16]])
        self.assertEqual(spawn_outcomes(full), [])

    def test_single_empty_cell(self):
        board = make_board([[2, 4], [8, 0]])
        outcomes = sorted(
            (new_board.grid[1][1], odds) for odds, new_board in spawn_outcomes(board)
        )
        self.assertEqual([value for value, _ in outcomes], [2, 4])
        self.assertAlmostEqual(outcomes[0][1], 0.9)
        self.assertAlmostEqual(outcomes[1][1], 0.1)


class TestChanceValue(unittest.TestCase):
    def test_hand_computed_value(self):
        # the new tile is worth 0.9 * 2 + 0.1 * 4 = 2.2 on average
        board = make_board([[2, 0], [0, 4]])
        self.assertAlmostEqual(chance_value(board, tile_sum), 6 + 2.2)

    def test_full_board_uses_value_fn(self):
        full = make_board([[2, 4], [8, 16]])
        self.assertEqual(chance_value(full, tile_sum), 30)

    def test_weights_each_cell_equally(self):
        # value 1 only when the tile lands in the top right corner
        board = make_board([[2, 0], [0, 0]])
        value = chance_value(board, lambda b: 1 if b.grid[0][1] != 0 else 0)
        self.assertAlmostEqual(value, 1 / 3)

    def test_matches_the_real_game(self):
        # sample the real spawn many times and compare the average
        self.addCleanup(random.setstate, random.getstate())
        random.seed(560)
        start = make_board([
            [2, 0, 4, 8],
            [0, 16, 0, 2],
            [4, 2, 32, 0],
            [0, 8, 2, 0],
        ])

        def value_fn(board):
            # depends on both the cell and the tile value
            return sum(
                (i * 4 + j + 1) * board.grid[i][j]
                for i in range(4)
                for j in range(4)
            )

        game = GameState()
        runs = 50000
        total = 0

        for _ in range(runs):
            game.board = start.copy()
            game.add_random_tile()
            total += value_fn(game.board)

        expected = chance_value(start, value_fn)
        self.assertAlmostEqual(total / runs, expected, delta=0.5)
