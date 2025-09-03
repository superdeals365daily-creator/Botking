import os
import requests

# Load secrets (GitHub ya .env se)
CUELINKS_API_KEY = os.getenv("CUELINKS_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# 🔑 Step 1: Convert normal URL into affiliate tracking link
def convert_to_affiliate(url):
    api_url = "https://api.cuelinks.com/v2/tools/link-kit.json"
    headers = {"Authorization": f"Token token={CUELINKS_API_KEY}"}
    payload = {"url": url}
    try:
        r = requests.post(api_url, headers=headers, data=payload, timeout=10)
        if r.status_code == 200:
            return r.json().get("tracking_url", url)
        else:
            print("❌ Affiliate conversion failed:", r.text)
            return url
    except Exception as e:
        print("⚠️ Error converting affiliate link:", e)
        return url

# 🔑 Step 2: Fetch top campaigns / offers from Cuelinks
def fetch_deals():
    url = "https://api.cuelinks.com/v2/campaigns.json"
    headers = {"Authorization": f"Token token={CUELINKS_API_KEY}"}
    params = {"per_page": 5, "country_id": 1, "page": 1}  # top 5 deals
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        r.raise_for_status()
        return r.json().get("campaigns", [])
    except Exception as e:
        print("❌ Error fetching deals:", e)
        return []

# 🔑 Step 3: Post to Telegram channel
def post_to_telegram(title, description, link, logo=None):
    caption = f"""🔥 {title}
{description[:120]}...

👉 [Grab Deal Here]({link})"""

    if logo:
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        payload = {
            "chat_id": TELEGRAM_CHANNEL_ID,
            "photo": logo,
            "caption": caption,
            "parse_mode": "Markdown"
        }
    else:
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHANNEL_ID,
            "text": caption,
            "parse_mode": "Markdown"
        }

    resp = requests.post(telegram_url, data=payload)
    if resp.status_code == 200:
        print(f"✅ Posted: {title}")
    else:
        print("❌ Telegram Error:", resp.text)

# 🔑 Step 4: Main workflow
def main():
    deals = fetch_deals()
    if not deals:
        print("⚠️ No deals found.")
        return

    for d in deals:
        title = d.get("name", "No Title")
        description = d.get("description", "No description available.")
        raw_url = d.get("tracking_url") or d.get("url", "")
        affiliate_url = convert_to_affiliate(raw_url)
        logo = d.get("logo", "")

        post_to_telegram(title, description, affiliate_url, logo)

if __name__ == "__main__":
    main()
    
