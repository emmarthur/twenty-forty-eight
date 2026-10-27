const gridEl = document.getElementById("grid");
const scoreEl = document.getElementById("score");
const bannerEl = document.getElementById("banner");
const errorEl = document.getElementById("error-text");
const newBtn = document.getElementById("btn-new");

let state = { cells: null, score: 0, won: false, game_over: false };

const KEY_TO_MOVE = {
  ArrowUp: "W",
  ArrowLeft: "A",
  ArrowDown: "S",
  ArrowRight: "D",
  w: "W",
  a: "A",
  s: "S",
  d: "D",
  W: "W",
  A: "A",
  S: "S",
  D: "D",
};

const TILE_COLORS = {
  2: "#eee4da",
  4: "#ede0c8",
  8: "#f2b179",
  16: "#f59563",
  32: "#f67c5f",
  64: "#f65e3b",
  128: "#edcf72",
  256: "#edcc61",
  512: "#edc850",
  1024: "#edc53f",
  2048: "#edc22e",
};

function setError(message) {
  errorEl.hidden = !message;
  errorEl.textContent = message || "";
}

function render() {
  if (!state.cells) return;
  scoreEl.textContent = String(state.score);
  gridEl.innerHTML = "";
  state.cells.forEach((row) => {
    row.forEach((value) => {
      const cell = document.createElement("div");
      cell.className = "cell" + (value ? " has-tile" : "");
      if (value) {
        cell.textContent = String(value);
        cell.style.background = TILE_COLORS[value] || "#3c3a32";
        cell.style.color = value > 4 ? "#f9f6f2" : "#776e65";
        if (value >= 1000) cell.classList.add("is-small");
      }
      gridEl.appendChild(cell);
    });
  });

  if (state.game_over) {
    bannerEl.hidden = false;
    bannerEl.textContent = "Game over — no moves left.";
    bannerEl.className = "banner is-over";
  } else if (state.won) {
    bannerEl.hidden = false;
    bannerEl.textContent = "You reached 2048! Keep going or start a new game.";
    bannerEl.className = "banner is-win";
  } else {
    bannerEl.hidden = true;
  }
}

async function newGame() {
  setError(null);
  const res = await fetch("/api/new", { method: "POST" });
  const data = await res.json();
  if (!res.ok) {
    setError(data.detail || "Could not start game.");
    return;
  }
  state = { ...data, already_won: false };
  render();
}

async function sendMove(move) {
  if (!state.cells || state.game_over) return;
  setError(null);
  const res = await fetch("/api/move", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      cells: state.cells,
      move,
      already_won: state.won,
    }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    setError(data.detail || "Invalid move.");
    return;
  }
  if (data.changed) {
    state = data;
    render();
  }
}

document.addEventListener("keydown", (event) => {
  const move = KEY_TO_MOVE[event.key];
  if (!move) return;
  event.preventDefault();
  sendMove(move);
});

newBtn.addEventListener("click", () => newGame());
newGame();
