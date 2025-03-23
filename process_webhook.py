import os
import requests
import json

NOCO_API_URL = "http://app.nocodb.com/api/v2"
NOCO_API_TOKEN = os.getenv("OXUxBBtiQQZDELL51Hg2p6zlqrs_KUIRGze21z-w")

HEADERS = {
    "xc-token": "OXUxBBtiQQZDELL51Hg2p6zlqrs_KUIRGze21z-w",
    "Content-Type": "application/json"
}

def get_languages():
    """Fetch all languages from the Languages table."""
    url = f"{NOCO_API_URL}/tables/mhuq2qb2ur6vkgn/records"
    response = requests.get(url, headers=HEADERS)
    return response.json().get("list", [])

def create_translation_records(article_id, languages):
    """Create translation records for each language."""
    for lang in languages:
        data = {
            "Main Article": article_id,
            "Language Code": lang["id"],
        }
        url = f"{NOCO_API_URL}/tables/mr422qhi3kt0r4h/records"
        requests.post(url, headers=HEADERS, json=data)

def main():
    """Main function triggered by webhook."""
    webhook_payload = os.getenv("GITHUB_EVENT_PATH")

    if not webhook_payload:
        print("No webhook payload received")
        return

    with open(webhook_payload, 'r') as f:
        event_data = json.load(f)

    article_id = event_data.get("data", {}).get("Serial #")

    if not article_id:
        print("No article ID found in payload")
        return

    languages = get_languages()
    create_translation_records(article_id, languages)

if __name__ == "__main__":
    main()
