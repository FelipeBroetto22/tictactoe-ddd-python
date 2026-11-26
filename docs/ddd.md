# DDD in Tic-Tac-Toe

This document explains how I applied Domain-Driven Design to the game. The idea that helped me most is that the code should speak the same language as the problem. Anyone reading `match.make_move(position)` understands what happens without knowing how it is implemented.

## Ubiquitous language

- **Match**: one game, from start to finish.
- **Board**: the 3x3 grid.
- **Position**: a cell of the board, with row and column from 0 to 2.
- **Symbol**: `X` or `O`.
- **Move**: a player marking a position with their symbol.
- **MatchStatus**: `IN_PROGRESS`, `WON` or `DRAW`.
- **Winner**: the symbol that completed a row, column or diagonal.

The same words are used in the code and in the docs, so there is no need to translate between what the game says and what the code says.

## Value objects

These have no identity of their own. Only the value matters.

- **Position**: (0, 0) is equal to any other (0, 0). It validates itself: creating `Position(3, 0)` raises `InvalidPosition`. That way a position outside the board never exists in the program. It is a frozen dataclass, so it cannot change after creation.
- **Symbol** and **MatchStatus**: enums, because only those values are possible. `Symbol` has an `opponent()` method that returns the other symbol, used to pass the turn.

## Main entity: Match

`Match` is the main entity. It has state that changes over time (whose turn it is, the status, the winner) and it owns the `Board`. That also makes it the aggregate root: to play, you go through `Match` instead of changing the board directly.

The rules live inside it:

- a move is only allowed while the match is in progress (otherwise `MatchFinished`);
- a move on an occupied cell is rejected (`PositionOccupied`, raised by `Board`);
- after each move it checks for a win or a draw;
- if the game goes on, it passes the turn to the other player.

If a move is invalid, the exception is raised before anything changes, so the turn is not switched by mistake.

`Board` is also in the domain. It knows how to mark a cell, whether it is full, and how to find a winner by checking the 8 winning lines (3 rows, 3 columns and 2 diagonals). I kept those lines in a constant because it is easier to read than many `if` statements.

The rules are here because, if they were in `cli.py`, any other interface (a GUI, for example) would have to copy all of them.

## Domain exceptions

These are errors that make sense in the game, each with a clear message:

- `InvalidPosition`: row or column outside the board.
- `PositionOccupied`: the cell already has a symbol.
- `MatchFinished`: someone tried to play after the end.
- `MatchNotFound`: the use case did not find a match in the repository.

All of them inherit from `DomainError`, so the terminal catches a single type and shows the message as it is.

## Repository

`MatchRepository` is only an interface (abstract class) with two methods, `save` and `find`. It lives in the domain because the domain defines what it needs: store and retrieve the match. Where it is actually stored is the infrastructure's concern. The game has one match at a time, so `find` takes no id.

## What I left out

I did not use domain events, factories or domain services. For a game this size they would only make the code harder to follow without adding anything.
