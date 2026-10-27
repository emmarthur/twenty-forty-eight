# Twenty Forty-Eight (catalog #521)

Al Sweigart — *The Big Book of Small Python Projects*, Project #79 (2048-style puzzle).

| Artifact | Path |
|----------|------|
| Book steps | [`BOOK_DIRECTIONS.md`](./BOOK_DIRECTIONS.md) |
| Upstream script | [`reference/twentyfortyeight.py`](./reference/twentyfortyeight.py) |
| CLI | [`reference/run_cli.py`](./reference/run_cli.py) |
| Shared logic | [`game2048_core.py`](./game2048_core.py) |
| Web (FastAPI) | [`web/`](./web/) — port **3025** |

## Run the web demo

```powershell
Set-Location "c:\Users\emmak\Desktop\Content\CodingProjects\PortProjects\demos\twenty-forty-eight\web"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 3025
```

Open [http://127.0.0.1:3025/](http://127.0.0.1:3025/).

## Run the CLI

```powershell
Set-Location "c:\Users\emmak\Desktop\Content\CodingProjects\PortProjects\demos\twenty-forty-eight"
python reference\run_cli.py
```

Portfolio: [`PORTFOLIO_INTEGRATION.md`](./PORTFOLIO_INTEGRATION.md).
