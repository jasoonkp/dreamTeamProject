import os
from flask import Flask, redirect, render_template, request, jsonify, session, url_for
from dotenv import load_dotenv
from openai import OpenAI
from firebase_admin import credentials, auth, initialize_app
from functools import wraps

# Initialize the Firebase Admin SDK
cred = credentials.Certificate(".private/firebase.service.key.json")
initialize_app(cred)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Load the .env file where your API key is stored
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Decorator: Login Required!
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        app.logger.info("login_required: User ID in session: %s", session.get('user_id'))
        # Check if the user is logged in
        if 'user_id' not in session:
            return redirect(url_for('login'))  # Redirect to login page
        return f(*args, **kwargs)
    return decorated_function

# Load instructions from the text file
with open("GPT_instructions.txt", "r") as file:
    gpt_instructions = file.read()

client = OpenAI(api_key=OPENAI_API_KEY)

# Route to serve the web page
@app.route("/")
@login_required
def home():
    app.logger.info("Rendering the '/' route!")
    return render_template("index.html")

@app.route("/login", methods=['GET'])
def login():
    app.logger.info("login: User ID in session: %s", session.get('user_id'))
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template("login.html")

@app.route('/newchat')
@login_required  # Ensure the user is logged in before accessing this route
def newchat():
    return render_template("subjects.html")  # Render the subjects.html template

@app.route('/login', methods=['POST'])
def login_api():
    id_token = request.json.get('idToken')  # Get the ID token from the request
    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(id_token)
        session['user_id'] = decoded_token['uid']  # Store user ID in session
        return {'status': 'success'}, 200
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 401

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    app.logger.info("logout: User ID in session: %s", session.get('user_id'))
    return redirect(url_for('login'))  # Redirect to login page

# API route to handle GPT interaction
@app.route('/ask', methods=['POST'])
@login_required
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

def is_logged_in():
    return 'user_id' in session

if __name__ == '__main__':
    app.run(debug=True)
