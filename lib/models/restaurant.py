from .database import Database

class Restaurant:
    def __init__(self, db):
        self.db = db

    def add(self, restaurant_type, location):
        self.db.execute(
            "INSERT INTO restaurants (restaurant_type, location) VALUES (?, ?)",
            (restaurant_type, location)
        )

    def show_all(self):
        return self.db.fetchall("SELECT * FROM restaurants")
