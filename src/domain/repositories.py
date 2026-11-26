from abc import ABC, abstractmethod


class MatchRepository(ABC):
    @abstractmethod
    def save(self, match):
        pass

    @abstractmethod
    def find(self):
        pass
