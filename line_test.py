import requests
import re
import os

url = "https://xn--42cah7d0cxcvbbb9x.com/"

try:
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    html = res.text
except:
    html = ""

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

LINE_TOKEN = os.getenv("nVV9K+Xb5Myd6hjkVWkkA/JbiDR4V+LUjfXS8mJfhMIQElpvcP/BTgtutIeA3Z52t82kcVeSQZOOU4MgM5+2OAiobJjhoRUSiEjX1fgkI5dt5E5Vc/bCyj3H4QkmRfl468zLrr5nkXwN9DblPIpx3QdB04t89/1O/w1cDnyilFU=")

try:
    requests.post(
        "https://notify-api.line.me/api/notify",
        headers={"Authorization": f"Bearer {LINE_TOKEN}"},
        data={"message": message},
        timeout=10
    )
    print("Message sent")

except Exception as e:
    print("LINE send failed:", e)

response = requests.post(
    "https://notify-api.line.me/api/notify",
    headers={"Authorization": f"Bearer {LINE_TOKEN}"},
    data={"message": message}
)

print(response.status_code)
print(response.text)
