import requests

# 🔹 Replace with your actual NocoDB instance & API token
NOCODB_API_URL = "https://app.nocodb.com/api/v2/db/data/v2"
API_TOKEN = "pRns3hnE7P-gPXqDg79rzLDwm6gSqPoBifQJv8eN"

# 🔹 Headers for authentication
HEADERS = {
    "xc-auth": API_TOKEN,
    "Content-Type": "application/json"
}

# 🔹 Define tables
SOURCE_TABLE = "Main_Articles"      # Articles table
TARGET_TABLE = "Article_Translations"  # Translations table
LANGUAGE_TABLE = "Languages"       # Supported languages table

# 🔹 Fetch all records from a given table
def fetch_records(table_name):
    url = f"{NOCODB_API_URL}/{table_name}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json().get("list", [])
    else:
        print(f"❌ Error fetching {table_name} records: {response.text}")
        return []

# 🔹 Fetch existing translations for an article (to avoid duplicates)
def fetch_existing_translations(article_id):
    url = f"{NOCODB_API_URL}/{TARGET_TABLE}?where=(Main article,eq,{article_id})"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return {record["Language code"] for record in response.json().get("list", [])}
    else:
        print(f"⚠️ Error fetching existing translations: {response.text}")
        return set()

# 🔹 Insert a new translation record
def insert_record(data):
    url = f"{NOCODB_API_URL}/{TARGET_TABLE}"
    response = requests.post(url, json={"data": data}, headers=HEADERS)
    
    if response.status_code == 200:
        print(f"✅ Translation added: {data}")
    else:
        print(f"❌ Error adding translation: {response.text}")

# 🔹 Main sync function
def sync_records():
    articles = fetch_records(SOURCE_TABLE)  # Step 1: Fetch new articles
    languages = fetch_records(LANGUAGE_TABLE)  # Step 2: Fetch supported languages

    # Extract language codes
    language_codes = {lang["Language code"] for lang in languages}

    for article in articles:
        if article.get("Create translations", False):  # Only process if checkbox is checked
            article_id = article["id"]
            existing_languages = fetch_existing_translations(article_id)

            for lang_code in language_codes:
                if lang_code not in existing_languages:
                    translation_data = {
                        "Main article": article_id,  # Link to the main article
                        "Language code": lang_code,
                        "Title": f"{article['Title']} ({lang_code})",
                        "Content": "",  # Empty content for translations to be filled later
                    }
                    insert_record(translation_data)

if __name__ == "__main__":
    sync_records()
