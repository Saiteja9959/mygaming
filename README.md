# MY GAME ZONE — `mygaming`

A responsive Flask-powered mini-game arcade with a neon interface, three playable games, player profiles, and a SQLite leaderboard.

## Features
- **Memory Flip:** match eight pairs and earn a move-based score.
- **Reaction Rush:** five-round reaction-time challenge.
- **Tic Tac Toe:** play against the computer.
- **Player profile:** choose a display name stored in a Flask session.
- **Leaderboard:** scores saved to SQLite and filterable by game.
- Responsive interface, `/health` endpoint, Dockerfile, Compose setup, and starter tests.

## Run locally
Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000. SQLite data is created automatically at `data/games.db`. Set a unique `SECRET_KEY` for deployment.

## Run with Docker
```bash
docker compose up --build -d
```
Open http://localhost:5000. Scores persist in the named `game-data` volume.

## API
- `GET /health` — health status
- `POST /api/player` — JSON `{"name":"PLAYER ONE"}`
- `GET /api/leaderboard?game=all` — top scores; filters: `memory`, `reaction`, `tictactoe`
- `POST /api/scores` — JSON `{"game":"memory","score":1200}`

Scores are validated for supported game names and numeric bounds. For a public competitive deployment, replace client-reported scores with server-verifiable events and add CSRF protection, rate limiting, and proper identity management.

## Project structure
```text
app.py
requirements.txt
Dockerfile
compose.yml
templates/index.html
static/css/style.css
static/js/app.js
tests/test_app.py
```

Architecture inspiration: https://github.com/devops0014/python-code-library-app/tree/master. This is a new gaming implementation, not a copy of that app's domain-specific source.