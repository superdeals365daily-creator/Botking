import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
CUELINKS_API_TOKEN = os.getenv("CUELINKS_TOKEN")  # Real API token

# Categories you want to fetch deals for
CATEGORIES = [
    "Shopping", "Grocery", "Food", "Rides", 
    "Insurance", "Medical", "Flights/Hotels"
]

def fetch_deals():
    headers = {"Authorization": f"Bearer {CUELINKS_API_TOKEN}"}
    all_deals = []

    for category in CATEGORIES:
        try:
            # Example real API endpoint (update according to Cuelinks API docs)
            url = "https://api.cuelinks.com/v2/campaigns.json"
            params = {
                "search_term": category,
                "page": 1,
                "per_page": 5,
                "country_id": 1,
                "sort_column": "id",
                "sort_direction": "asc"
            }
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            for item in data.get("campaigns", []):
                deal = {
                    "title": item.get("name"),
                    "affiliate_link": item.get("url"),
                    "image_url": item.get("image_url")
                }
                all_deals.append(deal)
        except Exception as e:
            print(f"Error fetching {category} deals:", e)

    return all_deals

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
        
