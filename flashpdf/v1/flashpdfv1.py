import pdfplumber
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import numpy as np

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')

# Function to tokenize words and lemmatize them
def tokenize(text):
    text = "".join([ch for ch in text if ch not in string.punctuation])
    tokens = nltk.word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized

# Use pdfplumber to extract text from the pdf
with pdfplumber.open("iceburger.pdf") as pdf:
    text = '\n'.join(page.extract_text() for page in pdf.pages)

# Convert text into a list
documents = [text]

# Apply TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'), tokenizer=tokenize)
X = vectorizer.fit_transform(documents)

# Get feature names and tfidf score of last document
feature_names = vectorizer.get_feature_names_out()
tfidf = X.toarray()[-1]

# Get indices sorted by score
indices = np.argsort(tfidf)[::-1]

# Get top n terms with highest tfidf
n = 100
top_features = [(feature_names[i], tfidf[i]) for i in indices[:n]]

# Create a dictionary to hold the key terms and their definitions
key_terms = {}

# Iterate over each word
for word, _ in top_features:
    # Check if wordnet has a definition for this word
    synsets = wordnet.synsets(word)
    if synsets:
        # If there are synsets, use the definition of the first one as the definition of the word
        key_terms[word] = synsets[0].definition()

print(key_terms)

