import requests, os, time, random
from datetime import datetime, timedelta

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": text}
    requests.post(url, data=data)

print("Bot Started - Correct Period...")

while True:
    try:
        now = datetime.now() + timedelta(hours=5, minutes=30) # IST
        minute_of_day = now.hour * 60 + now.minute
        # Sahi sequence wala period
        period = f"{now.strftime('%Y%m%d')}{10001 + minute_of_day}"
        signal = random.choice(["BIG", "SMALL"])
        
        msg = f"""Period - {period}

Prediction - {signal} ✅

Register 🖇️ Link 👇

https://dhani11.com/register?inviteCode=793HTLN&from=web"""

        send_message(msg)
        print(f"Sent: {period} -> {signal}")
        time.sleep(60)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
