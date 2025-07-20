from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        RotatingFileHandler('sentiment_api.log', maxBytes=1000000, backupCount=5),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except Exception as e:
    logger.error(f"Failed to download NLTK data: {str(e)}")

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Initialize the sentiment analysis pipeline
try:
    sentiment_analyzer = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        tokenizer="distilbert-base-uncased-finetuned-sst-2-english"
    )
    logger.info("Sentiment analysis pipeline initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize sentiment pipeline: {str(e)}")
    raise

def preprocess_text(text):
    """Preprocess text by tokenizing and removing stopwords/punctuation."""
    try:
        tokens = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english') + list(string.punctuation))
        tokens = [token for token in tokens if token not in stop_words]
        return ' '.join(tokens)
    except Exception as e:
        logger.error(f"Text preprocessing failed: {str(e)}")
        raise

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    """Analyze sentiment of input text."""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            logger.warning("Invalid request: No text provided")
            return jsonify({'error': 'No text provided'}), 400

        text = data['text']
        if not isinstance(text, str) or not text.strip():
            logger.warning("Invalid request: Text is empty or not a string")
            return jsonify({'error': 'Text must be a non-empty string'}), 400

        processed_text = preprocess_text(text)
        result = sentiment_analyzer(processed_text)

        sentiment = result[0]['label']
        confidence = result[0]['score']

        logger.info(f"Sentiment analysis completed for text: {text[:50]}...")
        return jsonify({
            'text': text,
            'processed_text': processed_text,
            'sentiment': sentiment,
            'confidence': round(confidence, 4)
        })

    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint."""
    logger.info("Health check endpoint accessed")
    return jsonify({'status': 'API is running'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv('FLASK_ENV', 'production') == 'development',
        threaded=True
    )