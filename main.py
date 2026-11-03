import requests, os, time, random
from datetime import datetime, timedelta

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": text}
    requests.post(url, data=data)

print("Bot Started...")

while True:
    try:
        now = datetime.now() + timedelta(hours=5, minutes=30)
        # Period jaise 20261103108XX
        period = f"{now.strftime('%Y%m%d')}108{random.randint(10,99)}"
        signal = random.choice(["BIG", "SMALL"])
        
        msg = f"""Period - {period}

Prediction - {signal} ✅

Register 🖇️ Link 👇

https://dhani11.com/register?inviteCode=793HTLN&from=web"""

        send_message(msg)
        print(f"Sent: {period} -> {signal}")
        time.sleep(60) # 1 min me ek signal

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
