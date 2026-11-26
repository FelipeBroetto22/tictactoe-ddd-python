class DomainError(Exception):
    pass


class InvalidPosition(DomainError):
    def __init__(self):
        super().__init__("That position is outside the board.")


class PositionOccupied(DomainError):
    def __init__(self):
        super().__init__("That position is already occupied.")


class MatchFinished(DomainError):
    def __init__(self):
        super().__init__("The match is already over.")


class MatchNotFound(DomainError):
    def __init__(self):
        super().__init__("There is no match in progress.")
