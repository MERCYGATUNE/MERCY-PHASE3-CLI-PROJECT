from .database import Database

class AvailableSlot:
    def __init__(self, db):
        self.db = db

    def add(self, location_id, reservation_time):
        self.db.execute(
            "INSERT INTO available_slots (location_id, reservation_time) VALUES (?, ?)",
            (location_id, reservation_time)
        )

    def show_all(self):
        return self.db.fetchall("SELECT * FROM available_slots")
