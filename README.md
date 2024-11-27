---
# Distrans Project Discord Bot

## Overview

Distrans Project is a custom Discord bot designed to manage the purchasing, generation, and retrieval of script keys for users. This bot integrates **Discord** for user interaction and **Midtrans** as the API provider for payment and transaction processing. Built using the **Pycord** library, it provides efficient and scalable features.

---

## Features

### 1. **Order Weekly/Monthly Keys**
- **Commands:**  
  - `/weekly` - Generates a new order for a weekly key and provides a payment link via Midtrans.
  - `/monthly` - Generates a new order for a monthly key and provides a payment link via Midtrans.
- The bot communicates with the **Midtrans Snap API** to:
  - Generate unique order IDs.
  - Create and provide secure payment links for users.

### 2. **Transaction Status Check**
- **Command:** `/checktrx <transaction_id>`
- Allows users to check the status of a transaction by fetching data from Midtrans.

### 3. **Key Management**
- **Command:** `/keylist`
- Lists all purchased keys for a user in an interactive menu.
- Keys are categorized as:
  - **Weekly**: Purchased using `/weekly`.
  - **Monthly**: Purchased using `/monthly`.
- Interactive navigation allows users to browse through their keys.

---

## Setup Instructions

### Prerequisites
1. **Python**  
   Ensure Python 3.8 or later is installed.
2. **Discord Bot Token**  
   Register a bot at [Discord Developer Portal](https://discord.com/developers/applications) and copy the token.
3. **Midtrans API Credentials**  
   Obtain your **server key** and **client key** from the [Midtrans Dashboard](https://dashboard.midtrans.com/).

### Installation
1. Clone this repository or copy the bot files to your project directory.
2. Install dependencies:
   ```bash
   pip install py-cord requests
   ```
3. Create a `config.json` file in the root directory:
   ```json
   {
       "merchant-id": "your-merchant-id",
       "client-key": "your-midtrans-client-key",
       "server-key": "your-midtrans-server-key",
       "bot-token": "your-discord-bot-token"
   }
   ```
4. Create required JSON files for data storage if they don't already exist:
   - `order_idsw.json` for weekly order logs.
   - `order_idsm.json` for monthly order logs.
   - `transaction_log.json` for recording transactions.

### Running the Bot
Run the bot using the following command:
```bash
python main.py
```

---

## Key Functionalities in Detail

### 1. **Integration with Midtrans**
- The bot uses Midtrans **Snap API** to handle transactions:
  - Generates payment links.
  - Checks transaction statuses.
  - Processes payments securely.

### 2. **Interactive Discord Commands**
- The bot utilizes **Pycord's slash commands** for a seamless user experience.
- Interactive views (e.g., paginated key lists) allow users to interact with their data.

---

## File Structure

```
/root
│
├── main.py                # Main bot script
├── config.json            # Configuration file for API keys
├── order_idsw.json        # Logs for weekly orders
├── order_idsm.json        # Logs for monthly orders
├── transaction_log.json   # Transaction records
├── checktrx.py            # Script for transaction status checking
├── orderweekly.py         # Script for weekly order processing
├── ordermonthly.py        # Script for monthly order processing
├── keylistw.json          # Weekly key list that will be sent to customer
├── keylistm.json          # Monthly key list that will be sent to customer
└── README.md              # Documentation
```

---

## Example Usage

### Ordering a Weekly Key
1. Run `/weekly` in Discord.
2. The bot generates an order ID and provides a payment link via Midtrans.
3. Complete the payment using the link.

### Viewing Purchased Keys
1. Run `/keylist` to see all keys purchased.
2. Use the interactive menu to browse and view details.

---

## Contribution Guidelines
Feel free to contribute to this project by creating pull requests or reporting issues. For API-related queries, visit the [Midtrans Documentation](https://api-docs.midtrans.com/).

---

## Credit
This project was developed by **@ny28** on Discord.  
For any questions or concerns about this repository, please contact **@ny28** directly on Discord.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---
