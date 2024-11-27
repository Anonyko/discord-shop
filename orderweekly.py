import requests
import json
from datetime import datetime
import base64
def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)
def generate_order_ids(json_file, user_id, count):
    try:
        with open(json_file, "r") as file:
            order_data = json.load(file)
    except FileNotFoundError:
        order_data = []
    today = datetime.now().strftime("%d%m%y")
    existing_numbers = [
        int(entry["order_id"][-4:]) for entry in order_data if entry["order_id"].startswith(f"TRXM{today}")
    ]
    next_number = max(existing_numbers, default=0) + 1
    new_orders = []
    for _ in range(count):
        order_id = f"TRXM{today}{next_number:04d}"
        new_order = {
            "order_id": order_id,
            "user_id": user_id
        }
        new_orders.append(new_order)
        order_data.append(new_order)
        next_number += 1
    with open(json_file, "w") as file:
        json.dump(order_data, file, indent=4)
    return [order["order_id"] for order in new_orders]

def send_transactions(order_ids):
    config = load_config()
    server_key = config['server-key']
    server_key_base64 = base64.b64encode(server_key.encode()).decode('utf-8')

    url = "https://app.sandbox.midtrans.com/snap/v1/transactions"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Basic {server_key_base64}"
    }
    responses = []

    for order_id in order_ids:
        payload = {
            "transaction_details": {
                "order_id": order_id,
                "gross_amount": 20000
            },
            "credit_card": {"secure": True}
        }
        response = requests.post(url, json=payload, headers=headers)
        responses.append(response.text)

    return responses
