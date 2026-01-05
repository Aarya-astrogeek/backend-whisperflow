from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)

# ---- CORS (CRITICAL) ----
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)

# ---- Groq Config ----
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """
You are an AI-native ingredient understanding copilot.

Your goal is not to list ingredients or act as a database.
Instead:
- Explain why certain ingredients matter
- Surface trade-offs (health, taste, cost, processing)
- Clearly communicate uncertainty when information is incomplete
- Reduce cognitive load for the user

Prefer reasoning and explanation over factual exhaustiveness.
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
        json=payload,
        timeout=30
    )

    response.raise_for_status()
    result = response.json()

    return jsonify(result["choices"][0]["message"])

# ---- Render-compatible entry ----
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

