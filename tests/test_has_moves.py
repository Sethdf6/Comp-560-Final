import unittest

from game.board import Board
from game.game_mechanics import has_moves


class TestHasMoves(unittest.TestCase):
    def test_empty_board_has_no_moves(self):
        self.assertFalse(has_moves(Board(4)))

    def test_one_tile_can_move(self):
        self.assertTrue(has_moves(Board(2, [[2, 0], [0, 0]])))

    def test_full_board_with_a_merge(self):
        self.assertTrue(has_moves(Board(2, [[2, 2], [4, 8]])))

    def test_full_board_without_a_merge(self):
        self.assertFalse(has_moves(Board(2, [[2, 4], [4, 2]])))


if __name__ == "__main__":
    unittest.main()
