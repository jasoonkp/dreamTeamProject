import os
from flask import Flask, render_template, request,jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import firebase_admin
from firebase_admin import credentials, auth

# Initialize the Firebase Admin SDK
cred = credentials.Certificate(".private/firebase.service.key.json")
firebase_admin.initialize_app(cred)

# Initialize Flask app
app = Flask(__name__)

# Load the .env file where your API key is stored
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load instructions from the text file
with open("GPT_instructions.txt", "r") as file:
    gpt_instructions = file.read()

client = OpenAI(api_key=OPENAI_API_KEY)

# Route to serve the web page
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=['GET'])
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_submit():
    # Extracting the ID token from the request
    id_token = request.form.get('id_token')  # Assuming the client sends the ID token

    # Attempting to verify the ID token
    try:
        app.logger.info(f"ID Token: {id_token}")
        user = auth.verify_id_token(id_token)  # Verify the ID token
        app.logger.info(f"User: {user}")
        # Returning a JSON response with a success message and user ID
        return jsonify({"message": "Login successful", "user_id": user['uid']}), 200
    except Exception as e:
        # Logging the error for debugging purposes
        app.logger.error(f"Login failed: {e}")
        # Returning a JSON response with an error message and a 401 status code
        return jsonify({"message": "Login failed", "error": str(e)}), 401

# API route to handle GPT interaction
@app.route('/ask', methods=['POST'])
def ask_gpt():
    user_message = request.json.get('message')  # Get the user's message from the frontend

# Create the message history (you can keep it dynamic if needed)
    messages = [
        {"role": "system", "content": gpt_instructions},
        {"role": "user", "content": user_message}
    ]

# Call OpenAI's API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    assistant_response = response.choices[0].message.content

    return jsonify({"response": assistant_response})  # Return the assistant's response as JSON

if __name__ == '__main__':
    app.run(debug=True)