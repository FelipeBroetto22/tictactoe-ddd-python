from src.application.make_move import MakeMove
from src.application.start_match import StartMatch
from src.infrastructure.in_memory_repository import InMemoryRepository
from src.presentation.cli import TerminalInterface


def main():
    repository = InMemoryRepository()
    interface = TerminalInterface(StartMatch(repository), MakeMove(repository))
    interface.play()


if __name__ == "__main__":
    main()
