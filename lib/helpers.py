import sqlite3

DATABASE = 'restaurant.db'

def add_reservation(name, party_size, reservation_time, phone_number, table_number, email, restaurant_id, location_id, user_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reservations (name, party_size, reservation_time, phone_number, table_number, email, restaurant_id, location_id, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (name, party_size, reservation_time, phone_number, table_number, email, restaurant_id, location_id, user_id)
        )
        conn.commit()

def show_reservations():
    reservations = get_all_reservations()
    for reservation in reservations:
        print(reservation)

def find_reservation():
    reservation_id = int(input("Enter reservation ID: "))
    reservation = get_reservation_by_id(reservation_id)
    if reservation:
        print(reservation)
    else:
        print(f"Reservation with ID {reservation_id} not found.")

def delete_reservation_cmd():
    reservation_id = int(input("Enter reservation ID to delete: "))
    delete_reservation(reservation_id)
    print(f"Reservation with ID {reservation_id} deleted successfully.")

def add_feedback():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    message = input("Enter your feedback message: ")
    submission_time = input("Enter submission time (YYYY-MM-DD HH:MM): ")

    add_feedback(name, email, message, submission_time)
    print("Feedback added successfully.")

def get_all_reservations():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservations")
        return cursor.fetchall()

def find_reservation(reservation_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservations WHERE id=?", (reservation_id,))
        return cursor.fetchone()

def get_reservation_by_id(reservation_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservations WHERE id=?", (reservation_id,))
        return cursor.fetchone()


def delete_reservation_cmd():
    reservation_id = int(input("Enter reservation ID to delete: "))
    delete_reservation(reservation_id)
    print(f"Reservation with ID {reservation_id} deleted successfully.")


def add_feedback(name, email, message, submission_time):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO feedback (name, email, message, submission_time) VALUES (?, ?, ?, ?)",
            (name, email, message, submission_time)
        )
        conn.commit()

def show_feedback():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM feedback")
        return cursor.fetchall()

def add_restaurant(restaurant_type, location):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO restaurants (restaurant_type, location) VALUES (?, ?)",
            (restaurant_type, location)
        )
        conn.commit()

def show_restaurants():
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM restaurants")
            restaurants = cursor.fetchall()
            for restaurant in restaurants:
                print(restaurant)
            return restaurants
    except sqlite3.Error as e:
        print(f"Error retrieving restaurants: {e}")
        return None

def add_location(name):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO locations (name) VALUES (?)", (name,))
            conn.commit()
            print(f"Location '{name}' added successfully.")
    except sqlite3.Error as e:
        print(f"Error adding location: {e}")
        raise

def show_locations():
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM locations")
            locations = cursor.fetchall()
        return locations
    except sqlite3.Error as e:
        print(f"Failed to retrieve locations: {e}")
        return None

def add_user(username, password):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()

def show_users():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()

def add_available_slot(location_id, reservation_time):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO available_slots (location_id, reservation_time) VALUES (?, ?)",
            (location_id, reservation_time)
        )
        conn.commit()

def show_available_slots():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM available_slots")
        return cursor.fetchall()

def add_best_restaurant(location_id, restaurant_type, reservation_count):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO best_restaurants (location_id, restaurant_type, reservation_count) VALUES (?, ?, ?)",
            (location_id, restaurant_type, reservation_count)
        )
        conn.commit()

def show_best_restaurants():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM best_restaurants")
        return cursor.fetchall()

def exit_program():
    print("Thank you for using Rave...Goodbye!")
    exit()
