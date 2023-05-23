import pdfplumber
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import numpy as np

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')

def tokenize(text):
    text = "".join([ch for ch in text if ch not in string.punctuation])
    tokens = nltk.word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized

def process_pdf(pdf_path, number_of_terms):
    with pdfplumber.open(pdf_path) as pdf:
        text = '\n'.join(page.extract_text() for page in pdf.pages)
    documents = [text]
    vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'), tokenizer=tokenize)
    X = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()
    tfidf = X.toarray()[-1]
    indices = np.argsort(tfidf)[::-1]
    top_features = [(feature_names[i], tfidf[i]) for i in indices[:number_of_terms]]
    key_terms = {}
    for word, _ in top_features:
        synsets = wordnet.synsets(word)
        if synsets:
            key_terms[word] = synsets[0].definition()
    return key_terms