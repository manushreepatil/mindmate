from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

CRISIS_KEYWORDS = [
    "suicid", "kill myself", "kill me", "want to die", "end my life",
    "hurt myself", "harm myself", "cut myself", "overdose", "die now",
    "can't go on", "i'm done"
]

def detect_crisis(text):
    t = text.lower()
    return any(k in t for k in CRISIS_KEYWORDS)

def fallback_response(user_text):
    t = user_text.lower()
    if any(word in t for word in ["exam", "final", "failed", "results", "study", "studying", "grades"]):
        return "Exams can be overwhelming. Try a 5-minute focused breathing exercise and plan small study goals. You're not alone."
    if any(word in t for word in ["stressed","stress","anxiety","anxious","panic"]):
        return "I’m sorry you’re feeling stressed — try this: breathe in for 4s, hold for 4s, breathe out for 6s (repeat 3 times). Want more coping tips?"
    if any(word in t for word in ["sad","depressed","low","hopeless"]):
        return "I'm really sorry you're feeling low. It might help to share a little about what happened. If you're feeling unsafe, please consider contacting a local helpline."
    return "Thanks for telling me. I’m here to listen — can you say more about what’s on your mind?"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"ok": False, "reply": "Please type something so I can help."})

    if detect_crisis(user_message):
        return jsonify({
            "ok": True,
            "escalate": True,
            "reply": (
                "I'm really sorry you're feeling this way. If you are in immediate danger, call emergency services at 112 now. "
                "You can also call the Snehi helpline: +91-22-2772-6771 or the local mental health helpline."
            )
        })

    reply_text = fallback_response(user_message)

    return jsonify({"ok": True, "escalate": False, "reply": reply_text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
