import requests

# NocoDB API details
NOCO_BASE_URL = "https://app.nocodb.com/api/v2"  
API_KEY = "OXUxBBtiQQZDELL51Hg2p6zlqrs_KUIRGze21z-w"  # NocoDB API token
MAIN_ARTICLES_TABLE = "m3ocvzfbhk8ahk1"
SERIAL_CONTROL_TABLE = "mt51tlpooytmoro"

HEADERS = {
    "xc-token": API_KEY,
    "Content-Type": "application/json"
}


def get_existing_serials():
    all_articles = []
    limit = 100
    offset = 0
    url = f"{NOCO_BASE_URL}/tables/{MAIN_ARTICLES_TABLE}/records"
   
    while True:
        response = requests.get(
            url,
            headers=HEADERS,
            params={"limit": limit, "offset": offset, "viewId": "vwzv328131fpcn4o" }
        )
        data = response.json()
        records = data.get("list", [])

        if not records:
            break

        all_articles.extend(records)
        offset += limit

    # Now extract Serial # and Product
    serial_product_list = [
        (record.get("Serial #"), record.get("Product"))
        for record in all_articles
    ]
    print("_______________get existing serials________________")
    print(len(serial_product_list))  # Total number of records retrieved
    print(serial_product_list[:5])  # Preview the first 5
    print("_______________XXXget existing serialsXXX________________")

    return serial_product_list



def get_products():
    url = f"{NOCO_BASE_URL}/tables/{SERIAL_CONTROL_TABLE}/records"
    response = requests.get(url, headers=HEADERS)
    
    products_list = response.json().get("list", [])
    products = [(product.get('Id'), product.get('Product')) for product in products_list]

    return products
"""
def find_next_available(product, all_serials):
    filtered_list = [item for item in all_serials if item[1] == product]

    print("_______________find next available________________")
    print(filtered_list)
    
    # Extract prefix and numbers
    prefix = filtered_list[0][0].split('-')[0]
    numbers = [int(serial.split('-')[1]) for serial, _ in filtered_list]

    # Get next number
    next_number = max(numbers) + 1
    next_serial = f"{prefix}-{next_number:03}"

    print(next_serial)
    print("_______________XXXfind next availableXXX________________")
    return next_serial
"""

def find_next_available(product, all_serials):
    # Filter the list based on the product
    filtered_list = [item for item in all_serials if item[1] == product]

    print("_______________find next available________________")
    print(filtered_list)
    print(len(filtered_list))
    
    # Extract prefix and numbers
    prefix = filtered_list[0][0].split('-')[0]
    numbers = [int(serial.split('-')[1]) for serial, _ in filtered_list]

    # Sort the numbers to detect any gaps
    numbers.sort()

    # Get the first missing number in the sequence
    next_number = 1
    for number in numbers:
        if number != next_number:
            break
        next_number += 1

    # Generate the next serial number
    next_serial = f"{prefix}-{next_number:03}"

    print(next_serial)
    print("_______________XXXfind next availableXXX________________")
    return next_serial


def update_next_avaible(product_id,next_serial):
    """Update the serial # control next availble."""
    url = f"{NOCO_BASE_URL}/tables/{SERIAL_CONTROL_TABLE}/records"
    update_payload = {
       "Id": product_id,
       "Next available serial #": next_serial
    }
    print(update_payload)
    requests.patch(url, headers=HEADERS, json=update_payload)



def main():
    
    all_serials = get_existing_serials() #get all existing serail numbers from main table
    products = get_products()

    for product in products:
        print(product)
        product_name = product[1]
        product_id = product[0]
        next_serial = find_next_available(product_name, all_serials)
        print(product_id," -> ",next_serial)
        update_next_avaible(product_id,next_serial)


main()