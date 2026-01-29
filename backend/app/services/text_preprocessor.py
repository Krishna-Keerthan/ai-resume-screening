# backend/app/services/text_preprocessor.py
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import string

class TextPreprocessor:
    def __init__(self):
        # Download required NLTK data (if not already downloaded)
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')
        
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
    
    def preprocess(self, text, remove_stopwords=True, lemmatize=True):
        """
        Preprocess text for NLP tasks
        
        Args:
            text: Input text
            remove_stopwords: Whether to remove stopwords
            lemmatize: Whether to lemmatize tokens
        
        Returns:
            Preprocessed text as string
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove punctuation and special characters
        text = re.sub(f'[{re.escape(string.punctuation)}]', ' ', text)
        
        # Remove numbers (optional - you may want to keep years of experience)
        # text = re.sub(r'\d+', '', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords
        if remove_stopwords:
            tokens = [token for token in tokens if token not in self.stop_words]
        
        # Lemmatize
        if lemmatize:
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        # Remove single characters and empty tokens
        tokens = [token for token in tokens if len(token) > 1]
        
        # Join back to string
        return ' '.join(tokens)
    
    def get_tokens(self, text):
        """Get list of tokens from text"""
        preprocessed = self.preprocess(text)
        return preprocessed.split()