from flask import Flask, request, jsonify
from flask_cors import CORS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests

app = Flask(__name__)
CORS(app)

API_KEY = "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"  # Replace with your actual key
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
analyzer = SentimentIntensityAnalyzer()

CRISIS_KEYWORDS = ["suicide", "kill myself", "i want to die", "give up", "can't go on", "end it"]

def is_crisis(text):
    return any(word in text.lower() for word in CRISIS_KEYWORDS)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    message = data.get("message", "")
    sentiment = analyzer.polarity_scores(message)
    score = sentiment["compound"]

    if is_crisis(message):
        return jsonify({
            "reply": "⚠️ You're not alone. Please reach out to a trusted professional or helpline immediately.",
            "mood": "Crisis",
            "score": score,
            "crisis": True
        })

    mood = "Positive" if score > 0.5 else "Negative" if score < -0.5 else "Neutral"
    prompt = f"You are a compassionate AI mental health support bot. The user is feeling {mood} and said: '{message}'. Respond in 1-2 kind and supportive sentences."

    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "openai/gpt-4o",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500
        }

        response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
        response.raise_for_status()

        ai_reply = response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("OpenRouter error:", e)
        ai_reply = "Sorry, I'm having trouble responding right now."

    return jsonify({
        "reply": ai_reply,
        "mood": mood,
        "score": score,
        "crisis": False
    })

if __name__ == "__main__":

    app.run(debug=True)
    app.run(host="0.0.0.0", port=3000)
