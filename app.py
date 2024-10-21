from flask import Flask, render_template, request,jsonify
from dotenv import load_dotenv
from openai import OpenAI

# Load the .env file where your API key is stored
load_dotenv()

# Load instructions from the text file
with open("GPT_instructions.txt", "r") as file:
    gpt_instructions = file.read()

client = OpenAI()

# Initialize Flask app
app = Flask(__name__)

# Route to serve the web page
@app.route("/")
def home():
    return render_template("index.html")

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

if __name__ == "__main__":
    app.run(debug=True)