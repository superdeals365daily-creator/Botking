import os
import requests

# Secrets
CUELINKS_API_KEY = os.getenv("CUELINKS_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

def fetch_deals():
    url = "https://api.cuelinks.com/v2/campaigns.json"
    headers = {"Authorization": f"Token token={CUELINKS_API_KEY}"}
    params = {"country_id": 1, "per_page": 5, "page": 1}
    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    return r.json()["campaigns"]

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHANNEL_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=payload)

def main():
    deals = fetch_deals()
    for d in deals:
        title = d.get("name", "Deal")
        url = d.get("tracking_link", "#")
        payout = d.get("payout", "N/A")
        message = f"🔥 <b>{title}</b>\n💰 Payout: {payout}\n🔗 <a href='{url}'>Grab Deal</a>"
        send_to_telegram(message)

if __name__ == "__main__":
    main()
    
