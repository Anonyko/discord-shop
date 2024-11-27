import requests
import json

def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

def check_transaction_status(transaction_id, user_id):
    config = load_config()
    server_key = config['server-key']
    server_key_base64 = base64.b64encode(server_key.encode()).decode('utf-8')
    # Determine the keylist and order log files based on the transaction ID prefix
    if transaction_id.startswith("TRXW"):
        keylist_file = "keylistw.json"
        order_log_file = "order_idsw.json"
    elif transaction_id.startswith("TRXM"):
        keylist_file = "keylistm.json"
        order_log_file = "order_idsm.json"
    else:
        return "Invalid transaction ID format. Must start with TRXW or TRXM."

    # API URL to fetch transaction status
    url = f"https://api.sandbox.midtrans.com/v2/{transaction_id}/status"

    headers = {
        "accept": "application/json",
        "authorization": f"Basic {server_key_base64}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return f"Failed to fetch transaction status. Error: {response.status_code} - {response.text}"

    try:
        transaction_data = response.json()
        transaction_status = transaction_data.get("transaction_status", "unknown")

        # Load the transaction log to check if the ID already exists
        log_file = "transaction_log.json"
        try:
            with open(log_file, "r") as file:
                transaction_log = json.load(file)
        except FileNotFoundError:
            transaction_log = []

        if any(log["transaction_id"] == transaction_id for log in transaction_log):
            return "Key already redeemed"

        # Check if the transaction ID is associated with the given user ID
        try:
            with open(order_log_file, "r") as file:
                order_log = json.load(file)
        except FileNotFoundError:
            return f"Order log file '{order_log_file}' not found."

        if not any(entry["order_id"] == transaction_id and entry["user_id"] == user_id for entry in order_log):
            return "Transaction ID not associated with the given user ID."

        if transaction_status == "settlement":
            # Load the appropriate keylist
            try:
                with open(keylist_file, "r") as file:
                    keylist = json.load(file)
            except FileNotFoundError:
                return f"Keylist file '{keylist_file}' not found."

            if not keylist:
                return "No keys available in the keylist."

            # Get the first key and remove it
            key = keylist.pop(0)

            # Save the updated keylist back to the file
            with open(keylist_file, "w") as file:
                json.dump(keylist, file, indent=4)

            # Log the transaction details
            log_entry = {
                "user_id": user_id,
                "transaction_id": transaction_id,
                "transaction_status": transaction_status,
                "key_issued": key,
            }

            transaction_log.append(log_entry)

            with open(log_file, "w") as file:
                json.dump(transaction_log, file, indent=4)

            return f"Transaction settled. Key issued: {key}"
        else:
            return f"Transaction status is: {transaction_status}. No key issued."
    except json.JSONDecodeError:
        return "Failed to decode the response. Invalid JSON."