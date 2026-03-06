import requests
import os
from bs4 import BeautifulSoup

# Get LINE token from GitHub Secret
LINE_TOKEN = os.environ["LINE_TOKEN"]

PRICE_FILE = "last_price.txt"


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
            buy = cols[1].replace(",", "")
            sell = cols[2].replace(",", "")
            break

    return int(buy), int(sell)


def load_last_price():

    try:
        with open(PRICE_FILE, "r") as f:
            data = f.read().split(",")

            last_buy = int(data[0])
            last_sell = int(data[1])

            return last_buy, last_sell

    except:
        return None, None


def save_price(buy, sell):

    with open(PRICE_FILE, "w") as f:
        f.write(f"{buy},{sell}")


def price_change(new, old):

    if old is None:
        return ""

    diff = new - old

    if diff > 0:
        return f"⬆ +{diff}"
    elif diff < 0:
        return f"⬇ {diff}"
    else:
        return "→ 0"


def send_line(message):

    url = "https://notify-api.line.me/api/notify"

    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}"
    }

    data = {
        "message": message
    }

    r = requests.post(url, headers=headers, data=data)

    print("LINE status:", r.status_code)
    print(r.text)


# MAIN

buy, sell = get_gold_price()

last_buy, last_sell = load_last_price()

buy_change = price_change(buy, last_buy)
sell_change = price_change(sell, last_sell)

message = f"""
Gold Price Update

Gold Bar 96.5%
Buy: {buy:,} THB {buy_change}
Sell: {sell:,} THB {sell_change}

Source: ราคาทอง.com
"""

print(message)

send_line(message)

save_price(buy, sell)
