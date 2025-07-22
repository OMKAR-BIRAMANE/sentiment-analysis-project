from flask import Flask, request, jsonify
from transformers import pipeline
import redis
import jwt
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")

app = Flask(__name__)
redis_client = redis.Redis.from_url(REDIS_URL)
sentiment_pipeline = None

def load_model():
    global sentiment_pipeline
    try:
        sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise

try:
    load_model()
except Exception:
    raise

@app.route("/analyze", methods=["POST"])
def analyze():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid token"}), 401
    token = auth_header.split(" ")[1]
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing text"}), 400
    text = data["text"]
    cached_result = redis_client.get(text)
    if cached_result:
        return jsonify({"sentiment": cached_result.decode(), "score": 0.999})
    try:
        result = sentiment_pipeline(text)[0]
        sentiment = result["label"]
        score = result["score"]
        redis_client.set(text, sentiment, ex=3600)
        return jsonify({"sentiment": sentiment, "score": score})
    except Exception as e:
        return jsonify({"error": str(e)}), 500