import json
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from tokenizer import custom_tokenizer

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

# Define a tokenizer function instead of using lambda
def custom_tokenizer(text):
    return [lemmatizer.lemmatize(word.lower()) for word in nltk.word_tokenize(text)]

# Load intents file
with open('intents.json') as file:
    data = json.load(file)

# Prepare data for training
training_sentences = []
training_labels = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        training_sentences.append(pattern)
        training_labels.append(intent['tag'])

# Create a machine learning pipeline with the named tokenizer
model = make_pipeline(
    TfidfVectorizer(tokenizer=custom_tokenizer),
    LogisticRegression(max_iter=1000)
)

# Train the model
model.fit(training_sentences, training_labels)

# Save the trained model to a file
with open('chatbot_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("✅ Model trained and saved as chatbot_model.pkl")
