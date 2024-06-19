from .database import Database

class User:
    def __init__(self, db):
        self.db = db

    def add(self, username, password):
        self.db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

    def show_all(self):
        return self.db.fetchall("SELECT * FROM users")
