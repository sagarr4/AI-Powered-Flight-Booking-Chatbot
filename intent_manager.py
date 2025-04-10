import random

# Predefined intents
intents = {
    "GreetUser": {
          "responses": [
            "Hi! Welcome aboard. How can I help you today? \ Bonjour ! Bienvenue à bord. Comment puis-je vous aider aujourd'hui ?",
            "Hello! We’re delighted to welcome you. What can I do for you? \ Bonjour ! Nous sommes ravis de vous accueillir. Que puis-je faire pour vous ?",
            "Good morning, and welcome! How may I assist you today? \ Bonjour et bienvenue ! Comment puis-je vous assister aujourd'hui ?",
            "Good afternoon, and welcome! Is there anything I can help you with? \ Bon après-midi et bienvenue ! Y a-t-il quelque chose avec lequel je peux vous aider ?",
            "Good evening, and welcome! How can I be of service? \ Bonsoir et bienvenue ! En quoi puis-je vous être utile ?"
          ]
          },
    "AskDeparture": {
          "responses": [
            "Great! Where are you planning to fly from? \ Super ! D'où prévoyez-vous de partir ?",
            "Please tell me your Departure city. \ Veuillez me dire votre ville de départ.",
            "What is your Departure? \ Quelle est votre ville de départ ?",
            "Can you share the city you want to fly From? \ Pouvez-vous partager la ville d'où vous souhaitez partir ?",
            "From where would you like to go? \ D'où aimeriez-vous partir ?"
          ]
        },
    "AskDestination": {
          "responses": [
            "Great! Where are you planning to fly to? \ Super ! Où prévoyez-vous de vous rendre ?",
            "Please tell me your Destination city. \ Veuillez me dire votre ville de destination.",
            "What is your Destination? \ Quelle est votre ville de destination ?",
            "Can you share the city you want to fly to? \ Pouvez-vous partager la ville où vous souhaitez vous rendre ?",
            "Where would you like to go? \ Où aimeriez-vous aller ?"
          ]
},
    "AskFlightType": {
          "responses": [
            "Is it a One-Way or Round Trip? \ Est-ce un aller simple ou un aller-retour ?",
            "What type of trip is it One-Way or Round? \ Quel type de voyage est-ce, aller simple ou aller-retour ?"
          ]
},
    "AskOneDate": {
          "responses": [
            "Please provide the departure date for your one-way trip in the format YYYY-MM-DD. \ Veuillez fournir la date de départ pour votre voyage aller simple au format YYYY-MM-DD.",
            "What date will you be departing on your one-way trip? Use the format YYYY-MM-DD. \ Quelle est la date de départ de votre voyage aller simple ? Utilisez le format YYYY-MM-DD."
          ]
},
    "AskTwoDate": {
          "responses": [
            "Please provide the departure date for your round-trip in the format YYYY-MM-DD. Once you provide that, I'll also need your return date. \ Veuillez fournir la date de départ pour votre voyage aller-retour au format YYYY-MM-DD. Une fois cela fait, j'aurai également besoin de votre date de retour.",
            "What is the departure date for your round-trip? After that, please give me the return date, both in the format YYYY-MM-DD. \ Quelle est la date de départ pour votre voyage aller-retour ? Ensuite, veuillez me fournir la date de retour, les deux au format YYYY-MM-DD."
          ]
},
    "CollectFlightDetails": {
        "responses": [
            "Your flight details:\n{table}",
            "You are flying from {departure_city} to {destination_city} with a {flight_type} ticket.\nYour travel dates are: {dates}",
            "Flight information confirmed: Departing from {departure_city} to {destination_city}. Type of flight: {flight_type}.\nTravel Dates: {dates}.",
            "Your booking is noted: You will depart from {departure_city} to {destination_city}. Flight type: {flight_type}.\nTravel Dates: {dates}."
        ]
},
    "EndConversation": {
          "responses": [
            "You're very welcome! Safe travels, and feel free to reach out if you need anything else. \ Je vous en prie ! Bon voyage, et n'hésitez pas à me contacter si vous avez besoin de quoi que ce soit.",
            "Thank you for choosing [Airline Name]! Have a wonderful journey! \ Merci d'avoir choisi [Nom de la compagnie aérienne] ! Passez un merveilleux voyage !",
            "It was my pleasure assisting you. Goodbye, and have a great day! \ Ce fut un plaisir de vous aider. Au revoir, et passez une excellente journée !",
            "Safe travels! If you need further assistance, I'm here to help. \ Bon voyage ! Si vous avez besoin d'aide supplémentaire, je suis là pour vous aider.",
            "Thank you, and take care! Hope to see you again soon! \ Merci, et prenez soin de vous ! J'espère vous revoir bientôt !"
          ]
},
    "ValidateLogin": {
          "responses": [
            "Please login to proceed with booking \ Veuillez vous connecter pour continuer la réservation."
          ]
},
     "Help" : {
          "responses": [
                f"""
        I'm sorry, I didn't understand that. Here are some resources that might help:

        1. **How to Book a Flight**: [Flight Booking Guide](#)
        2. **Mail Support**: [Frequently Asked Questions](mailto:sagarbmw1@gmail.com)
        3. **Contact Support**: [Call Us at 236-338-4424](tel:2363384424)

        Feel free to ask any specific questions, and I'll try to assist you further!
        """
          ]
     }
}

def get_intent_response(intent_name):
    """Returns a random response for a given intent."""
    if intent_name in intents:
        return random.choice(intents[intent_name]["responses"])
    return "I'm sorry, I don't have a response for that."