"""
Twenty Forty-Eight (2048) — board logic from the book's dictionary grid.

Coordinates: x 0–3 left→right, y 0–3 top→bottom. BLANK is an empty cell.
"""

from __future__ import annotations

import copy
import random
from typing import Any

BLANK = ""
SIZE = 4
WIN_TILE = 2048

Move = str  # W, A, S, D


def new_board() -> dict[tuple[int, int], int | str]:
    board: dict[tuple[int, int], int | str] = {}
    for x in range(SIZE):
        for y in range(SIZE):
            board[(x, y)] = BLANK
    placed = 0
    while placed < 2:
        space = (random.randint(0, 3), random.randint(0, 3))
        if board[space] == BLANK:
            board[space] = 2
            placed += 1
    return board


def get_score(board: dict[tuple[int, int], int | str]) -> int:
    score = 0
    for x in range(SIZE):
        for y in range(SIZE):
            tile = board[(x, y)]
            if tile != BLANK:
                score += int(tile)
    return score


def combine_tiles_in_column(column: list[int | str]) -> list[int | str]:
    combined: list[int | str] = [tile for tile in column if tile != BLANK]
    while len(combined) < 4:
        combined.append(BLANK)
    for i in range(3):
        if combined[i] == combined[i + 1] and combined[i] != BLANK:
            combined[i] = int(combined[i]) * 2
            for above in range(i + 1, 3):
                combined[above] = combined[above + 1]
            combined[3] = BLANK
    return combined


def _column_spaces(move: Move) -> list[list[tuple[int, int]]]:
    if move == "W":
        return [
            [(0, 0), (0, 1), (0, 2), (0, 3)],
            [(1, 0), (1, 1), (1, 2), (1, 3)],
            [(2, 0), (2, 1), (2, 2), (2, 3)],
            [(3, 0), (3, 1), (3, 2), (3, 3)],
        ]
    if move == "A":
        return [
            [(0, 0), (1, 0), (2, 0), (3, 0)],
            [(0, 1), (1, 1), (2, 1), (3, 1)],
            [(0, 2), (1, 2), (2, 2), (3, 2)],
            [(0, 3), (1, 3), (2, 3), (3, 3)],
        ]
    if move == "S":
        return [
            [(0, 3), (0, 2), (0, 1), (0, 0)],
            [(1, 3), (1, 2), (1, 1), (1, 0)],
            [(2, 3), (2, 2), (2, 1), (2, 0)],
            [(3, 3), (3, 2), (3, 1), (3, 0)],
        ]
    if move == "D":
        return [
            [(3, 0), (2, 0), (1, 0), (0, 0)],
            [(3, 1), (2, 1), (1, 1), (0, 1)],
            [(3, 2), (2, 2), (1, 2), (0, 2)],
            [(3, 3), (2, 3), (1, 3), (0, 3)],
        ]
    raise ValueError('Move must be "W", "A", "S", or "D".')


def make_move(board: dict[tuple[int, int], int | str], move: Move) -> dict[tuple[int, int], int | str]:
    all_columns = _column_spaces(move)
    board_after: dict[tuple[int, int], int | str] = {}
    for column_spaces in all_columns:
        column = [board[space] for space in column_spaces]
        combined = combine_tiles_in_column(column)
        for space, tile in zip(column_spaces, combined):
            board_after[space] = tile
    return board_after


def boards_equal(
    a: dict[tuple[int, int], int | str],
    b: dict[tuple[int, int], int | str],
) -> bool:
    for x in range(SIZE):
        for y in range(SIZE):
            if a[(x, y)] != b[(x, y)]:
                return False
    return True


def add_two_to_board(board: dict[tuple[int, int], int | str]) -> None:
    while True:
        space = (random.randint(0, 3), random.randint(0, 3))
        if board[space] == BLANK:
            board[space] = 2
            return


def is_full(board: dict[tuple[int, int], int | str]) -> bool:
    for x in range(SIZE):
        for y in range(SIZE):
            if board[(x, y)] == BLANK:
                return False
    return True


def has_win_tile(board: dict[tuple[int, int], int | str]) -> bool:
    for x in range(SIZE):
        for y in range(SIZE):
            if board[(x, y)] == WIN_TILE:
                return True
    return False


def can_move(board: dict[tuple[int, int], int | str]) -> bool:
    for direction in ("W", "A", "S", "D"):
        if not boards_equal(board, make_move(copy.deepcopy(board), direction)):
            return True
    return False


def board_to_cells(board: dict[tuple[int, int], int | str]) -> list[list[int | None]]:
    """Rows top→bottom, each row left→right."""
    rows: list[list[int | None]] = []
    for y in range(SIZE):
        row: list[int | None] = []
        for x in range(SIZE):
            tile = board[(x, y)]
            row.append(int(tile) if tile != BLANK else None)
        rows.append(row)
    return rows


def cells_to_board(cells: list[list[int | None]]) -> dict[tuple[int, int], int | str]:
    board: dict[tuple[int, int], int | str] = {}
    for y in range(SIZE):
        for x in range(SIZE):
            value = cells[y][x]
            board[(x, y)] = BLANK if value is None else int(value)
    return board


def state_for_client(board: dict[tuple[int, int], int | str], *, won: bool = False) -> dict[str, Any]:
    game_over = is_full(board) and not can_move(board)
    return {
        "cells": board_to_cells(board),
        "score": get_score(board),
        "won": won or has_win_tile(board),
        "game_over": game_over,
    }


def apply_turn(
    cells: list[list[int | None]],
    move: Move,
    *,
    already_won: bool = False,
) -> dict[str, Any]:
    board = cells_to_board(cells)
    moved = make_move(board, move)
    if boards_equal(board, moved):
        return {
            **state_for_client(board, won=already_won),
            "changed": False,
        }
    board = moved
    add_two_to_board(board)
    won = already_won or has_win_tile(board)
    return {
        **state_for_client(board, won=won),
        "changed": True,
    }
