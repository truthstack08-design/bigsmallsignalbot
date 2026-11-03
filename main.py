import requests
import time
import os
import random
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def send_signal():
    signal = random.choice(["BIG", "SMALL"])
    confidence = random.randint(85, 98)
    now = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    
    message = f"""🚨 *BIG SMALL VIP SIGNAL* 🚨

🔮 *SIGNAL: {signal}*
🎯 Confidence: {confidence}%
⏰ Time: {now}

⚡️ Next signal in 1 min
👉 Join: @parasbigsmallvipsignal24h"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, data=data)
    print(f"Sent: {signal}")

while True:
    try:
        send_signal()
    except Exception as e:
        print(e)
    time.sleep(60)
