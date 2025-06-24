from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import nltk
import json
import random
import os
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import joblib

# === Setup NLTK ===
nltk.download('punkt')
nltk.download('wordnet')

app = Flask(__name__)
CORS(app)

# === Paths ===
INTENTS_PATH = 'intents.json'
MODEL_PATH = 'model.joblib'

lemmatizer = WordNetLemmatizer()

# === Tokenizer with Lemmatization ===
def tokenize(text):
    tokens = word_tokenize(text.lower())
    return [lemmatizer.lemmatize(t) for t in tokens]

# === Load Intents ===
def load_intents():
    with open(INTENTS_PATH, 'r') as f:
        return json.load(f)

# === Train Model ===
def train_model():
    intents = load_intents()
    texts, labels = [], []

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            texts.append(pattern)
            labels.append(intent['tag'])

    pipeline = make_pipeline(
        TfidfVectorizer(tokenizer=tokenize),
        LogisticRegression(max_iter=1000)
    )
    pipeline.fit(texts, labels)
    joblib.dump(pipeline, MODEL_PATH)
    print("✅ Model trained and saved.")

# === Load Model ===
if not os.path.exists(MODEL_PATH):
    train_model()
model = joblib.load(MODEL_PATH)
intents = load_intents()

# === Get Response ===
def get_response(message):
    tag = model.predict([message])[0]
    for intent in intents['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])
    return "I'm not sure how to help with that."

# === Routes ===
@app.route("/")
def home():
    return render_template("index.html")  # Optional: Add UI if needed

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"answer": "Please enter a message."})
    response = get_response(user_message)
    return jsonify({"answer": response})

@app.route("/retrain", methods=["POST"])
def retrain():
    train_model()
    global model
    model = joblib.load(MODEL_PATH)
    return jsonify({"status": "Model retrained successfully."})

# === Start App ===
if __name__ == "__main__":
    app.run(debug=True)
