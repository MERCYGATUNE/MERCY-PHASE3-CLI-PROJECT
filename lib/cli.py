import os
import sys
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone_number = Column(String)  
    email = Column(String)
    party_size = Column(Integer)
    reservation_time = Column(DateTime, default=datetime.now)
    table_number = Column(Integer)

class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    message = Column(String)
    submission_time = Column(DateTime, default=datetime.now)

def create_database(engine):
    Base.metadata.create_all(engine)

def make_reservation(session, name, phone_number, email, party_size, reservation_time, table_number):
    reservation = Reservation(name=name, phone_number=phone_number, email=email, party_size=party_size, reservation_time=reservation_time, table_number=table_number)
    session.add(reservation)
    session.commit()

def adjust_reservation(session, reservation_id, party_size, table_number):
    reservation = session.query(Reservation).filter_by(id=reservation_id).first()
    if reservation:
        reservation.party_size = party_size
        reservation.table_number = table_number
        session.commit()
        print("Reservation adjusted successfully!")
    else:
        print("Reservation not found.")

def delete_reservation(session, reservation_id):
    reservation = session.query(Reservation).filter_by(id=reservation_id).first()
    if reservation:
        session.delete(reservation)
        session.commit()
        print("Reservation deleted successfully!")
    else:
        print("Reservation not found.")

def show_reservations(session):
    reservations = session.query(Reservation).all()
    if reservations:
        for reservation in reservations:
            print(f"Reservation ID: {reservation.id}, Name: {reservation.name}, Phone Number: {reservation.phone_number}, Email: {reservation.email}, Party Size: {reservation.party_size}, Table Number: {reservation.table_number}, Time: {reservation.reservation_time.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("No reservations found.")

def collect_feedback(session, name, email, message):
    feedback = Feedback(name=name, email=email, message=message)
    session.add(feedback)
    session.commit()

if __name__ == "__main__":
    print("Welcome to Rave!!The Restaurant Reservation System!")
    restaurant_type = input("Select the type of restaurant (e.g., French,Italian, Mexican, Chinese): ")
    location = input("Enter the location of the restaurant: ")

    
    database_url = f'sqlite:///{restaurant_type.lower()}_{location.lower()}_restaurant.db'

    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    create_database(engine)
    

    while True:
        print("\nRave Restaurant Reservation System")
        print("1. Make a reservation")
        print("2. Adjust a reservation")
        print("3. View reservations")
        print("4. Provide Feedback")
        print("5. Delete a reservation")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter your name: ")
            phone_number = input("Enter your phone number: ")
            email = input("Enter your email: ")
            party_size = int(input("Enter party size: "))
            reservation_time = input("Enter reservation time (YYYY-MM-DD HH:MM:SS): ")
            try:
                reservation_time = datetime.strptime(reservation_time, "%Y-%m-%d %H:%M:%S")
                table_number = int(input("Enter table number: "))
                make_reservation(session, name, phone_number, email, party_size, reservation_time, table_number)
                print("Reservation made successfully!")
            except ValueError:
                print("Invalid date/time or table number format. Please enter date/time in YYYY-MM-DD HH:MM:SS format and table number as an integer.")

        elif choice == '2':
            reservation_id = int(input("Enter the ID of the reservation to adjust: "))
            party_size = int(input("Enter new party size: "))
            table_number = int(input("Enter new table number: "))
            adjust_reservation(session, reservation_id, party_size, table_number)

        elif choice == '3':
            show_reservations(session)

        elif choice == '4':
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            message = input("Enter your feedback message: ")
            collect_feedback(session, name, email, message)
            print("Thank you for your feedback!")

        elif choice == '5':
            reservation_id = int(input("Enter the ID of the reservation to delete: "))
            delete_reservation(session, reservation_id)

        elif choice == '6':
            print("Exiting...")
            session.close()
            sys.exit()

        else:
            print("Invalid choice. Please try again.")
