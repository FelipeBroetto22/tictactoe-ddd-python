from dataclasses import dataclass
from enum import Enum

from src.domain.exceptions import InvalidPosition


class Symbol(Enum):
    X = "X"
    O = "O"

    def opponent(self):
        return Symbol.O if self == Symbol.X else Symbol.X


class MatchStatus(Enum):
    IN_PROGRESS = "in progress"
    WON = "won"
    DRAW = "draw"


@dataclass(frozen=True)
class Position:
    row: int
    column: int

    def __post_init__(self):
        if not (0 <= self.row <= 2 and 0 <= self.column <= 2):
            raise InvalidPosition()
