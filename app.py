from flask import Flask, request, jsonify
form requests
import openai
import os
from dotenv import load_dotenv
load_dotenv()

# OpenRouter config
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

app = Flask(__name__)

@app.route("/", methods=["get"])
def health_check():
    return "OK", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    user_message = req["queryResult"]["queryText"]

    response = openai.ChatCompletion.create(
        model="mistralai/mistral-7b-instruct",
        messages=[
            {"role": "system", "content": "You are an emotional support chatbot. Talk in a caring, empathetic way."},
            {"role": "user", "content": user_message}
        ],
        temperature=0.8
    )

    reply_text = response["choices"][0]["message"]["content"]
    return jsonify({"fulfillmentText": reply_text})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
