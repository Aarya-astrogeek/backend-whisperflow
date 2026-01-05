from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """
You are an AI-native ingredient understanding copilot.
Reduce cognitive load, explain trade-offs, and communicate uncertainty.
Do not list ingredients or act as a database.
"""

@app.route("/chat", methods=["POST"])
def chat():
    messages = request.json["messages"]

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
        json=payload
    )

    return jsonify(res.json()["choices"][0]["message"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
