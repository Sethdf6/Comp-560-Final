import unittest

from game.board import Board
from solver.expectimax import best_move


class TestExpectimax(unittest.TestCase):
    def test_only_legal_move_preserves_input(self):
        board = Board(2, [[2, 0], [4, 8]])
        self.assertEqual(best_move(board, lambda _: 0, depth=2), "right")
        self.assertEqual(board.grid, [[2, 0], [4, 8]])

    def test_merge_score_is_counted(self):
        board = Board(2, [[2, 2], [0, 0]])
        self.assertEqual(best_move(board, lambda _: 0, depth=1), "left")

    def test_search_depth_changes_decision(self):
        board = Board(2, [[0, 4], [0, 4]])
        free_spaces = lambda b: 100 * sum(tile == 0 for row in b.grid for tile in row)
        self.assertEqual(best_move(board, free_spaces, depth=1), "up")
        self.assertEqual(best_move(board, free_spaces, depth=2), "left")

    def test_terminal_board_has_no_move(self):
        board = Board(2, [[2, 4], [8, 16]])
        self.assertIsNone(best_move(board, lambda _: 0))


if __name__ == "__main__":
    unittest.main()
