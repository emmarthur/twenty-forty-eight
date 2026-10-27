"""
FastAPI app — Twenty Forty-Eight (2048).

Run: uvicorn main:app --reload --port 3025
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

_DEMO_ROOT = Path(__file__).resolve().parent.parent
if str(_DEMO_ROOT) not in sys.path:
    sys.path.insert(0, str(_DEMO_ROOT))

from game2048_core import apply_turn, new_board, state_for_client  # noqa: E402

app = FastAPI(title="Twenty Forty-Eight")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")


class CellsModel(BaseModel):
    cells: list[list[int | None]] = Field(..., min_length=4, max_length=4)


class MoveRequest(BaseModel):
    cells: list[list[int | None]]
    move: Literal["W", "A", "S", "D"]
    already_won: bool = False


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html")


@app.get("/help", response_class=HTMLResponse)
async def help_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "help.html")


@app.post("/api/new")
async def api_new() -> JSONResponse:
    return JSONResponse(state_for_client(new_board()))


@app.post("/api/move")
async def api_move(body: MoveRequest) -> JSONResponse:
    if len(body.cells) != 4 or any(len(row) != 4 for row in body.cells):
        raise HTTPException(status_code=400, detail="Invalid board size.")
    try:
        return JSONResponse(
            apply_turn(body.cells, body.move, already_won=body.already_won),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
