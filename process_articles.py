import requests

# NocoDB API details
NOCO_BASE_URL = "https://app.nocodb.com/api/v2"  # Replace with your NocoDB instance and table ID
API_KEY = "OXUxBBtiQQZDELL51Hg2p6zlqrs_KUIRGze21z-w"  # Replace with your API token
MAIN_ARTICLES_TABLE = "m3ocvzfbhk8ahk1"
TRANSLATIONS_TABLE = "mr422qhi3kt0r4h"
LANGUAGES_TABLE = "mhuq2qb2ur6vkgn"



HEADERS = {
    "xc-token": API_KEY,
    "Content-Type": "application/json"
}

def get_main_articles():
    """Fetch main articles where translations should be created."""
    querystring = {
        "offset": "0",
        "limit": "25",
        "where": "(translations_record_status,eq,Create translations records)",
    }
    url = f"{NOCO_BASE_URL}/tables/{MAIN_ARTICLES_TABLE}/records"
    response = requests.get(url, headers=HEADERS, params=querystring)
    print("Response JSON main_articles:")
    print(response.json())
    return response.json().get("data", [])  # Assuming "data" contains the records

def get_languages():
    """Fetch available languages from the Languages table."""
    url = f"{NOCO_BASE_URL}/tables/{LANGUAGES_TABLE}/records"
    response = requests.get(url, headers=HEADERS)
    print("Response JSON languages:")
    print(response.json())
    return [lang["Language Code"] for lang in response.json().get("data", [])]  # Assuming 'code' is the language identifier

def create_translation_records(article_serial):
    """Create translation records for each language."""
    languages = get_languages()
    print("languages list:")
    print(languages)
    for lang in languages:
        payload = {
            "Main Article": article_serial,  # Linking to the main article
            "Language Code": lang,  # Assigning language
        }
        url = f"{NOCO_BASE_URL}/tables/{TRANSLATIONS_TABLE}/records"
        requests.post(url, headers=HEADERS, json=payload)

def update_main_article(article_serial, updates):
    """Update the main article's status."""
    url = f"{NOCO_BASE_URL}/tables/{MAIN_ARTICLES_TABLE}/records/{article_serial}"
    update_payload = {
        "data": updates
    }
    requests.patch(url, headers=HEADERS, json=update_payload)

def process_articles():
    """Main function to process articles needing translation."""
    articles = get_main_articles()
    for article in articles:
        print("main loop check")
        create_translation_records(article["Serial #"])  # Use the 'id' field from the main article
        update_main_article(article["Serial #"], {"translations_record_status": "Translations records created"})

# Run the script
process_articles()
