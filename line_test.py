import requests
from bs4 import BeautifulSoup
import os
import json

LINE_TOKEN = os.environ["LINE_TOKEN"]
LINE_USER = os.environ["LINE_USER"]

DATA_FILE = "last_price.json"


def get_gold_price():

    url = "https://xn--42cah7d0cxcvbbb9x.com/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    rows = soup.find_all("tr")

    buy = None
    sell = None

    for row in rows:
        text = row.get_text()

        if "ทองคำแท่ง" in text:
            cols = [c.strip() for c in row.get_text("\n").split("\n") if c.strip()]
            buy = cols[1]
            sell = cols[2]
            break

    return buy, sell


def load_last_price():

    if not os.path.exists(DATA_FILE):
        return None

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_price(buy, sell):

    data = {
        "buy": buy,
        "sell": sell
    }

    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


def send_line(message):

    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_TOKEN}"
    }

    body = {
        "to": LINE_USER,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    r = requests.post(url, headers=headers, json=body)

    print("Status:", r.status_code)
    print(r.text)


buy, sell = get_gold_price()

if buy and sell:

    last = load_last_price()

    change = ""

    if last:
        if buy != last["buy"] or sell != last["sell"]:
            change = "📈 Price changed"
        else:
            change = "➖ Price unchanged"
    else:
        change = "🆕 First record"

    message = f"""Gold Price Update

Gold Bar 96.5%
Buy: {buy} THB
Sell: {sell} THB

{change}

Source: ราคาทอง.com
"""

    send_line(message)

    save_price(buy, sell)

else:
    send_line("⚠️ Gold price not detected")
