from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "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"

@app.route("/", methods=["GET"])
def health_check():
    return "OK", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(silent=True, force=True)
    user_message = req.get("queryResult").get("queryText")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an emotional support assistant. Reply with empathy, kindness, and calm tone."},
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
