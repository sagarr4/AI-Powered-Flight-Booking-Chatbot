import sys
from scripts.flight_manager import get_response

def main():
    print("Welcome to the Flight Booking Assistant!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Flight Booking Assistant: Goodbye! Have a great day!")
            break
        response = get_response(user_input)
        print(f"Bunty: {response}")

if __name__ == "__main__":
    main()
