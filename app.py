from flask import Flask, render_template, request, jsonify, session
from pathlib import Path
import sqlite3, os, secrets, time

BASE = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("GAME_DB", BASE / "data" / "games.db"))
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def connect():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with connect() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT NOT NULL,
            game TEXT NOT NULL,
            score INTEGER NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")
        db.execute("CREATE INDEX IF NOT EXISTS idx_scores_game_score ON scores(game, score DESC)")

@app.get("/")
def index():
    player = session.get("player", "PLAYER ONE")
    return render_template("index.html", player=player)

@app.post("/api/player")
def set_player():
    name = (request.json or {}).get("name", "").strip()[:18]
    if not name:
        return jsonify(error="Enter a player name."), 400
    session["player"] = name.upper()
    return jsonify(player=session["player"])

@app.get("/api/leaderboard")
def leaderboard():
    game = request.args.get("game", "all")
    with connect() as db:
        if game == "all":
            rows = db.execute("""SELECT player, game, score, created_at FROM scores
                ORDER BY score DESC, id ASC LIMIT 10""").fetchall()
        else:
            rows = db.execute("""SELECT player, game, score, created_at FROM scores
                WHERE game=? ORDER BY score DESC, id ASC LIMIT 10""", (game,)).fetchall()
    return jsonify([dict(r) for r in rows])

@app.post("/api/scores")
def save_score():
    data = request.get_json(silent=True) or {}
    game = data.get("game")
    score = data.get("score")
    allowed = {"memory", "reaction", "tictactoe"}
    if game not in allowed or not isinstance(score, int) or isinstance(score, bool):
        return jsonify(error="Invalid score payload."), 400
    score = max(0, min(score, 1_000_000))
    player = session.get("player", "PLAYER ONE")
    with connect() as db:
        db.execute("INSERT INTO scores(player, game, score) VALUES(?,?,?)", (player, game, score))
    return jsonify(ok=True, player=player, game=game, score=score)

@app.get("/health")
def health():
    return jsonify(status="ok", app="mygamingapplication")

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
