from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """
You are an AI-native ingredient understanding copilot.
Reduce cognitive load, explain trade-offs, and communicate uncertainty.
Do not list ingredients or act as a database.
"""

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        messages = data.get("messages", [])

        if not GROQ_API_KEY:
            return jsonify({"error": "GROQ_API_KEY not set"}), 500

        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages
            ],
            "temperature": 0.4
        }

        res = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=60
        )

        return jsonify(res.json()["choices"][0]["message"])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)



