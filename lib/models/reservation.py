from .database import Database

class Reservation:
    def __init__(self, db):
        self.db = db

    def add(self, name, party_size, reservation_time, phone_number, table_number, email, restaurant_id, location_id, user_id):
        self.db.execute(
            "INSERT INTO reservations (name, party_size, reservation_time, phone_number, table_number, email, restaurant_id, location_id, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (name, party_size, reservation_time, phone_number, table_number, email, restaurant_id, location_id, user_id)
        )

    def show_all(self):
        return self.db.fetchall("SELECT * FROM reservations")

    def find(self, reservation_id):
        return self.db.fetchone("SELECT * FROM reservations WHERE id=?", (reservation_id,))

    def delete(self, reservation_id):
        self.db.execute("DELETE FROM reservations WHERE id=?", (reservation_id,))
