import requests
from bs4 import BeautifulSoup
import os

LINE_TOKEN = os.environ["LINE_TOKEN"]
LINE_USER_ID = os.environ["LINE_USER_ID"]

def get_gold_price():
    url = "https://xn--42cah7d0cxcvbbb9x.com/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    text = soup.get_text()

    import re

    buy_match = re.search(r"รับซื้อ\s*([\d,]+\.\d+)", text)
    sell_match = re.search(r"ขายออก\s*([\d,]+\.\d+)", text)

    buy = buy_match.group(1).replace(",", "")
    sell = sell_match.group(1).replace(",", "")

    return float(buy), float(sell)


def send_line(message):

    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + LINE_TOKEN
    }

    data = {
        "to": LINE_USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    requests.post(url, headers=headers, json=data)


buy, sell = get_gold_price()

message = f"""
Gold Price Update

Gold Bar 96.5%
Buy: {buy:,.0f} THB
Sell: {sell:,.0f} THB

Source: ราคาทอง.com
"""

print(message)

send_line(message)
