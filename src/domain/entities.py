from src.domain.exceptions import MatchFinished, PositionOccupied
from src.domain.value_objects import MatchStatus, Position, Symbol

WINNING_LINES = [
    [Position(0, 0), Position(0, 1), Position(0, 2)],
    [Position(1, 0), Position(1, 1), Position(1, 2)],
    [Position(2, 0), Position(2, 1), Position(2, 2)],
    [Position(0, 0), Position(1, 0), Position(2, 0)],
    [Position(0, 1), Position(1, 1), Position(2, 1)],
    [Position(0, 2), Position(1, 2), Position(2, 2)],
    [Position(0, 0), Position(1, 1), Position(2, 2)],
    [Position(0, 2), Position(1, 1), Position(2, 0)],
]


class Board:
    def __init__(self):
        self._cells = {}

    def symbol_at(self, position):
        return self._cells.get(position)

    def is_occupied(self, position):
        return position in self._cells

    def mark(self, position, symbol):
        if self.is_occupied(position):
            raise PositionOccupied()
        self._cells[position] = symbol

    def is_full(self):
        return len(self._cells) == 9

    def find_winner(self):
        for line in WINNING_LINES:
            symbols = [self.symbol_at(position) for position in line]
            if symbols[0] is not None and symbols.count(symbols[0]) == 3:
                return symbols[0]
        return None


class Match:
    def __init__(self):
        self.board = Board()
        self.current_player = Symbol.X
        self.status = MatchStatus.IN_PROGRESS
        self.winner = None

    def make_move(self, position):
        if self.status != MatchStatus.IN_PROGRESS:
            raise MatchFinished()

        self.board.mark(position, self.current_player)

        winner = self.board.find_winner()
        if winner is not None:
            self.winner = winner
            self.status = MatchStatus.WON
        elif self.board.is_full():
            self.status = MatchStatus.DRAW
        else:
            self.current_player = self.current_player.opponent()
