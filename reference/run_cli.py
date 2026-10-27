"""Terminal 2048 — uses shared game2048_core logic."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from game2048_core import (  # noqa: E402
    add_two_to_board,
    board_to_cells,
    boards_equal,
    can_move,
    is_full,
    make_move,
    new_board,
    state_for_client,
)

print(
    """Twenty Forty-Eight

Slide tiles with W A S D. Combine matching numbers. Reach 2048 if you can.
"""
)
input("Press Enter to begin...")
board = new_board()

while True:
    st = state_for_client(board)
    for row in st["cells"]:
        print(" ".join(f"{v or '.':>5}" for v in row))
    print("Score:", st["score"])
    move = input("Move (WASD, Q to quit): ").strip().upper()
    if move == "Q":
        print("Thanks for playing!")
        break
    if move not in ("W", "A", "S", "D"):
        continue
    next_board = make_move(board, move)
    if boards_equal(board, next_board):
        continue
    board = next_board
    add_two_to_board(board)
    if is_full(board) and not can_move(board):
        for row in board_to_cells(board):
            print(" ".join(f"{v or '.':>5}" for v in row))
        print("Game over — thanks for playing!")
        break
