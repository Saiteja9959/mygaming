import os
import tempfile
import unittest
from pathlib import Path
import app as app_module
from app import app, init_db

class ArcadeApiTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        app_module.DB_PATH = Path(self.tmp.name) / "test.db"
        app_module.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        init_db()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def tearDown(self):
        self.tmp.cleanup()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"MY GAME ZONE", response.data)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")

    def test_player_name_required(self):
        response = self.client.post("/api/player", json={"name": "  "})
        self.assertEqual(response.status_code, 400)

    def test_player_name_saved_to_session(self):
        response = self.client.post("/api/player", json={"name": "ArcadeAce"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["player"], "ARCADEACE")

    def test_invalid_game_score_rejected(self):
        response = self.client.post("/api/scores", json={"game": "not-a-game", "score": 50})
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
