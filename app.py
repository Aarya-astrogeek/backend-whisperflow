from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)  # VERY IMPORTANT for Vercel → Render

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """
You are an AI-native ingredient understanding copilot.
Reduce cognitive load.
Explain trade-offs.
Communicate uncertainty.
Do NOT list ingredients.
Do NOT act as a database.
"""

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            *messages
        ],
        "temperature": 0.4
    }

    response = requests.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload
    )

    result = response.json()
    return jsonify(result["choices"][0]["message"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


