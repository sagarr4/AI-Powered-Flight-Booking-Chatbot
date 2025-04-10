from dotenv import load_dotenv
load_dotenv()
from tkinter import Y
from scripts.intent_manager import get_intent_response
from scripts.city_manager import fuzzy_match_city, fetch_city_names
from scripts.flight_results import search_flights
from datetime import datetime
from tabulate import tabulate
import pyodbc
import scripts.email_notifications as email_notifications
import os
import re

def validate_email(email):
    """
    Validates an email address using a regex pattern.
    Returns True if the email is valid, otherwise False.
    """
    # Regular expression pattern for validating an email
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Use the re.match() function to check if the email matches the pattern
    if re.match(email_pattern, email):
        return True
    else:
        return False

# Establish connection to Microsoft SQL Server
import os

conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={os.getenv('DB_SERVER')};"
    f"DATABASE={os.getenv('DB_NAME')};"
    f"UID={os.getenv('DB_USER')};"
    f"PWD={os.getenv('DB_PASSWORD')};"
)



cursor = conn.cursor()

def save_booking_to_db():
    """Saves the booking details to the Microsoft SQL Server database."""
    booking_data = (
        user_details['departure_city'],
        user_details['destination_city'],
        user_details['flight_type'],
        user_details['departure_date'],
        user_details.get('return_date', None),  # Round trip might not have a return date
        datetime.now()  # Booking time as current timestamp
    )

    cursor.execute('''
    INSERT INTO tbl_UserDetails (departureCity, destinationCity, flightType, departureDate, returnDate, bookingDate)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', booking_data)
    
    conn.commit()

# Initialize user details to keep track of booking information
user_details = {
    'departure_city': None,
    'destination_city': None,
    'is_booking': False,
    'flight_type': None,
    'departure_date': None,
    'return_date': None,
    'has_greeted': False,
    'passport_photo':None,
    'has_farewelled': False,
    'isLogin':'Y'
}

def show_booking_summary():
    """
    Displays the user's booking details in a table format if all necessary details are available.
    """
    booking_data = [
        ["Departure City", user_details['departure_city']],
        ["Destination City", user_details['destination_city']],
        ["Flight Type", user_details['flight_type'].capitalize()],
        ["Departure Date", user_details['departure_date']]
    ]
    
    if user_details['flight_type'] == "round trip":
        booking_data.append(["Return Date", user_details['return_date']])

    
    booking_table = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Booking Details</title>
        <!-- Add Bootstrap CSS link -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container my-4">
            <h2 class="text-center mb-4">Booking Details</h2>
            <table class="table table-bordered table-striped">
                <thead class="table-dark">
                    <tr>
                        <th>Booking Detail</th>
                        <th>Information</th>
                    </tr>
                </thead>
                <tbody>
    """

    # Add each row of the booking data
    for item in booking_data:
        booking_table += f"""
            <tr>
                <td>{item[0]}</td>
                <td>{item[1]}</td>
            </tr>
        """

    # Close the table HTML
    booking_table += "</tbody></table>"

    return f"{booking_table}"

def is_valid_date(date_str):
    """
    Validates that the date string is in the format YYYY-MM-DD and is not a past date.
    """
    try:
        date = datetime.strptime(date_str.strip(), "%Y-%m-%d")
        return date >= datetime.now()
    except ValueError:
        return False

def check_city(user_input, city_names):
    """Check if a city in the user's input matches a known city."""
    return fuzzy_match_city(user_input, city_names)

def get_response(user_input):
    """
    Main function to generate responses based on user input.
    """
    user_input = user_input.lower().strip()
    city_names = fetch_city_names()
    
    # Handle greeting
    if not user_details['has_greeted'] and any(greet in user_input for greet in ["hi", "hello", "good morning", "good afternoon", "good evening"]):
        user_details['has_greeted'] = True
        return get_intent_response("GreetUser")


    # Start booking process
    if any(intent in user_input for intent in ["book a flight", "i want to book a flight", "i want to book a flight ticket", "help me book", "want to fly", "planning a trip"]) and not user_details['is_booking'] and user_details['isLogin'] == 'Y':
        user_details['is_booking'] = True
        return get_intent_response("AskDeparture")
    elif user_details['isLogin'] == 'N' :
       return get_intent_response("ValidateLogin")

    # Capture departure city
    if user_details['is_booking'] and not user_details['departure_city']:
        matched_city = check_city(user_input, city_names)
        if matched_city:
            user_details['departure_city'] = matched_city
            return get_intent_response("AskDestination")

    # Capture destination city
    if user_details['is_booking'] and user_details['departure_city'] and not user_details['destination_city']:
        matched_city = check_city(user_input, city_names)
        if matched_city:
            user_details['destination_city'] = matched_city
            return get_intent_response("AskFlightType")

    # Capture flight type
    if user_details['is_booking'] and user_details['departure_city'] and user_details['destination_city'] and not user_details['flight_type']:
        if "one way" in user_input:
            user_details['flight_type'] = "one way"
            return get_intent_response("AskOneDate")
        elif "round trip" in user_input:
            user_details['flight_type'] = "round trip"
            return get_intent_response("AskTwoDate")
        else:
            return "What type of trip is it? One Way or Round Trip?"

        # For one-way flights
    if user_details['flight_type'] == "one way":
        if not user_details['departure_date']:
            if is_valid_date(user_input):
                user_details['departure_date'] = user_input
                # Perform the flight search immediately after setting the departure date
                flight_results = search_flights(
                    user_details['departure_city'],
                    user_details['destination_city'],
                    user_details['flight_type'],
                    user_details['departure_date']
                )
                save_booking_to_db()
                # Combine the booking summary and flight results for one-way flight
                return f"{show_booking_summary()}\n{flight_results}\n Can you Please enter a valid Email for Email Notifications"


            return "Please enter a valid departure date in the format YYYY-MM-DD (must be today or in the future)."

    # For round-trip flights
    if user_details['flight_type'] == "round trip":
        if not user_details['departure_date']:
            if is_valid_date(user_input):
                user_details['departure_date'] = user_input
                return "Thank you. Now, please provide the return date. Veuillez entrer une date de retour qui soit apres votre date de depart."
            return "Please enter a valid departure date in the format YYYY-MM-DD (must be today or in the future)."
    
        if not user_details['return_date']:
            if is_valid_date(user_input):
                return_date = datetime.strptime(user_input, "%Y-%m-%d")
                departure_date = datetime.strptime(user_details['departure_date'], "%Y-%m-%d")
            
                if return_date > departure_date:
                    user_details['return_date'] = user_input
                    # Perform the flight search after both dates are set
                    flight_results = search_flights(
                        user_details['departure_city'],
                        user_details['destination_city'],
                        user_details['flight_type'],
                        user_details['departure_date'],
                        user_details['return_date']
                    )
                    save_booking_to_db()
                    # Combine the booking summary and flight results for round-trip flight
                    return f"{show_booking_summary()}\n{flight_results}\n Can you Please enter a valid Email for Email Notifications"

                return "Please enter a return date that is after your departure date. Veuillez entrer une date de retour qui soit apres votre date de depart."
            return "Please enter a valid return date in the format YYYY-MM-DD (must be today or in the future)."

    # Handle email submission
    if "gmail" in user_input:
        email = user_input.strip()
        if validate_email(email):  # Validate email using your validation function
            # Process the email (send flight details to this email)
            flight_results = search_flights(
                        user_details['departure_city'],
                        user_details['destination_city'],
                        user_details['flight_type'],
                        user_details['departure_date'],
                        user_details['return_date']
                    )
            email_notifications.send_email(email, flight_results)  # Example function to send the email
            return f"Your flight details have been sent to {email}.\n Please attach your Doucuments using the attach icon"
        else:
            return "Please enter a valid email address."
   
    if not user_details['has_farewelled'] and any(
        farewell in user_input.lower() for farewell in ["bye", "see you", "thank you", "goodbye", "get lost"]):
            user_details['has_farewelled'] = True
            return get_intent_response("EndConversation")      

    return(f"I'm sorry, I didn't quite understand that. Here are some helpful resources for you futher: Contact no:(236-338-1111), Mail (sagarbmw1@gmail.com)")

