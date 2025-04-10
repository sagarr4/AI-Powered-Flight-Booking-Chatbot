import requests
from tabulate import tabulate

# Amadeus API credentials
API_KEY = "F9eJ5Z1mdH92gXF7JkazLFrQ4zELTbP4"
API_SECRET = "2rr0xGWEadDZsvMK"  # Replace with your secret API key
BASE_URL = "https://test.api.amadeus.com"

def predict_flight_price(base_price, days_until_departure, season='regular', time_of_day='afternoon'):
    """
    Predicts a flight price based on simple rules.
    
    Parameters:
    - base_price (float): The base price of the ticket in CAD.
    - days_until_departure (int): Days between booking date and departure date.
    - season (str): 'peak' for holiday seasons, 'regular' otherwise.
    - time_of_day (str): 'morning', 'afternoon', or 'evening' flight time.
    
    Returns:
    - float: Predicted flight price in CAD.
    """
    # Start with the base price
    price = base_price
    
    # Increase price if booked close to departure date
    if days_until_departure <= 7:
        price *= 1.5  # 50% increase within a week
    elif days_until_departure <= 30:
        price *= 1.2  # 20% increase within a month
    
    # Add a premium for peak seasons
    if season == 'peak':
        price *= 1.3  # 30% increase for peak season
    
    # Adjust price based on time of day
    if time_of_day == 'morning':
        price *= 1.1  # 10% increase for morning flights
    elif time_of_day == 'evening':
        price *= 1.05  # 5% increase for evening flights
    
    return round(price, 2)


def get_access_token():
    """Fetch access token from Amadeus."""
    url = f"{BASE_URL}/v1/security/oauth2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": API_SECRET,
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Raise exception for non-200 status codes
        return response.json().get('access_token', None)
    except requests.exceptions.RequestException as e:
        return f"Error retrieving access token: {e}"

def get_iata_code(city_name):
    """Fetch IATA code using static city-to-IATA mapping."""
    # Updated static mapping of city names to IATA codes
    city_to_iata = {
        "New York": "JFK",
        "Los Angeles": "LAX",
        "London": "LHR",
        "Paris": "CDG",
        "Tokyo": "HND",
        "Mumbai": "BOM",
        "Beijing": "PEK",
        "Dubai": "DXB",
        "Sydney": "SYD",
        "Singapore": "SIN",
        "Berlin": "TXL",
        "Kamloops": "YKA",
        "Vancouver": "YVR"
    }

    # Fetch the IATA code if it exists, otherwise return an error
    iata_code = city_to_iata.get(city_name)
    if iata_code:
        return iata_code
    else:
        return f"No IATA code found for {city_name}"

def search_flights(departure_city_name, destination_city_name, flight_type, departure_date, return_date=None):
    """Search flights using the Amadeus API with IATA codes, fetched from city names."""
    
    # Fetch IATA codes for cities
    departure_iata = get_iata_code(departure_city_name)
    destination_iata = get_iata_code(destination_city_name)
    
    # Ensure that valid IATA codes are fetched
    if "No IATA code found" in departure_iata or "No IATA code found" in destination_iata:
        return f"Error: {departure_iata if 'No IATA code found' in departure_iata else destination_iata}"

    # If IATA codes are valid, proceed with flight search
    access_token = get_access_token()
    if access_token is None:
        return "Error: Unable to fetch access token"
    
    # Debugging: Check if the token is correct
    print(f"Access token: {access_token}")
    
    # Amadeus Flight Search API URL
    url = f"{BASE_URL}/v2/shopping/flight-offers"
    
    # Define query parameters for flight search
    params = {
        "originLocationCode": departure_iata,  # 3-letter IATA code for departure city
        "destinationLocationCode": destination_iata,  # 3-letter IATA code for destination city
        "departureDate": departure_date,  # YYYY-MM-DD format
        "returnDate": return_date if flight_type == "round trip" else None,
        "adults": 1,  # For simplicity, assume 1 adult passenger
        "currencyCode": "CAD",  # Default to USD currency
    }

    # Set the correct Authorization header
    headers = {
        "Authorization": f"Bearer {access_token}"  # Include the access token in the request headers
    }

    # Debugging: print the parameters and headers being passed
    print(f"Sending request with parameters: {params}")
    print(f"Headers: {headers}")

    # Make the actual API request
    return make_api_request(url, params, headers)

def make_api_request(url, params, headers):
    """Helper function to make the API request and handle response."""
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise exception for non-200 status codes
        
        flight_data = response.json()
        
        # Check if flight offers are available
        if "data" in flight_data:
            return format_flight_results(flight_data['data'])
        return "Sorry, no flights found for your criteria."
    
    except requests.exceptions.RequestException as e:
        return f"Error searching for flights: {e}"

import csv
from datetime import datetime

def format_flight_results(flights):
    """Format flight results into an HTML table with prices in both CAD, USD, and Predicted Price."""
    conversion_rate = 0.7203  # Updated conversion rate from CAD to USD
    table_rows = []

    # Constructing HTML table rows for each flight
    for flight in flights[:5]:  # Limit to the first 5 flight offers
        airline = flight['validatingAirlineCodes'][0]
        price_cad = float(flight['price']['grandTotal'])
        price_usd = round(price_cad * conversion_rate, 2)  # Convert to USD
        departure_time = flight['itineraries'][0]['segments'][0]['departure']['at']
        arrival_time = flight['itineraries'][0]['segments'][-1]['arrival']['at']

        # Calculate days until departure for prediction
        departure_date = datetime.strptime(departure_time.split("T")[0], "%Y-%m-%d")
        days_until_departure = (departure_date - datetime.now()).days

        # Predict price using a predefined function
        predicted_price = predict_flight_price(price_cad, days_until_departure, season='regular', time_of_day='evening')

        # Add each flight's details as an HTML row
        table_rows.append(f"""
            <tr>
                <td>{airline}</td>
                <td>{price_cad:.2f} CAD</td>
                <td>{price_usd:.2f} USD</td>
                <td>{predicted_price:.2f} CAD</td>
                <td>{departure_time}</td>
                <td>{arrival_time}</td>
            </tr>
        """)

    # Combine rows into a responsive Bootstrap table structure
    flight_table = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <title>Responsive Flight Table</title>
    </head>
    <body>
        <div class="container mt-4">
            <h2 class="text-center mb-4">Available Flights</h2>
            <div class="table-responsive">
                <table class="table table-bordered table-hover">
                    <thead class="table-primary text-center">
                        <tr>
                            <th>Flight Name</th>
                            <th>Price (CAD)</th>
                            <th>Price (USD)</th>
                            <th>Predicted Price (CAD)</th>
                            <th>Departure Time</th>
                            <th>Arrival Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(table_rows)}
                    </tbody>
                </table>
            </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    return flight_table
