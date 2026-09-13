import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from google import genai

from chatbot_config import SYSTEM_PROMPT

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=API_KEY)


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    try:
        prompt = f"{SYSTEM_PROMPT}\n\nUser question:\n{message}"

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
        )

        answer = (response.text or "").strip()

        if not answer:
            answer = "I couldn't generate a response. Please try again."

        return jsonify({"answer": answer})

    except Exception:
        return jsonify({
            "error": "Unable to connect to the AI service right now. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
