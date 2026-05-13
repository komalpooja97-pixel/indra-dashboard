from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

GEMINI_KEY = "AIzaSyArerEKZXATmXMGKHkUzMcVZntgsjjnKAE"
GEMINI_MODEL = "gemini-2.0-flash"

SETTLEMENT_CONTEXT = """Real settlement data Feb 10-12 2024. 30 rows. 7 anomalies:
1.CRITICAL RULE1 Feb11 06:00 Energy DAM expected $13,000 actual $450,000
2.CRITICAL RULE1 Feb11 07:00 Energy RTM expected $14,000 actual $495,000
3.CRITICAL RULE1 Feb11 08:00 Energy RTM expected $15,000 actual $540,000
4.WARNING RULE3 Feb11 09:00 Uplift DAM expected $8,000 actual $42,000
5.WARNING RULE3 Feb11 10:00 Uplift RTM expected $7,500 actual $38,500
6.WARNING RULE5 Feb11 13:00 Ancillary DAM expected $3,100 actual $0
7.WARNING RULE4 Feb11 14:00 REC Credit DAM expected -$4,500 actual $0
Total exposure $1,522,500. Annual $18,270,000."""

AGENTS = {
    "settlement": "You are Settlement Analysis Agent A1. Analyse settlement data. Be concise.",
    "financial": "You are Financial Impact Agent A2. Calculate exposure and projections. Be concise.",
    "compliance": "You are Compliance Agent A3. Validate NERC/FERC rules. Be concise.",
    "nlp": "You are NLP Agent A4. Explain in plain English for CFO. No jargon.",
    "dispute": "You are Dispute Agent A5. Draft dispute letters with dates and amounts."
}

def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1200}}
    response = requests.post(url, json=payload)
    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

@app.route("/analyse", methods=["POST"])
def analyse():
    try:
        body = request.get_json()
        message = body.get("message", "")
        agent = body.get("agent", "settlement")
        prompt = f"{AGENTS.get(agent)}\n\nDATA:\n{SETTLEMENT_CONTEXT}\n\nQUESTION: {message}"
        response_text = call_gemini(prompt)
        return jsonify({"success": True, "response": response_text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "INDRA Backend Running", "port": 5000})

if __name__ == "__main__":
    print("INDRA Flask Backend Starting on http://localhost:5000")
    app.run(debug=True, port=5000)