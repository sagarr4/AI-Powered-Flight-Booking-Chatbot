# ✈️ AI Powered Flight Booking Chatbot Assistant 🤖

![Demo](https://img.shields.io/badge/Demo-Available-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey)

An intelligent flight booking chatbot with both **Web UI** and **Command Line Interface**. Supports natural conversations, city name recognition, booking logic, and email confirmations.

---

## 🌟 Features

- **Dual Interfaces**
  - 🌐 Web-based interface (Flask + REST API)
  - 💻 Command-line version for local testing
- **Smart City Recognition**
  - 🌍 50,000+ global cities
  - 🔍 Fuzzy matching (e.g., _"San Fransico"_ → _"San Francisco"_)
- **Core Flight Operations**
  - ✈️ Search & booking logic
  - 📅 Date/time parsing
  - 💸 Price comparison logic
- **Conversational Intelligence**
  - 🧠 Intent detection (NLP)
  - 📧 Email confirmation system
  - 🔁 Context-aware dialogue management

---

## 🛠️ Setup & Installation

```bash
# Clone the repo
git clone https://github.com/your-username/flight-booking-chatbot.git
cd flight-booking-chatbot

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Recommended for faster fuzzy matching
pip install python-Levenshtein
```

---

## 🚀 Usage

### ▶️ Web Interface
```bash
python app.py
```
Visit: [http://localhost:5000](http://localhost:5000)

### 💬 CLI Interface
```bash
python chat.py
```
Example queries:
- `Find flights from Mumbai to Dubai next week`
- `Book a flight from New York to Berlin on May 20`
- Type `exit` to quit

---

## 📁 Project Structure

```
flight-booking-chatbot/
├── app.py                  # Web interface (Flask)
├── chat.py                 # CLI tool
│
├── core/                   # Core logic modules
│   ├── city_manager.py         # City recognition + fuzzy matching
│   ├── flight_manager.py       # Booking/search logic
│   ├── intent_manager.py       # Intent classification
│   ├── flight_results.py       # Sample flight data logic
│   └── email_notifications.py  # Email confirmations
│
├── templates/              # HTML templates (Flask UI)
│   └── index.html
├── static/                 # JS/CSS assets
├── requirements.txt        # Python dependencies
└── README.md               # You're here!
```

---

## 📦 Dependencies

| Package              | Purpose                        |
|----------------------|--------------------------------|
| Flask                | Web framework                  |
| geonamescache        | City database (50k+ cities)    |
| fuzzywuzzy           | Fuzzy string matching          |
| python-Levenshtein   | Optimizes fuzzy matching speed |
| smtplib (builtin)    | Email notifications            |

---

## 🧪 Quick Testing

### 🏙️ City Match Test
```python
from core.city_manager import fuzzy_match_city
print(fuzzy_match_city("los angles"))  # → "Los Angeles"
```

### 🔌 API Test (POST)
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"flights from Paris to Rome"}'
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more details.

---

## 📬 Contact

**Your Name** – Sagar Prajapati  
Project Link: [https://github.com/your-username/flight-booking-chatbot](https://github.com/your-username/flight-booking-chatbot)


### ✅ Key Improvements:
- More structured and scannable layout
- Simplified technical terms where possible
- Enhanced visuals using spacing and emojis
- Polished project description and headings
- Easier to follow setup and commands
