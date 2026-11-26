from src.domain.exceptions import DomainError
from src.domain.value_objects import MatchStatus, Position


class TerminalInterface:
    def __init__(self, start_match, make_move):
        self.start_match = start_match
        self.make_move = make_move

    def play(self):
        match = self.start_match.execute()
        print("Tic-Tac-Toe")
        print("Enter row and column from 1 to 3.")

        while match.status == MatchStatus.IN_PROGRESS:
            self.show_board(match)
            print(f"Player {match.current_player.value}'s turn")
            try:
                row = int(input("Row: ")) - 1
                column = int(input("Column: ")) - 1
                match = self.make_move.execute(row, column)
            except ValueError:
                print("Enter numbers only.")
            except DomainError as error:
                print(error)

        self.show_board(match)
        if match.status == MatchStatus.WON:
            print(f"Player {match.winner.value} wins!")
        else:
            print("It's a draw.")

    def show_board(self, match):
        print()
        for row in range(3):
            cells = []
            for column in range(3):
                symbol = match.board.symbol_at(Position(row, column))
                cells.append(symbol.value if symbol else " ")
            print(" " + " | ".join(cells))
            if row < 2:
                print("---+---+---")
        print()
