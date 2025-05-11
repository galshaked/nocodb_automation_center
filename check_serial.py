import requests
import re

# Constants
NOCO_BASE_URL = "https://app.nocodb.com/api/v2"
API_KEY = "OXUxBBtiQQZDELL51Hg2p6zlqrs_KUIRGze21z-w"
ARTICLES_TABLE = "m3ocvzfbhk8ahk1"  # Main Articles table
SERIAL_CONTROL_TABLE = "mt51tlpooytmoro"  

HEADERS = {
    "xc-token": API_KEY,
    "Content-Type": "application/json"
}

def get_existing_serials(product):
    """Fetch all serials starting with a given product prefix."""
    url = f"{NOCO_BASE_URL}/tables/{ARTICLES_TABLE}/records?limit=1000"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    records = response.json().get("list", [])
    return [r.get("serial_number", "") for r in records if r.get("serial_number", "").startswith(f"{product}-")]

def suggest_next_serial(existing_serials, product):
    numbers = [
        int(re.search(rf"{product}-(\d+)", s).group(1))
        for s in existing_serials if re.match(rf"{product}-\d+$", s)
    ]
    next_num = max(numbers) + 1 if numbers else 1
    return f"{product}-{next_num:03d}"

def update_serial_control(row_id, next_serial):
    url = f"{NOCO_BASE_URL}/tables/{SERIAL_CONTROL_TABLE}/records"
    payload = {
        "Id": row_id,
        "Next available serial #": next_serial
    }
    requests.patch(url, headers=HEADERS, json=payload)

def handler(request_body):
    row_id = request_body["Id"]
    product = request_body["Product"]
    existing = get_existing_serials(product)
    next_serial = suggest_next_serial(existing, product)
    update_serial_control(row_id, next_serial)
