import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
CUELINKS_TOKEN = os.getenv("CUELINKS_TOKEN")

# Function to fetch top deals from Cuelinks
def fetch_deals():
    headers = {"Authorization": f"Bearer {CUELINKS_TOKEN}"}
    categories = ["Shopping", "Grocery", "Food", "Rides", "Insurance", "Medical", "Flights/Hotels"]
    all_deals = []

    for category in categories:
        try:
            url = f"https://api.cuelinks.com/v2/campaigns.json"
            params = {
                "sort_column": "id",
                "sort_direction": "asc",
                "page": 1,
                "per_page": 5,
                "search_term": category,
                "country_id": 1
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
        
