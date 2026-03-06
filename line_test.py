import requests
from bs4 import BeautifulSoup
import os
import json

LINE_TOKEN = os.environ["LINE_TOKEN"]
LINE_USER_ID = os.environ["LINE_USER_ID"]

def get_gold_price():

    url = "https://xn--42cah7d0cxcvbbb9x.com/"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    rows = soup.find_all("tr")

    buy = None
    sell = None

    for row in rows:
        text = row.get_text()

        if "ทองคำแท่ง" in text:

            cols = [c.strip() for c in row.get_text("\n").split("\n") if c.strip()]

            if len(cols) >= 3:
                buy = cols[1].replace(",", "")
                sell = cols[2].replace(",", "")

            break

    return int(float(buy)), int(float(sell))


def send_line(message):

    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_TOKEN}"
    }

    body = {
        "to": LINE_USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    r = requests.post(url, headers=headers, json=body)

    print("LINE Status:", r.status_code)
    print(r.text)


def load_last_price():

    try:
        with open("last_price.json", "r") as f:
            return json.load(f)
    except:
        return {"buy": 0, "sell": 0}


def save_last_price(buy, sell):

    with open("last_price.json", "w") as f:
        json.dump({"buy": buy, "sell": sell}, f)


buy, sell = get_gold_price()

last = load_last_price()

diff_buy = buy - last["buy"]
diff_sell = sell - last["sell"]

message = f"""Gold Price Update

Gold Bar 96.5%
Buy: {buy:,} THB ({diff_buy:+})
Sell: {sell:,} THB ({diff_sell:+})

Source: ราคาทอง.com
"""

print(message)

send_line(message)

save_last_price(buy, sell)
