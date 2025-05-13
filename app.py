from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Choose provider: OpenAI or OpenRouter
USE_OPENROUTER = os.getenv("USE_OPENROUTER", "false").lower() == "true"

if USE_OPENROUTER:
    openrouter.api_base = "https://openrouter.ai/api/v1"
    openrouter.api_key = os.getenv("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")
    MODEL = "openrouter/openai/gpt-3.5-turbo"
else:
    openai.api_key = os.getenv("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")
    MODEL = "gpt-3.5-turbo"  # Or gpt-4 if you have access

@app.route("/", methods=["GET"])
def health():
    return "Webhook active", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    user_message = req.get("queryResult", {}).get("queryText", "")

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an emotional support assistant. Reply with empathy, warmth, and understanding."},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7
    )

    reply_text = response["choices"][0]["message"]["content"]

    return jsonify({
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [reply_text]
                }
            }
        ]
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
