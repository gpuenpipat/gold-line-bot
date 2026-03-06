import requests
from bs4 import BeautifulSoup

LINE_TOKEN = "rY8xBYsQpEpLrXDViRB2eC6aYrsttGkPUSx0+1hk1xPW6YhjyOft/6U0mf6IGRzrt82kcVeSQZOOU4MgM5+2OAiobJjhoRUSiEjX1fgkI5cqDhpy1ed8NBrAPaCzbNqQ4cj+1dvkBApinXCZ0zwA8AdB04t89/1O/w1cDnyilFU="

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


def send_line(message):

    url = "https://api.line.me/v2/bot/message/broadcast"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_TOKEN}"
    }

    body = {
        "messages":[
            {
                "type":"text",
                "text":message
            }
        ]
    }

    r = requests.post(url, headers=headers, json=body)

    print("Status:", r.status_code)
    print(r.text)


buy, sell = get_gold_price()

if buy and sell:

    message = f"""Gold Price Update

Gold Bar 96.5%
Buy: {buy} THB
Sell: {sell} THB

Source: ราคาทอง.com
"""

    print(message)

    send_line(message)

else:
    print("❌ Could not detect gold price")
