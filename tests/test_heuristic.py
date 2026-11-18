import unittest

from game.board import Board
from solver.heuristic import evaluate, snake_weights, snake_with_bonus


class TestSnakeWeights(unittest.TestCase):
    def test_path_snakes_from_top_left(self):
        weights = snake_weights(3)
        self.assertEqual(weights, [
            [256, 128, 64],
            [8, 16, 32],
            [4, 2, 1],
        ])

    def test_each_weight_is_used_once(self):
        flat = [weight for row in snake_weights(4) for weight in row]
        self.assertEqual(sorted(flat), [2 ** rank for rank in range(16)])


class TestEvaluate(unittest.TestCase):
    def test_big_tile_in_the_corner_is_better(self):
        corner = Board(2, [[8, 0], [0, 0]])
        far = Board(2, [[0, 0], [8, 0]])
        self.assertGreater(evaluate(corner), evaluate(far))

    def test_ordered_row_is_better(self):
        ordered = Board(2, [[8, 4], [0, 0]])
        mixed = Board(2, [[4, 8], [0, 0]])
        self.assertGreater(evaluate(ordered), evaluate(mixed))

    def test_hand_computed_value(self):
        # 8 * 1 + 4 * 0.5 = 10
        board = Board(2, [[8, 4], [0, 0]])
        self.assertAlmostEqual(evaluate(board), 10)

    def test_board_is_untouched(self):
        board = Board(2, [[8, 4], [2, 0]])
        evaluate(board)
        self.assertEqual(board.grid, [[8, 4], [2, 0]])


class TestSnakeWithBonus(unittest.TestCase):
    def test_empty_cells_help(self):
        # same snake score, one board has more room
        open_board = Board(2, [[8, 0], [0, 0]])
        tight = Board(2, [[4, 8], [0, 0]])
        self.assertGreater(snake_with_bonus(open_board), snake_with_bonus(tight))

    def test_hand_computed_value(self):
        # snake score 10, two empty cells
        board = Board(2, [[8, 4], [0, 0]])
        self.assertAlmostEqual(snake_with_bonus(board), 10 * 1.2)


if __name__ == "__main__":
    unittest.main()
