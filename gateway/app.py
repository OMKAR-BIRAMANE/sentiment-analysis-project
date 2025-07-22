from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/auth/<path:path>", methods=["POST"])
def auth_proxy(path):
    return requests.post(f"http://auth-service:8000/{path}", json=request.get_json()).json()

@app.route("/analyze/<path:path>", methods=["POST"])
def analysis_proxy(path):
    return requests.post(f"http://analysis-service:8000/{path}", json=request.get_json(), headers=request.headers).json()

@app.route("/store/<path:path>", methods=["POST"])
def storage_proxy(path):
    return requests.post(f"http://storage-service:8000/{path}", json=request.get_json(), headers=request.headers).json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)