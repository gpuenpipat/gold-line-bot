import os
import requests
from bs4 import BeautifulSoup

LINE_TOKEN = os.getenv("rY8xBYsQpEpLrXDViRB2eC6aYrsttGkPUSx0+1hk1xPW6YhjyOft/6U0mf6IGRzrt82kcVeSQZOOU4MgM5+2OAiobJjhoRUSiEjX1fgkI5cqDhpy1ed8NBrAPaCzbNqQ4cj+1dvkBApinXCZ0zwA8AdB04t89/1O/w1cDnyilFU=")
USER_ID = "Ub27b8ca8be36588af796a26e0a2b4af1"

url = "https://xn--42cah7d0cxcvbbb9x.com/"
res = requests.get(url)

soup = BeautifulSoup(res.text, "html.parser")

text = soup.get_text()

import re

buy_match = re.search(r"Buy\s*:\s*([\d,]+)", text)
sell_match = re.search(r"Sell\s*:\s*([\d,]+)", text)

buy = buy_match.group(1)
sell = sell_match.group(1)

buy_num = int(buy.replace(",", ""))
sell_num = int(sell.replace(",", ""))

# Load previous price
prev_buy = None
prev_sell = None

if os.path.exists("last_price.txt"):
    with open("last_price.txt") as f:
        prev_buy, prev_sell = map(int, f.read().split(","))

# Detect change
buy_change = 0
sell_change = 0

if prev_buy:
    buy_change = buy_num - prev_buy
    sell_change = sell_num - prev_sell

# Arrow indicator
def arrow(change):
    if change > 0:
        return f"▲ +{change}"
    elif change < 0:
        return f"▼ {change}"
    else:
        return "— 0"

message = f"""Gold Price Update

Gold Bar 96.5%
Buy: {buy} THB {arrow(buy_change)}
Sell: {sell} THB {arrow(sell_change)}

Source: ราคาทอง.com
"""

# Save latest price
with open("last_price.txt", "w") as f:
    f.write(f"{buy_num},{sell_num}")

headers = {
    "Authorization": f"Bearer {LINE_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "to": USER_ID,
    "messages": [{"type": "text", "text": message}]
}

requests.post(
    "https://api.line.me/v2/bot/message/push",
    headers=headers,
    json=payload
)
