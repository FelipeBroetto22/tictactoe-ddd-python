# Clean Architecture in Tic-Tac-Toe

This document explains how I split the project into layers and why. What I took from Clean Architecture is that the game rules must not depend on details such as the terminal or where data is stored. The details depend on the rules.

In practice: the win rule is separate from the terminal because, if I later replace `print`/`input` with a graphical interface, I do not have to rewrite the game rules.

## The layers

```text
src/
  domain/          game rules
  application/     use cases
  infrastructure/  technical details (storage)
  presentation/    talks to the user (terminal)
main.py            wires everything together
```

- **domain**: `Partida`, `Tabuleiro`, `Posicao`, `Simbolo`, the exceptions and the repository interface. It has no `print()` or `input()` and imports nothing from the other folders.
- **application**: `IniciarPartida` and `FazerJogada`. Each use case is one thing the user wants to do. It fetches the match, asks it to play and saves it again. The repository is received in `__init__`.
- **infrastructure**: `MemoriaRepository`, which keeps the match in an attribute. It implements the interface defined in the domain.
- **presentation**: `InterfaceTerminal` in `cli.py`. It draws the board, reads row and column and shows errors. It has no game rules.
- **main.py**: creates the repository, the use cases and the UI, and connects them.

## Dependency direction

```text
Presentation  ---->  Application  ---->  Domain  <----  Infrastructure
 (cli.py)            (use cases)         (rules)        (memoria_repository)
```

The arrows always point to the domain. The domain knows no one. The infrastructure also points to the domain, because it inherits from `PartidaRepository`. The use case only knows the repository interface and does not know it is in memory. `main.py` decides that.

To check, search for `print(` or `input(` inside `src/domain`: nothing shows up.

## What happens when the player enters a move

Example: the player enters row 2 and column 3.

1. `InterfaceTerminal` reads both numbers with `input()`. It shows 1 to 3 to the user and subtracts 1, because the domain uses 0 to 2.
2. It calls `FazerJogada.executar(1, 2)`.
3. The use case asks the repository for the match (`buscar`).
4. It creates `Posicao(1, 2)`. If it is outside the board, `PosicaoInvalida` is raised here.
5. It calls `partida.fazer_jogada(posicao)`. The match checks that it is still in progress, marks the cell on the `Tabuleiro` (`PosicaoOcupada` if occupied), checks for a win or draw and passes the turn.
6. The use case saves the match in the repository and returns it.
7. The terminal draws the board again. If a domain error came up along the way, it only shows the message and asks for another move.

## Swapping a detail

To save the match in a file, I would create an `ArquivoRepository` in the infrastructure inheriting from `PartidaRepository` and change one line in `main.py`. The domain, the use cases and the terminal stay as they are.

## Tests

`tests/test_partida.py` runs the use cases with the in-memory repository, without going through the terminal. That is only possible because the rules are separate from the interface. The tests cover wins by row, column and diagonal, draw, occupied cell, outside the board and a move after the end.
