import requests
import re

url = "https://xn--42cah7d0cxcvbbb9x.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(url, headers=headers)
html = res.text

buy_match = re.search(r'รับซื้อ\s*([\d,]+)', html)
sell_match = re.search(r'ขายออก\s*([\d,]+)', html)

if buy_match and sell_match:
    buy = buy_match.group(1)
    sell = sell_match.group(1)

    message = f"""Gold Price Update

Gold Bar 96.5%
Buy: {buy} THB
Sell: {sell} THB

Source: ราคาทอง.com
"""
else:
    message = "Gold Price Update\n\nUnable to detect gold price today."

LINE_TOKEN = "rY8xBYsQpEpLrXDViRB2eC6aYrsttGkPUSx0+1hk1xPW6YhjyOft/6U0mf6IGRzrt82kcVeSQZOOU4MgM5+2OAiobJjhoRUSiEjX1fgkI5cqDhpy1ed8NBrAPaCzbNqQ4cj+1dvkBApinXCZ0zwA8AdB04t89/1O/w1cDnyilFU="

headers = {
    "Authorization": f"Bearer {LINE_TOKEN}"
}

data = {
    "message": message
}

requests.post(
    "https://notify-api.line.me/api/notify",
    headers=headers,
    data=data
)

print("Message sent")
