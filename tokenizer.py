import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

def custom_tokenizer(text):
    return [lemmatizer.lemmatize(word.lower()) for word in nltk.word_tokenize(text)]
