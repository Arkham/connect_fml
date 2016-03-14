import unittest
from board import *

class BoardTestCase(unittest.TestCase):
    def test_board_is_empty(self):
        board = Board()
        self.assertEqual(board.is_empty, True)

    def test_board_is_not_empty(self):
        board = Board().player_move('R', 0)
        self.assertEqual(board.is_empty, False)

    def test_board_is_full(self):
        board = Board(num_rows = 1, num_columns = 2)
        self.assertEqual(board.is_full, False)

        board = board.player_move('R', 0)
        self.assertEqual(board.is_full, False)

        board = board.player_move('Y', 1)
        self.assertEqual(board.is_full, True)

    def test_invalid_column(self):
        board = (Board(num_rows = 1, num_columns = 2)
            .player_move('R', 0))

        with self.assertRaises(InvalidColumnException):
            board.player_move('R', -1)

        with self.assertRaises(InvalidColumnException):
            board.player_move('R', 2)

    def test_invalid_player(self):
        board = (Board(num_rows = 1, num_columns = 2)
            .player_move('R', 0))

        with self.assertRaises(InvalidPlayerException):
            board.player_move('Z', -1)

    def test_columns_can_fill_up(self):
        board = (Board(num_rows = 2, num_columns = 3)
            .player_move('R', 0)
            .player_move('R', 0))

        with self.assertRaises(ColumnFullException):
            board.player_move('R', 0)

    def test_valid_moves(self):
        board = Board(num_rows = 1, num_columns = 3)
        self.assertEqual(board.valid_moves, [0, 1, 2])

        self.assertEqual(board.player_move('R', 0).valid_moves, [1, 2])

    def test_display_board(self):
        board = (Board(num_rows = 3, num_columns = 3)
            .player_move('R', 0)
            .player_move('Y', 1)
            .player_move('R', 2)
            .player_move('Y', 0)
            .player_move('R', 1)
            .player_move('Y', 2))

        self.assertEqual(board.__str__(), """. . .\nY R Y\nR Y R\n0 1 2""")

    def test_check_horizontal_win(self):
        board = (Board(num_rows = 2, num_columns = 3, required_to_win = 2)
            .player_move('R', 0)
            .player_move('Y', 2)
            .player_move('R', 1))

        status = board.status
        self.assertEqual(status.is_over, True)
        self.assertEqual(status.is_win, True)
        self.assertEqual(status.winner, 'R')

    def test_check_vertical_win(self):
        board = (Board(num_rows = 2, num_columns = 3, required_to_win = 2)
            .player_move('Y', 0)
            .player_move('R', 2)
            .player_move('Y', 0))

        status = board.status
        self.assertEqual(status.is_over, True)
        self.assertEqual(status.is_win, True)
        self.assertEqual(status.winner, 'Y')

    def test_check_diagonal_win(self):
        board = (Board(num_rows = 2, num_columns = 3, required_to_win = 2)
            .player_move('R', 0)
            .player_move('Y', 1)
            .player_move('R', 1))

        status = board.status
        self.assertEqual(status.is_over, True)
        self.assertEqual(status.is_win, True)
        self.assertEqual(status.winner, 'R')

    def test_check_other_diagonal_win(self):
        board = (Board(num_rows = 2, num_columns = 3, required_to_win = 2)
            .player_move('Y', 1)
            .player_move('R', 0)
            .player_move('Y', 0))

        status = board.status
        self.assertEqual(status.is_over, True)
        self.assertEqual(status.is_win, True)
        self.assertEqual(status.winner, 'Y')

    def test_check_draw(self):
        board = (Board(num_rows = 2, num_columns = 3, required_to_win = 3)
            .player_move('Y', 0)
            .player_move('R', 1)
            .player_move('Y', 2)
            .player_move('R', 0)
            .player_move('Y', 1)
            .player_move('R', 2))

        status = board.status
        self.assertEqual(status.is_over, True)
        self.assertEqual(status.is_draw, True)

    def test_check_still_playing(self):
        board = (Board(num_rows = 2, num_columns = 3, required_to_win = 3)
            .player_move('Y', 0)
            .player_move('R', 1))

        status = board.status
        self.assertEqual(status.is_over, False)

    def test_check_sub_matches(self):
        board = (Board(num_rows = 3, num_columns = 3, required_to_win = 3)
            .player_move('Y', 0)
            .player_move('Y', 1)
            .player_move('Y', 0)
            .player_move('Y', 1))

        self.assertEqual(board.match_subset('Y', 2), 5)

if __name__ == '__main__':
    unittest.main()
