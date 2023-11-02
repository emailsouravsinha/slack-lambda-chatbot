import os
import json
import requests

def lambda_handler(event, context):
    # Verify the request is from Slack
    print("Got to point 1")
    event = json.loads(event["body"])
    print(event)
    if "token" in event and event["token"] == "nqAWS3Ic1EPjWZT7UkUJ3II1":
        if "type" in event and event["type"] == "url_verification":
            # Slack event subscription verification
            return {
                'statusCode': 200,
                'body': event['challenge']
            }

        # Handle messages from Slack
        if "event" in event and "type" in event["event"] and "client_msg_id" in event["event"] and event["event"]["type"] == "message":
            print("Got to point 2")
            # Extract the necessary information from the event
            user_id = event["event"]["user"]
            channel = event["event"]["channel"]
            text = event["event"]["text"]
            print(event)
            # Process the message (you can perform your logic here)
            response_text = f"You said: '{text}'. Thanks for your message!"

            # Post the response back to the channel
            post_message(channel, response_text)
    print("Token verification is failing")
    return {
        'statusCode': 200,
        'body': "Message received"
    }

def post_message(channel, text):
    SLACK_TOKEN = os.environ["BOT_TOKEN"]

    headers = {
        'Content-type': 'application/json',
        'Authorization': f"Bearer {SLACK_TOKEN}"
    }

    data = {
        'channel': channel,
        'text': text
    }

    # Make a POST request to Slack's chat.postMessage API
    response = requests.post('https://slack.com/api/chat.postMessage', headers=headers, data=json.dumps(data))

    if response.status_code != 200:
        print("Failed to post message to Slack")
