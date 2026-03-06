import requests
from bs4 import BeautifulSoup
import os

URL = "https://xn--42cah7d0cxcvbbb9x.com/"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

price = soup.get_text()[:200]

LINE_TOKEN = os.environ["nVV9K+Xb5Myd6hjkVWkkA/JbiDR4V+LUjfXS8mJfhMIQElpvcP/BTgtutIeA3Z52t82kcVeSQZOOU4MgM5+2OAiobJjhoRUSiEjX1fgkI5dt5E5Vc/bCyj3H4QkmRfl468zLrr5nkXwN9DblPIpx3QdB04t89/1O/w1cDnyilFU="]
USER_ID = os.environ["Ub27b8ca8be36588af796a26e0a2b4af1"]

headers = {
    "Authorization": f"Bearer {LINE_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "to": USER_ID,
    "messages": [
        {
            "type": "text",
            "text": f"Gold Price Update\n\n{price}"
        }
    ]
}

requests.post(
    "https://api.line.me/v2/bot/message/push",
    headers=headers,
    json=data
)
