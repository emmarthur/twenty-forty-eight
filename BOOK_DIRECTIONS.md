# Book directions — Twenty Forty-Eight

**Catalog #521** · Al Sweigart, *The Big Book of Small Python Projects*, **Project #79** — Twenty Forty-Eight

- Invent with Python: [project79.html](https://inventwithpython.com/bigbookpython/project79.html)
- Upstream: [twentyfortyeight.py](https://github.com/asweigart/the-big-book-of-small-python-projects/blob/main/twentyfortyeight.py)
- Local reference: [`reference/twentyfortyeight.py`](./reference/twentyfortyeight.py)
- Shared logic: [`game2048_core.py`](./game2048_core.py)

## What the book asks you to build

A 4×4 **dictionary board** `(x, y) → tile value or blank`:

1. Slide tiles **W/A/S/D** using column compression + merge (double equal neighbors).
2. Spawn a new **2** after each move; score = sum of all tiles.
3. Lose when the board is full (book exits; web also checks for no legal merges).

## Web version (`web/` — FastAPI, port **3025**)

| Book step | Web equivalent |
|-----------|----------------|
| `getNewBoard` / `makeMove` / `addTwoToBoard` | `game2048_core` |
| WASD input | Arrow keys + WASD in browser |
| Score | HUD + API `score` field |
| Win at 2048 | `won` flag (play can continue) |

CLI: [`reference/run_cli.py`](./reference/run_cli.py)
