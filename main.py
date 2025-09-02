import os
import requests

# Read secrets from environment (GitHub Actions)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
CUELINKS_TOKEN = os.getenv("CUELINKS_TOKEN")

# Function to fetch deals from Cuelinks (dummy example, replace with real API call)
def fetch_deals():
    # Example hardcoded deals for testing
    return [
        "🔥 Zepto: 20% off on first order",
        "🍕 Domino's: Buy 1 Get 1 Free",
        "🏨 OYO: Up to 50% discount",
    ]

# Function to post deals to Telegram
def post_to_telegram(deals):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    for deal in deals:
        data = {"chat_id": CHANNEL_ID, "text": deal}
        try:
            resp = requests.post(url, data=data)
            print(resp.json())
        except Exception as e:
            print("Telegram post failed:", e)

if __name__ == "__main__":
    print("BOT_TOKEN:", BOT_TOKEN)
    print("CHANNEL_ID:", CHANNEL_ID)
    deals = fetch_deals()
    if deals:
        post_to_telegram(deals)
    else:
        print("No deals fetched")
        
