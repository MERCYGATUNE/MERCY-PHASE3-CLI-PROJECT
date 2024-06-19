from .database import Database

class Location:
    def __init__(self, db):
        self.db = db

    def add(self, name):
        self.db.execute("INSERT INTO locations (name) VALUES (?)", (name,))

    def show_all(self):
        return self.db.fetchall("SELECT * FROM locations")
