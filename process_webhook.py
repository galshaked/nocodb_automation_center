import os
import requests

NOCO_API_URL = os.getenv("app.nocodb.com")
NOCO_API_TOKEN = os.getenv("OXUxBBtiQQZDELL51Hg2p6zlqrs_KUIRGze21z-w")

HEADERS = {
    "xc-token": NOCO_API_TOKEN,
    "Content-Type": "application/json"
}

def get_languages():
    """Fetch all languages from the Languages table."""
    url = f"{NOCO_API_URL}/api/v2/db/data/v2/wozkj4fx/Languages"
    response = requests.get(url, headers=HEADERS)
    return response.json().get("list", [])

def create_translation_records(article_id, languages):
    """Create translation records for each language."""
    for lang in languages:
        data = {
            "MainArticle": article_id,
            "Language": lang["id"]
        }
        url = f"{NOCO_API_URL}/api/v2/db/data/v2/wozkj4fx/Article Translations"
        requests.post(url, headers=HEADERS, json=data)

def main():
    """Main function triggered by webhook."""
    # GitHub Actions will pass the webhook payload as an environment variable
    webhook_payload = os.getenv("GITHUB_EVENT_PATH")

    if not webhook_payload:
        print("No webhook payload received")
        return

    with open(webhook_payload, 'r') as f:
        event_data = json.load(f)

    # Extract the article ID from the webhook payload
    article_id = event_data.get("data", {}).get("Serial #")

    if not article_id:
        print("No article ID found in payload")
        return

    # Fetch languages and create translation records
    languages = get_languages()
    create_translation_records(article_id, languages)

if __name__ == "__main__":
    main()
