from flask import Flask, request, jsonify, render_template

from flask_cors import CORS
import json
import random
import pickle
from tokenizer import custom_tokenizer  # ✅ this is key

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load model and intents
model = pickle.load(open('chatbot_model.pkl', 'rb'))
with open('intents.json') as file:
    intents = json.load(file)

def get_bot_response(message):
    tag = model.predict([message])[0]
    for intent in intents['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])
    return "I'm not sure how to respond to that."
@app.route("/")
def index():
    return render_template("index.html") # type: ignore


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    message = data['message']
    response = get_bot_response(message)
    return jsonify({'answer': response})

if __name__ == '__main__':
    app.run(debug=True)
