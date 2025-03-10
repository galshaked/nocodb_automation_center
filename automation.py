import os
import requests

# NocoDB API details
NOCODB_API_URL = os.getenv("https://app.nocodb.com/api/v2")
NOCODB_API_TOKEN = os.getenv("pRns3hnE7P-gPXqDg79rzLDwm6gSqPoBifQJv8eN")

HEADERS = {
    "xc-auth": NOCODB_API_TOKEN,
    "Content-Type": "application/json"
}

def get_languages():
    """Fetch all available languages from the Languages table."""
    url = f"{NOCODB_API_URL}/Languages"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("list", [])
    return []

def create_translation_entries(main_article_id):
    """Create a translation entry for each language."""
    languages = get_languages()
    for language in languages:
        language_code = language["Language Code"]  # Adjust based on your field name
        payload = {
            "Main Article": main_article_id,  # Linking to the newly created article
            "Language Code": language_code
        }
        url = f"{NOCODB_API_URL}/Article Translations"
        response = requests.post(url, json=payload, headers=HEADERS)
        if response.status_code == 200:
            print(f"Translation entry created for {language_code}")
        else:
            print(f"Failed to create entry for {language_code}: {response.text}")

def main():
    """Fetch event data from GitHub and process it."""
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path:
        print("No event data found.")
        return

    with open(event_path, "r") as f:
        event_data = json.load(f)

    main_article_id = event_data["client_payload"]["main_article_id"]
    create_translation_entries(main_article_id)

if __name__ == "__main__":
    main()
