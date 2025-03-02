import requests

# 🔹 Replace with your actual NocoDB instance & API token
NOCODB_API_URL = "https://app.nocodb.com/#/wozkj4fx/pcxgyw39qi99zg9/api/v1"
API_TOKEN = "xc-token: fjyPX0Bd-kEhlakJfsqjhYO4n1619rogrx-fwHNS"

# 🔹 Headers for authentication
HEADERS = {
    "xc-auth": API_TOKEN,
    "Content-Type": "application/json"
}

# 🔹 Define your tables
SOURCE_TABLE = "Main Articles"  # Change this to your source table name
TARGET_TABLE = "Article Translations"  # Change this to your target table name

# 🔹 Get all records from the source table
def fetch_records():
    url = f"{NOCODB_API_URL}/tables/{SOURCE_TABLE}/records"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json().get("list", [])
    else:
        print(f"Error fetching records: {response.text}")
        return []

# 🔹 Insert records into the target table
def insert_record(data):
    url = f"{NOCODB_API_URL}/tables/{TARGET_TABLE}/records"
    response = requests.post(url, json={"data": data}, headers=HEADERS)
    
    if response.status_code == 200:
        print("✅ Record added successfully!")
    else:
        print(f"❌ Error adding record: {response.text}")

# 🔹 Run the sync process
def sync_records():
    records = fetch_records()
    for record in records:
        insert_record(record)

if __name__ == "__main__":
    sync_records()
