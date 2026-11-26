from src.domain.repositories import MatchRepository


class InMemoryRepository(MatchRepository):
    def __init__(self):
        self._match = None

    def save(self, match):
        self._match = match

    def find(self):
        return self._match
