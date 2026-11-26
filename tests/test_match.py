import unittest

from src.application.make_move import MakeMove
from src.application.start_match import StartMatch
from src.domain.exceptions import InvalidPosition, MatchFinished, PositionOccupied
from src.domain.value_objects import MatchStatus, Position, Symbol
from src.infrastructure.in_memory_repository import InMemoryRepository


class TestMatch(unittest.TestCase):
    def setUp(self):
        repository = InMemoryRepository()
        StartMatch(repository).execute()
        self.make_move = MakeMove(repository)

    def play(self, moves):
        for row, column in moves:
            match = self.make_move.execute(row, column)
        return match

    def test_win_by_row(self):
        match = self.play([(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)])
        self.assertEqual(match.status, MatchStatus.WON)
        self.assertEqual(match.winner, Symbol.X)

    def test_win_by_column(self):
        match = self.play([(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)])
        self.assertEqual(match.winner, Symbol.X)

    def test_win_by_diagonal(self):
        match = self.play([(0, 0), (0, 1), (1, 1), (0, 2), (2, 2)])
        self.assertEqual(match.winner, Symbol.X)

    def test_o_wins(self):
        match = self.play([(0, 0), (1, 0), (0, 1), (1, 1), (2, 2), (1, 2)])
        self.assertEqual(match.winner, Symbol.O)

    def test_draw(self):
        match = self.play(
            [(0, 0), (0, 1), (0, 2), (1, 1), (1, 0), (1, 2), (2, 1), (2, 0), (2, 2)]
        )
        self.assertEqual(match.status, MatchStatus.DRAW)
        self.assertIsNone(match.winner)

    def test_position_occupied(self):
        self.play([(1, 1)])
        with self.assertRaises(PositionOccupied):
            self.make_move.execute(1, 1)

    def test_outside_the_board(self):
        with self.assertRaises(InvalidPosition):
            self.make_move.execute(3, 0)
        with self.assertRaises(InvalidPosition):
            self.make_move.execute(0, -1)

    def test_invalid_move_does_not_switch_turn(self):
        self.play([(1, 1)])
        with self.assertRaises(PositionOccupied):
            self.make_move.execute(1, 1)
        match = self.play([(0, 0)])
        self.assertEqual(match.board.symbol_at(Position(0, 0)), Symbol.O)

    def test_match_finished(self):
        self.play([(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)])
        with self.assertRaises(MatchFinished):
            self.make_move.execute(2, 2)


if __name__ == "__main__":
    unittest.main()
