from src.domain.entities import Match


class StartMatch:
    def __init__(self, repository):
        self.repository = repository

    def execute(self):
        match = Match()
        self.repository.save(match)
        return match
