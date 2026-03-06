import requests
import os

LINE_TOKEN = os.environ["nVV9K+Xb5Myd6hjkVWkkA/JbiDR4V+LUjfXS8mJfhMIQElpvcP/BTgtutIeA3Z52t82kcVeSQZOOU4MgM5+2OAiobJjhoRUSiEjX1fgkI5dt5E5Vc/bCyj3H4QkmRfl468zLrr5nkXwN9DblPIpx3QdB04t89/1O/w1cDnyilFU="]
LINE_USER = os.environ["Ub27b8ca8be36588af796a26e0a2b4af1"]

headers = {
    "Authorization": f"Bearer {LINE_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "to": LINE_USER,
    "messages": [
        {
            "type": "text",
            "text": "Test message from GitHub Actions"
        }
    ]
}

requests.post(
    "https://api.line.me/v2/bot/message/push",
    headers=headers,
    json=data
)
