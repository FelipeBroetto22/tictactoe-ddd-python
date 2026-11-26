from src.domain.exceptions import MatchNotFound
from src.domain.value_objects import Position


class MakeMove:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, row, column):
        match = self.repository.find()
        if match is None:
            raise MatchNotFound()

        match.make_move(Position(row, column))
        self.repository.save(match)
        return match
