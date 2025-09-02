import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
CUELINKS_TOKEN = os.getenv("CUELINKS_TOKEN")

# Function to fetch top deals from Cuelinks
def fetch_deals():
    headers = {"Authorization": f"Bearer {CUELINKS_TOKEN}"}
    try:
        url = "https://api.cuelinks.com/v2/campaigns.json"
        params = {
            "sort_column": "id",
            "sort_direction": "asc",
            "page": 1,
            "per_page": 10,
            "search_term": "",
            "country_id": 1
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        deals = []
        for item in data.get("campaigns", []):
            deals.append({
                "title": item.get("name"),
                "affiliate_link": item.get("url"),
                "image_url": item.get("image_url")
            })
        return deals
    except Exception as e:
        print("Error fetching deals:", e)
        return []

# Function to post deals to Telegram
def post_to_telegram(deals):
    for deal in deals:
        try:
            if deal["image_url"]:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
                data = {
                    "chat_id": CHANNEL_ID,
                    "photo": deal["image_url"],
                    "caption": f"{deal['title']}\n{deal['affiliate_link']}"
                }
                resp = requests.post(url, data=data)
            else:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                data = {"chat_id": CHANNEL_ID, "text": f"{deal['title']}\n{deal['affiliate_link']}"}
                resp = requests.post(url, data=data)
            print(resp.json())
        except Exception as e:
            print("Telegram post failed:", e)

if __name__ == "__main__":
    deals = fetch_deals()
    if deals:
        post_to_telegram(deals)
    else:
        print("No deals to post")
        
