# Flight Booking Chatbot ✈️

A conversational AI assistant that helps users find and book flights through natural language interactions.

## Features 🌟
- **Dual Interface**: Web-based (Flask) and command-line versions
- **City Recognition**: Fuzzy matching for accurate city name understanding
- **Flight Management**: Core logic for handling flight searches and bookings
- **Intent Handling**: Processes different user requests (booking, searching, etc.)
- **Email Notifications**: Optional email confirmation system

## Installation 🛠️

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/flight-booking-chatbot.git
   cd flight-booking-chatbot
2. Install Dependencies:
   ```bash
   pip install -r requirements.txt
3.Web Interface (Recommended)
  ```bash
   python app.py
  ```
  Command Line Interface
  ```bash
  python chat.py
  ```
3.Project Structure 📂
```
  ├── app.py                 # Flask web application
├── chat.py                # Command-line interface
├── city_manager.py        # Handles city name recognition
├── flight_manager.py      # Core flight logic
├── flight_results.py      # Flight data processing
├── intent_manager.py      # User intent classification
├── email_notifications.py # Email confirmation system
└── requirements.txt       # Python dependencies
