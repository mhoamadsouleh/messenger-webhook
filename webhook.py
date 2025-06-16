from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = 'Nactivi2025'
PAGE_ACCESS_TOKEN = 'EAARRlvmJ1MMBO9oE2UOOwm6l7wwk9RGKrZBR0yu8jwVt2z286BLM5IeoFwENUWNcUazzGhiDUlOPpmEEJtKTTLXZBqyEbKSR72eNcyvzdrGWZAzYOGBHE8ZAMcE00F1vkKWXPatzhcak3zaYn9yHtvt6MijjMpdNkfxNwFnbM29FbnZAOvjx2f4ZCIhoLuEoSulEdDigZDZD'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode and token:
            if token == VERIFY_TOKEN:
                return challenge, 200
            else:
                return 'Unauthorized', 403

    elif request.method == 'POST':
        data = request.get_json()
        if data.get('object') == 'page':
            for entry in data.get('entry', []):
                for messaging_event in entry.get('messaging', []):
                    sender_id = messaging_event['sender']['id']
                    if 'message' in messaging_event:
                        send_message(sender_id, "✅ تم استلام رسالتك بنجاح.")
        return 'EVENT_RECEIVED', 200
    else:
        return 'Not Found', 404

def send_message(recipient_id, message_text):
    payload = {
        'recipient': {'id': recipient_id},
        'message': {'text': message_text}
    }
    headers = {
        'Content-Type': 'application/json'
    }
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    requests.post(url, json=payload, headers=headers)

if __name__ == '__main__':
    app.run(debug=True)
