# DDD in Tic-Tac-Toe

This document explains how I applied Domain-Driven Design to the game. The idea that helped me most is that the code should speak the same language as the problem. Anyone reading `partida.fazer_jogada(posicao)` understands what happens without knowing how it is implemented.

The names in the code are in Portuguese on purpose, because they are the project's ubiquitous language. The English meaning is next to each term.

## Ubiquitous language

- **Partida** (match): one game, from start to finish.
- **Tabuleiro** (board): the 3x3 grid.
- **Posicao** (position): a cell of the board, with row and column from 0 to 2.
- **Simbolo** (symbol): `X` or `O`.
- **Jogada** (move): a player marking a position with their symbol.
- **StatusPartida** (match status): `EM_ANDAMENTO`, `VENCIDA` or `EMPATADA`.
- **Vencedor** (winner): the symbol that completed a row, column or diagonal.

The same words are used in the code and in the docs, so there is no need to translate between what the game says and what the code says.

## Value objects

These have no identity of their own. Only the value matters.

- **Posicao**: (0, 0) is equal to any other (0, 0). It validates itself: creating `Posicao(3, 0)` raises `PosicaoInvalida`. That way a position outside the board never exists in the program. It is a frozen dataclass, so it cannot change after creation.
- **Simbolo** and **StatusPartida**: enums, because only those values are possible. `Simbolo` has an `outro()` method that returns the opponent's symbol, used to pass the turn.

## Main entity: Partida

`Partida` is the main entity. It has state that changes over time (whose turn it is, the status, the winner) and it owns the `Tabuleiro`. That also makes it the aggregate root: to play, you go through `Partida` instead of changing the board directly.

The rules live inside it:

- a move is only allowed while the match is in progress (otherwise `PartidaEncerrada`);
- a move on an occupied cell is rejected (`PosicaoOcupada`, raised by `Tabuleiro`);
- after each move it checks for a win or a draw;
- if the game goes on, it passes the turn to the other player.

If a move is invalid, the exception is raised before anything changes, so the turn is not switched by mistake.

`Tabuleiro` is also in the domain. It knows how to mark a cell, whether it is full, and how to find a winner by checking the 8 winning lines (3 rows, 3 columns and 2 diagonals). I kept those lines in a constant because it is easier to read than many `if` statements.

The rules are here because, if they were in `cli.py`, any other interface (a GUI, for example) would have to copy all of them.

## Domain exceptions

These are errors that make sense in the game, each with a clear message:

- `PosicaoInvalida`: row or column outside the board.
- `PosicaoOcupada`: the cell already has a symbol.
- `PartidaEncerrada`: someone tried to play after the end.
- `PartidaNaoEncontrada`: the use case did not find a match in the repository.

All of them inherit from `ErroDeDominio`, so the terminal catches a single type and shows the message as it is.

## Repository

`PartidaRepository` is only an interface (abstract class) with two methods, `salvar` and `buscar`. It lives in the domain because the domain defines what it needs: store and retrieve the match. Where it is actually stored is the infrastructure's concern. The game has one match at a time, so `buscar` takes no id.

## What I left out

I did not use domain events, factories or domain services. For a game this size they would only make the code harder to follow without adding anything.
