from models import Database, Reservation, Feedback, Restaurant, Location, User, AvailableSlot, BestRestaurant

def add_reservation_cmd():
    name = input("Enter name: ")
    party_size = int(input("Enter party size: "))
    reservation_time = input("Enter reservation time (YYYY-MM-DD HH:MM): ")
    phone_number = input("Enter phone number: ")
    table_number = int(input("Enter table number: "))
    email = input("Enter email: ")
    restaurant_id = int(input("Enter restaurant ID: "))
    location_id = int(input("Enter location ID: "))
    user_id = int(input("Enter user ID: "))
    
    reservation_model.add(name, party_size, reservation_time, phone_number, table_number, email, restaurant_id, location_id, user_id)
    print("Reservation added successfully.")
    
def find_reservation_cmd():
    reservation_id = int(input("Enter reservation ID: "))
    reservation = reservation_model.find(reservation_id)
    if reservation:
        print(f"Reservation details:")
        print(f"ID: {reservation[0]}")
        print(f"Name: {reservation[1]}")
        print(f"Party Size: {reservation[2]}")
        print(f"Reservation Time: {reservation[3]}")
        print(f"Phone Number: {reservation[4]}")
        print(f"Table Number: {reservation[5]}")
        print(f"Email: {reservation[6]}")
        print(f"Restaurant ID: {reservation[7]}")
        print(f"Location ID: {reservation[8]}")
        print(f"User ID: {reservation[9]}")
    else:
        print(f"Reservation with ID {reservation_id} not found.")

def add_feedback_cmd():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    message = input("Enter your feedback message: ")
    submission_time = input("Enter submission time (YYYY-MM-DD HH:MM): ")
    
    feedback_model.add(name, email, message, submission_time)
    print("Feedback added successfully.")

def add_restaurant_cmd():
    restaurant_type = input("Enter restaurant type: ")
    location = input("Enter location: ")
    
    restaurant_model.add(restaurant_type, location)
    print("Restaurant added successfully.")

def show_reservations_cmd():
    reservations = reservation_model.show_all()
    if reservations:
        for reservation in reservations:
            print(reservation)
    else:
        print("No reservations found.")

def show_feedback_cmd():
    feedbacks = feedback_model.show_all()
    if feedbacks:
        for feedback in feedbacks:
            print(feedback)
    else:
        print("No feedback found.")

def show_restaurants_cmd():
    restaurants = restaurant_model.show_all()
    if restaurants:
        for restaurant in restaurants:
            print(restaurant)
    else:
        print("No restaurants found.")

def add_location_cmd():
    name = input("Enter location name: ")
    location_model.add(name)
    print("Location added successfully.")

def show_locations_cmd():
    locations = location_model.show_all()
    if locations:
        for location in locations:
            print(location)
    else:
        print("No locations found.")

def add_user_cmd():
    username = input("Enter username: ")
    password = input("Enter password: ")
    user_model.add(username, password)
    print("User added successfully.")

def show_users_cmd():
    users = user_model.show_all()
    if users:
        for user in users:
            print(user)
    else:
        print("No users found.")

def add_available_slot_cmd():
    location_id = input("Enter location ID: ")
    reservation_time = input("Enter reservation time (YYYY-MM-DD HH:MM): ")
    available_slot_model.add(location_id, reservation_time)
    print("Available slot added successfully.")

def show_available_slots_cmd():
    available_slots = available_slot_model.show_all()
    if available_slots:
        for slot in available_slots:
            print(slot)
    else:
        print("No available slots found.")

def add_best_restaurant_cmd():
    location_id = int(input("Enter location ID: "))
    restaurant_type = input("Enter restaurant type: ")
    reservation_count = int(input("Enter reservation count: "))
    best_restaurant_model.add(location_id, restaurant_type, reservation_count)
    print("Best restaurant added successfully.")

def show_best_restaurants_cmd():
    best_restaurants = best_restaurant_model.show_all()
    if best_restaurants:
        for restaurant in best_restaurants:
            print(restaurant)
    else:
        print("No best restaurants found.")

def menu():
    print("Welcome to Rave Restaurant Reservation:")
    print("1. Add a reservation")
    print("2. Show all reservations")
    print("3. Find a reservation by ID")
    print("4. Delete a reservation")
    print("5. Add feedback")
    print("6. Show all feedback")
    print("7. Add a restaurant")
    print("8. Show all restaurants")
    print("9. Add a location")
    print("10. Show all locations")
    print("11. Register user")
    print("12. View all registered users")
    print("13. Add an available slot")
    print("14. Show all available slots")
    print("15. Add a best restaurant")
    print("16. Show all best restaurants")
    print("0. Exit the program")

def main():
    global reservation_model, feedback_model, restaurant_model, location_model, user_model, available_slot_model, best_restaurant_model
    db = Database()
    reservation_model = Reservation(db)
    feedback_model = Feedback(db)
    restaurant_model = Restaurant(db)
    location_model = Location(db)
    user_model = User(db)
    available_slot_model = AvailableSlot(db)
    best_restaurant_model = BestRestaurant(db)
    
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            db.close()
            exit()
        elif choice == "1":
            add_reservation_cmd()
        elif choice == "2":
            show_reservations_cmd()
        elif choice == "3":
            find_reservation_cmd()
        elif choice == "4":
          delete_reservation_cmd()
        elif choice == "5":
            add_feedback_cmd()
        elif choice == "6":
            show_feedback_cmd()
        elif choice == "7":
            add_restaurant_cmd()
        elif choice == "8":
            show_restaurants_cmd()
        elif choice == "9":
            add_location_cmd()
        elif choice == "10":
            show_locations_cmd()
        elif choice == "11":
            add_user_cmd()
        elif choice == "12":
            show_users_cmd()
        elif choice == "13":
            add_available_slot_cmd()
        elif choice == "14":
            show_available_slots_cmd()
        elif choice == "15":
            add_best_restaurant_cmd()
        elif choice == "16":
            show_best_restaurants_cmd()
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
