from flask import Flask, request, jsonify
import psycopg2
import redis
import jwt

# Hardcoded secret key (replace with a secure value or generate one)
SECRET_KEY = "0fa9b569eb8cb0c04eefac0a09aa2f41f2f1d5f060935852"  # Use your chosen key
POSTGRES_URL = "postgresql://user:password@postgres:5432/auth_db"
REDIS_URL = "redis://redis:6379"

app = Flask(__name__)

try:
    conn = psycopg2.connect(POSTGRES_URL)
    print("Database connection established.")
except psycopg2.Error as e:
    print(f"Database connection failed: {e}")
    raise

redis_client = redis.Redis.from_url(REDIS_URL)

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Missing username or password"}), 400
    username, password = data["username"], data["password"]
    try:
        api_key = jwt.encode({"username": username}, SECRET_KEY, algorithm="HS256")  # No decode needed
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, password, api_key) VALUES (%s, %s, %s) ON CONFLICT (username) DO NOTHING RETURNING id",
                (username, password, api_key)
            )
            result = cur.fetchone()
            conn.commit()
            if result:
                return jsonify({"api_key": api_key, "id": result[0]})
            return jsonify({"error": "Username already exists"}), 409
    except jwt.InvalidKeyError:
        return jsonify({"error": "Invalid secret key"}), 500
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Missing username or password"}), 400
    username, password = data["username"], data["password"]
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT password, api_key FROM users WHERE username = %s", (username,))
            result = cur.fetchone()
            if result and result[0] == password:
                token = jwt.encode({"username": username}, SECRET_KEY, algorithm="HS256")  # No decode needed
                return jsonify({"token": token, "api_key": result[1]})
            return jsonify({"error": "Invalid credentials"}), 401
    except psycopg2.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)