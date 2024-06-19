from .database import Database

class BestRestaurant:
    def __init__(self, db):
        self.db = db

    def add(self, location_id, restaurant_type, reservation_count):
        self.db.execute(
            "INSERT INTO best_restaurants (location_id, restaurant_type, reservation_count) VALUES (?, ?, ?)",
            (location_id, restaurant_type, reservation_count)
        )

    def show_all(self):
        return self.db.fetchall("SELECT * FROM best_restaurants")
