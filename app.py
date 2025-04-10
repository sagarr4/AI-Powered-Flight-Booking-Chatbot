from flask import Flask, request, jsonify, render_template
from flight_manager import get_response  # Assuming this is where your logic resides

app = Flask(__name__)

# Route to render the homepage (index.html)
@app.route('/')
def index():
    return render_template('index.html')  # Render your chat interface (index.html)

# Route to handle POST requests for chat
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()  # Get the incoming JSON data
        if not data or not data.get('message'):
            return jsonify({"response": "Please send a valid message."}), 400

        user_message = data.get('message')  # Extract user message

        # Process the user's message and get a response using your flight_manager logic
        response = get_response(user_message)

        return jsonify({"response": response})  # Return the chatbot's response

    except Exception as e:
        return jsonify({"response": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
