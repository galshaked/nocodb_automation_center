import requests

# NocoDB API details
NOCO_BASE_URL = "https://app.nocodb.com/api/v2"  
API_KEY = "OXUxBBtiQQZDELL51Hg2p6zlqrs_KUIRGze21z-w"  # NocoDB API token
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
    
    articles_list = response.json().get("list", [])
    return articles_list

def get_languages():
    """Fetch available languages from the Languages table."""
    url = f"{NOCO_BASE_URL}/tables/{LANGUAGES_TABLE}/records"
    response = requests.get(url, headers=HEADERS)
    return [{"Id": lang["Id"], "Code": lang["Language Code"]} for lang in response.json().get("list", [])]

def create_translation_records(article_Id):
    """Create translation records for each language."""
    main_id = article_Id
    languages = get_languages()
    for lang in languages:
        new_record_id = create_new_record()
        lang_id = lang["Id"]
        link_lang(new_record_id,lang_id)
        link_main_art(new_record_id,main_id)
        

def create_new_record():
    payload = {
            "creation_status": "WIP"
        }       
    url = f"{NOCO_BASE_URL}/tables/{TRANSLATIONS_TABLE}/records"
    requests.post(url, headers=HEADERS, json=payload) # create the record
    get_url = f"{NOCO_BASE_URL}/tables/{TRANSLATIONS_TABLE}/records?where=(creation_status,eq,WIP)"
    response = requests.get(get_url,headers=HEADERS) # get the new record
    new_record = response.json().get("list", [])
    new_record_id = new_record[0]["Id"]
    update_payload = {
        "Id": new_record_id,
        "creation_status": "Done"
    }
    requests.patch(url, headers=HEADERS, json=update_payload) # update the record creation status to Done

    return new_record_id

def link_lang(trans_id,lang_id):
    linked_field = "cw39fr3ddjgovdc"
    url = f"{NOCO_BASE_URL}/tables/{TRANSLATIONS_TABLE}/Links/{linked_field}/records/{trans_id}"
    payload = {
        "Id": lang_id
    }
    requests.post(url, headers=HEADERS, json=payload)


def link_main_art(trans_id,art_id):
    linked_field = "c0rov9w5fwaiu76"
    url = f"{NOCO_BASE_URL}/tables/{TRANSLATIONS_TABLE}/Links/{linked_field}/records/{trans_id}"
    payload = {
        "Id": art_id
    }
    requests.post(url, headers=HEADERS, json=payload)

def update_main_article(article_id):
    """Update the main article's status."""
    url = f"{NOCO_BASE_URL}/tables/{MAIN_ARTICLES_TABLE}/records"
    update_payload = {
       "Id": article_id,
       "translations_record_status": "Translations records created"
    }
    print(update_payload)
    print(article_id)
    requests.patch(url, headers=HEADERS, json=update_payload)

def process_articles():
    """Main function to process articles needing translation."""
    articles = get_main_articles()
  
    for article in articles:
        create_translation_records(article["Id"])  # Use the 'id' field from the main article
        update_main_article(article["Id"])#, {"translations_record_status": "Translations records created"})
        
# Run the script
process_articles()
