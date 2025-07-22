from flask import Flask, request, jsonify
import jwt
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
SECRET_KEY = os.getenv("SECRET_KEY")
POSTGRES_URL = os.getenv("POSTGRES_URL")

def get_db_connection():
    return psycopg2.connect(POSTGRES_URL)

def verify_token(token):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True
    except jwt.InvalidTokenError:
        return False

@app.route("/store", methods=["POST"])
def store():
    token = request.headers.get("Authorization")
    if not token or not verify_token(token.split(" ")[1]):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    user_id, text, sentiment = data["user_id"], data["text"], data["sentiment"]
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO results (user_id, text, sentiment) VALUES (%s, %s, %s)",
                (user_id, text, sentiment))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "stored"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)