from flask import Flask, request, jsonify
import os
from prompts import format_prompt
from klaviyo import fetch_klaviyo_data
import openai
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

app = Flask(__name__)

slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

client = WebClient(token=slack_bot_token)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    if "event" in data:
        event = data["event"]
        if event.get("type") == "app_mention":
            user = event.get("user")
            channel = event.get("channel")
            text = event.get("text")

            # Use Klaviyo and OpenAI to generate a response
            klaviyo_data = fetch_klaviyo_data()
            prompt = format_prompt(text, klaviyo_data)

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )

            reply = response["choices"][0]["message"]["content"]

            try:
                client.chat_postMessage(channel=channel, text=reply)
            except SlackApiError as e:
                print(f"Slack error: {e.response['error']}")

    return "", 200
