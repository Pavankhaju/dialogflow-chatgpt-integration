from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# OpenAI API Key
 Openai.api_key= "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"


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
    app.run(debug=True,host="0.0.0.0", port=10000)
