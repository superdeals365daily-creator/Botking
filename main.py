import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

deals = ["✅ Test message from GitHub workflow"]

def post_to_telegram(deals):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    for deal in deals:
        data = {"chat_id": CHANNEL_ID, "text": deal}
        resp = requests.post(url, data=data)
        print(resp.json())

if __name__ == "__main__":
    post_to_telegram(deals)
    
