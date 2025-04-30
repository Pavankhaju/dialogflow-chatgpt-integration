from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# OpenAI API Key
openai.api_key= "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"
# Health check / root route
@app.route("/", methods=["GET"])
def health_check():
    return "OK", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(silent=True, force=True)
    
    # User message from Dialogflow
    user_message = req.get("queryResult").get("queryText")
    
    # Call OpenAI ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Free tier
        messages=[
            {"role": "system", "content": "You are an emotional support assistant. Reply with empathy, kindness, and calm tone."},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7
    )

    reply_text = response["choices"][0]["message"]["content"]

    # Send response back to Dialogflow
    return jsonify({"fulfillmentText": reply_text})

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=8000)
