from .database import Database

class Feedback:
    def __init__(self, db):
        self.db = db

    def add(self, name, email, message, submission_time):
        self.db.execute(
            "INSERT INTO feedback (name, email, message, submission_time) VALUES (?, ?, ?, ?)",
            (name, email, message, submission_time)
        )

    def show_all(self):
        return self.db.fetchall("SELECT * FROM feedback")
