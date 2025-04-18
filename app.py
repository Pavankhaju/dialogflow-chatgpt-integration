from flask import Flask, request, jsonify
import openai

app = Flask(_name_)

# OpenAI API Key
openai.api_key = "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"

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

if _name_ == "_main_":
    app.run(debug=True, port=5000)