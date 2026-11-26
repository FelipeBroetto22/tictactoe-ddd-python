# Tic-Tac-Toe: DDD and Clean Architecture in Python

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Dependencies](https://img.shields.io/badge/dependencies-none-green)
![Tests](https://img.shields.io/badge/tests-unittest-informational)

A command-line Tic-Tac-Toe game built to practice **Domain-Driven Design (DDD)** and **Clean Architecture**. The game is intentionally simple. The goal is to show how to keep the game rules independent from the user interface and from storage.

Class and method names are in Portuguese on purpose. They are the project's ubiquitous language (see the glossary below).

## Getting started

Requires Python 3.10 or newer. There are no external dependencies.

```bash
git clone https://github.com/FelipeBroetto22/tictactoe-ddd-python.git
cd tictactoe-ddd-python
python main.py
```

Player `X` goes first. Enter a row and a column from 1 to 3.

```text
 X | O |
---+---+---
   | X |
---+---+---
   |   |

Player X's turn
Row:
```

Run the tests:

```bash
python -m unittest discover -s tests -t .
```

## Architecture

Dependencies always point toward the domain:

```text
Presentation  ---->  Application  ---->  Domain  <----  Infrastructure
 (cli.py)            (use cases)         (rules)        (in-memory repository)
```

The domain has no `print()`, no `input()` and no knowledge of where the match is stored. Swapping the terminal for a GUI, or memory for a file, does not touch the game rules.

| Layer | Folder | Contents |
|-------|--------|----------|
| Domain | `src/domain` | `Partida`, `Tabuleiro`, `Posicao`, `Simbolo`, domain exceptions, repository interface |
| Application | `src/application` | `IniciarPartida` and `FazerJogada` use cases |
| Infrastructure | `src/infrastructure` | `MemoriaRepository`, an in-memory repository |
| Presentation | `src/presentation` | `InterfaceTerminal`, the terminal UI |

`main.py` creates the repository, the use cases and the terminal UI, and connects them.

## Ubiquitous language

| Term | Meaning |
|------|---------|
| `Partida` | A match, from start to finish. It is the main entity. |
| `Tabuleiro` | The 3x3 board. |
| `Posicao` | A cell (row and column, from 0 to 2). Value object. |
| `Simbolo` | `X` or `O`. |
| `StatusPartida` | `EM_ANDAMENTO` (in progress), `VENCIDA` (won) or `EMPATADA` (draw). |
| `fazer_jogada` | Make a move. |
| `verificar_vencedor` | Check for a winner. |

## Game rules handled

- Win by row, column or diagonal.
- Draw when the board is full with no winner.
- Move on an occupied cell.
- Move outside the board.
- Move after the match has ended.

An invalid move raises a domain exception before any state changes, so the turn does not switch by mistake.

## Project structure

```text
.
├── main.py
├── docs/
│   ├── ddd.md
│   └── arquitetura_limpa.md
├── src/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── presentation/
└── tests/
    └── test_partida.py
```

## Documentation

- [docs/ddd.md](docs/ddd.md): the DDD concepts used and why the rules live in `Partida`.
- [docs/arquitetura_limpa.md](docs/arquitetura_limpa.md): the layers, the dependency direction and the path of a move from the terminal to the board.
