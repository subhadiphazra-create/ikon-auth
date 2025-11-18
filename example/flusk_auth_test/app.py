from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

from ikon_auth import verify_token

load_dotenv()  # loads .env variables

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Flask API running successfully 🚀"})

# Protected route
@app.route("/secure")
def secure():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({"error": "Missing Authorization header"}), 401

    try:
        token = auth_header.replace("Bearer ", "")
        
        # Wrap token to mimic FastAPI `credentials` object
        class Cred:
            def __init__(self, token):
                self.credentials = token

        verify_token(Cred(token))

        return jsonify({"message": "Secure data accessed ✔ Token valid"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 401



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
