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
    print("Response Status Code:", response.status_code)
    print("Response JSON main_articles:")
    print(response.json().get("list", []))
    #######################################
    articles_list = response.json().get("list", [])
    
    ID_list = []

   # for i in range(len(articles_list)):  # Iterate over the indices
    #    temp_art = articles_list[i]  # Get the dictionary
    #    print("Article:", temp_art)  # Debugging print
     #   temp_ID = temp_art.get("Id")  # Extract "Id"
     #   ID_list.append(temp_ID)  # Append instead of assigning
    
     #   print("Updated ID List:", ID_list)  # Debugging print
        #response.json().get("list", [])
    return articles_list # ,ID_list #response.json().get("list", [])  # Assuming "data" contains the records

def get_languages():
    """Fetch available languages from the Languages table."""
    print("IM in languages def")
    url = f"{NOCO_BASE_URL}/tables/{LANGUAGES_TABLE}/records"
    response = requests.get(url, headers=HEADERS)
    print("Response JSON languages:")
    print(response.json())
    return [lang["Language Code"] for lang in response.json().get("list", [])]  # Assuming 'code' is the language identifier

def create_translation_records(article_serial):
    """Create translation records for each language."""
    print("IM in create translations def")
    languages = get_languages()
    print("languages list:")
    print(languages)
    for lang in languages:
        payload = {
        #    "Main Article": article_serial,  # Linking to the main article
        #    "Language Code": lang,  # Assigning language
            "Priority": "Low"
        }
        print("test lang and serial:" , lang, article_serial)
        print(payload)
        print(type(payload))
        
        url = f"{NOCO_BASE_URL}/tables/{TRANSLATIONS_TABLE}/records"
        requests.post(url, headers=HEADERS, json=payload)

def update_main_article(article_serial, updates):
    """Update the main article's status."""
    print("IM in update_main_article def")
 #   temp_ID = temp_art.get("Id")  # Extract "Id"
    url = f"{NOCO_BASE_URL}/tables/{MAIN_ARTICLES_TABLE}/records"#/{article_serial}"
    update_payload = {
       "Id": article_serial,
       updates
    }
    print(update_payload)
    print(article_serial)
    requests.patch(url, headers=HEADERS, json=update_payload)

def process_articles():
    """Main function to process articles needing translation."""
    articles = get_main_articles()
    print("finished get main articles")
    print(articles)
    print(f"Articles after function call: {len(articles)}")
  
    for article in articles:
        print("main loop check")
        print("Article Data:", article)
        print("article serial:", article["Serial #"])
        print(len(articles))
        print(article)
        create_translation_records(article["Serial #"])  # Use the 'id' field from the main article
        update_main_article(article["Id"], {"translations_record_status": "Translations records created"})
        
# Run the script
process_articles()
