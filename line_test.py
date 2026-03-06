import requests
import os
from bs4 import BeautifulSoup

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

    return int(float(buy)), int(float(sell))


def load_last_price():

    try:
        with open(PRICE_FILE, "r") as f:
            data = f.read().split(",")

            return int(data[0]), int(data[1])

    except:
        return None, None


def save_price(buy, sell):

    with open(PRICE_FILE, "w") as f:
        f.write(f"{buy},{sell}")


def send_line(message):

    url = "https://notify-api.line.me/api/notify"

    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}"
    }

    data = {
        "message": message
    }

    requests.post(url, headers=headers, data=data)


buy, sell = get_gold_price()

last_buy, last_sell = load_last_price()

buy_diff = buy - last_buy if last_buy else 0
sell_diff = sell - last_sell if last_sell else 0

message = f"""
Gold Price Update

Gold Bar 96.5%
Buy: {buy:,} THB ({buy_diff:+})
Sell: {sell:,} THB ({sell_diff:+})

Source: ราคาทอง.com
"""

print(message)

send_line(message)

save_price(buy, sell)
