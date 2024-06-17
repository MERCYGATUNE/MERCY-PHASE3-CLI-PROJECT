import os
import sys
import sqlite3
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

# Function to create tables in the database
def create_tables(cursor):
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY,
                restaurant_type TEXT,
                location TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                restaurant_id INTEGER,
                location_id INTEGER,
                name TEXT,
                phone_number TEXT,
                email TEXT,
                party_size INTEGER,
                reservation_time DATETIME,
                table_number INTEGER,
                status TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(restaurant_id) REFERENCES restaurants(id),
                FOREIGN KEY(location_id) REFERENCES locations(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                message TEXT,
                submission_time DATETIME,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS available_slots (
                id INTEGER PRIMARY KEY,
                location_id INTEGER,
                reservation_time DATETIME
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS best_restaurants (
                id INTEGER PRIMARY KEY,
                location_id INTEGER,
                restaurant_type TEXT,
                reservation_count INTEGER,
                FOREIGN KEY(location_id) REFERENCES locations(id)
            )
        ''')
    except sqlite3.Error as e:
        print("Error creating tables:", e)

# Function to register a new user
def register_user(cursor, username, password):
    try:
        cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (?, ?)
        ''', (username, password))
        return True
    except sqlite3.Error as e:
        print("Error registering user:", e)
        return False

# Function to authenticate user login
def authenticate_user(cursor, username, password):
    try:
        cursor.execute('''
            SELECT * FROM users
            WHERE username = ? AND password = ?
        ''', (username, password))
        user = cursor.fetchone()
        if user:
            return user[0]
        else:
            return None
    except sqlite3.Error as e:
        print("Error authenticating user:", e)
        return None

# Function to make a reservation
def make_reservation(cursor, user_id, restaurant_id, location_id, name, phone_number, email, party_size, reservation_time):
    try:
        cursor.execute('''
            INSERT INTO reservations (user_id, restaurant_id, location_id, name, phone_number, email, party_size, reservation_time, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, restaurant_id, location_id, name, phone_number, email, party_size, reservation_time, "Pending"))

        # Add available slot to available_slots table
        add_available_slot(cursor, location_id, reservation_time)

        # Send reservation confirmation email
        send_confirmation_email(email, name, reservation_time)

        return True
    except sqlite3.Error as e:
        print("Error making reservation:", e)
        return False

# Function to confirm a reservation
def confirm_reservation(cursor, reservation_id):
    try:
        cursor.execute('''
            UPDATE reservations
            SET status = "Confirmed"
            WHERE id = ?
        ''', (reservation_id,))
        return True
    except sqlite3.Error as e:
        print("Error confirming reservation:", e)
        return False

# Function to cancel a reservation
def cancel_reservation(cursor, reservation_id):
    try:
        cursor.execute('''
            UPDATE reservations
            SET status = "Cancelled"
            WHERE id = ?
        ''', (reservation_id,))
        return True
    except sqlite3.Error as e:
        print("Error cancelling reservation:", e)
        return False

# Function to add available slot
def add_available_slot(cursor, location_id, reservation_time):
    try:
        cursor.execute('''
            INSERT INTO available_slots (location_id, reservation_time)
            VALUES (?, ?)
        ''', (location_id, reservation_time))
        return True
    except sqlite3.Error as e:
        print("Error adding available slot:", e)
        return False

# Function to send reservation confirmation email
def send_confirmation_email(email, name, reservation_time):
    try:
        # Setup email server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Add your email credentials here
        server.login('your_email@gmail.com', 'your_password')
        
        # Construct message
        msg = MIMEText(f"Hello {name}, Your reservation is confirmed for {reservation_time}.")
        msg['From'] = 'your_email@gmail.com'
        msg['To'] = email
        msg['Subject'] = 'Reservation Confirmation'
        
        # Send message
        server.sendmail('your_email@gmail.com', email, msg.as_string())
        server.quit()
        
        print("Reservation confirmation email sent successfully!")
    except Exception as e:
        print("Error sending confirmation email:", e)

# Function to view available reservation slots
def view_available_slots(cursor):
    try:
        date = input("Enter the date for reservation (YYYY-MM-DD): ")
        time = input("Enter the time for reservation (HH:MM): ")
        datetime_str = date + " " + time
        reservation_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

        # Check for available slots within a time window (e.g., 1 hour)
        start_time = reservation_time
        end_time = reservation_time + timedelta(hours=1)

        cursor.execute('''
            SELECT * FROM available_slots
            WHERE reservation_time >= ? AND reservation_time < ?
        ''', (start_time, end_time))

        available_slots = cursor.fetchall()
        if available_slots:
            print("The following slots are not available:")
            for slot in available_slots:
                print(f"Slot ID: {slot[0]}, Time: {slot[2]}")
        else:
            print("All slots within the selected time are available.")
    except ValueError:
        print("Invalid date or time format. Please enter in YYYY-MM-DD HH:MM format.")

# Function to view feedback
def view_feedback(cursor):
    try:
        cursor.execute('''
            SELECT * FROM feedback
        ''')
        feedback = cursor.fetchall()
        if feedback:
            for fb in feedback:
                print(f"Feedback ID: {fb[0]}, User ID: {fb[1]}, Message: {fb[2]}, Submission Time: {fb[3]}")
        else:
            print("No feedback found.")
    except sqlite3.Error as e:
        print("Error fetching feedback:", e)

# Function to add new restaurant
def add_new_restaurant(cursor, restaurant_type, location):
    try:
        cursor.execute('''
            INSERT INTO restaurants (restaurant_type, location)
            VALUES (?, ?)
        ''', (restaurant_type, location))
        return True
    except sqlite3.Error as e:
        print("Error adding new restaurant:", e)
        return False

# Function to add new location
def add_new_location(cursor, location_name):
    try:
        cursor.execute('''
            INSERT INTO locations (name)
            VALUES (?)
        ''', (location_name,))
        return True
    except sqlite3.Error as e:
        print("Error adding new location:", e)
        return False

# Function to view best restaurants
def view_best_restaurants(cursor):
    try:
        cursor.execute('''
            SELECT * FROM best_restaurants
        ''')
        best_restaurants = cursor.fetchall()
        if best_restaurants:
            for res in best_restaurants:
                print(f"ID: {res[0]}, Location ID: {res[1]}, Restaurant Type: {res[2]}, Reservation Count: {res[3]}")
        else:
            print("No best restaurants found.")
    except sqlite3.Error as e:
        print("Error fetching best restaurants:", e)

# Function to find best restaurants in a location
def find_best_restaurants(cursor, location_name):
    try:
        cursor.execute('''
            SELECT r.restaurant_type, COUNT(r.id) AS reservation_count
            FROM restaurants AS r
            LEFT JOIN reservations AS res ON r.id = res.restaurant_id
            WHERE res.location_id = ?
            GROUP BY r.id
            ORDER BY reservation_count DESC
            LIMIT 5
        ''', (location_id,))

        best_restaurants = cursor.fetchall()
        if best_restaurants:
            print("Top 5 restaurants in this location:")
            for idx, restaurant in enumerate(best_restaurants, start=1):
                print(f"{idx}. {restaurant[0]}")
                # Add best restaurants to best_restaurants table
                add_best_restaurant(cursor, location_id, restaurant[0], restaurant[1])
        else:
            print("No restaurants found in this location.")
    except sqlite3.Error as e:
        print("Error finding best restaurants:", e)

# Function to add best restaurant
def add_best_restaurant(cursor, location_id, restaurant_type, reservation_count):
    try:
        cursor.execute('''
            INSERT INTO best_restaurants (location_id, restaurant_type, reservation_count)
            VALUES (?, ?, ?)
        ''', (location_id, restaurant_type, reservation_count))
        return True
    except sqlite3.Error as e:
        print("Error adding best restaurant:", e)
        return False

# Function to display reservations
def show_reservations(cursor):
    try:
        cursor.execute('''
            SELECT * FROM reservations
        ''')
        reservations = cursor.fetchall()
        if reservations:
            for res in reservations:
                print(f"Reservation ID: {res[0]}, User ID: {res[1]}, Restaurant ID: {res[2]}, Location ID: {res[3]}, Name: {res[4]}, Phone: {res[5]}, Email: {res[6]}, Party Size: {res[7]}, Time: {res[8]}, Status: {res[10]}")
        else:
            print("No reservations found.")
    except sqlite3.Error as e:
        print("Error fetching reservations:", e)

# Function to get the restaurant ID based on restaurant type and location
def get_restaurant_id(cursor, restaurant_type, location):
    try:
        cursor.execute('''
            SELECT id FROM restaurants
            WHERE restaurant_type = ? AND location = ?
        ''', (restaurant_type, location))
        restaurant = cursor.fetchone()
        if restaurant:
            return restaurant[0]
        else:
            print("Restaurant not found.")
            return None
    except sqlite3.Error as e:
        print("Error getting restaurant ID:", e)
        return None

# Placeholder data for testing
if __name__ == "__main__":
    print("Welcome to Rave! The Restaurant Reservation System!")
    
    database_file = 'restaurant.db'

    try:
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        create_tables(cursor)

        while True:
            print("\nRave Restaurant Reservation System")
            print("1. Register")
            print("2. Login")
            print("3. Make a reservation")
            print("4. Adjust a reservation")
            print("5. View reservations")
            print("6. Provide Feedback")
            print("7. Delete a reservation")
            print("8. View available reservation slots")
            print("9. View feedback")
            print("10. Add a new restaurant")
            print("11. Add a new location")
            print("12. View best restaurants")
            print("13. Find the best restaurants in this location")
            print("14. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                if register_user(cursor, username, password):
                    conn.commit()
                    print("User registered successfully!")

            elif choice == '2':
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                user_id = authenticate_user(cursor, username, password)
                if user_id:
                    print("User authenticated successfully!")
                else:
                    print("Invalid username or password.")

            elif choice == '3':
                # Check if user is logged in
                if user_id:
                    restaurant_type = input("Enter the type of restaurant: ")
                    location = input("Enter the location: ")
                    name = input("Enter your name: ")
                    phone_number = input("Enter your phone number: ")
                    email = input("Enter your email: ")
                    party_size = int(input("Enter party size: "))
                    reservation_time_str = input("Enter reservation time (YYYY-MM-DD HH:MM:SS): ")
                    reservation_time = datetime.strptime(reservation_time_str, "%Y-%m-%d %H:%M:%S")

                    # Get restaurant and location IDs or add new if not exists
                    restaurant_id = get_restaurant_id(cursor, restaurant_type, location)
                    location_id = get_location_id(cursor, location)

                    # Make reservation
                    if make_reservation(cursor, user_id, restaurant_id, location_id, name, phone_number, email, party_size, reservation_time):
                        conn.commit()
                        print("Reservation made successfully!")
                else:
                    print("Please login to make a reservation.")

            elif choice == '4':
                # Implement adjust reservation functionality
                pass

            elif choice == '5':
                show_reservations(cursor)

            elif choice == '6':
                name = input("Enter your name: ")
                email = input("Enter your email: ")
                message = input("Enter your feedback message: ")
                if collect_feedback(cursor, name, email, message):
                    conn.commit()
                    print("Thank you for your feedback!")

            elif choice == '7':
                # Implement delete reservation functionality
                pass

            elif choice == '8':
                view_available_slots(cursor)

            elif choice == '9':
                view_feedback(cursor)

            elif choice == '10':
                restaurant_type = input("Enter restaurant type: ")
                location = input("Enter location: ")
                if add_new_restaurant(cursor, restaurant_type, location):
                    conn.commit()
                    print("New restaurant added successfully!")

            elif choice == '11':
                location_name = input("Enter location name: ")
                if add_new_location(cursor, location_name):
                    conn.commit()
                    print("New location added successfully!")

            elif choice == '12':
                view_best_restaurants(cursor)

            elif choice == '13':
                location_name = input("Enter location name: ")
                find_best_restaurants(cursor, location_name)

            elif choice == '14':
                print("Exiting...")
                conn.close()
                sys.exit()

            else:
                print("Invalid choice. Please try again.")

    except sqlite3.Error as e:
        print("SQLite error:", e)
