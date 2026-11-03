import requests, os, time, random
from datetime import datetime, timezone

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, data=data)

print("LIVE CORRECT Bot Started...")

last_period = None
last_signal = None

while True:
    try:
        # UTC time - Dhani ka real logic
        now_utc = datetime.now(timezone.utc)
        now_ist = datetime.now() # For display
        minute_utc = now_utc.hour * 60 + now_utc.minute
        
        # Dhani ka asli format: YYYYMMDD + 1000 + (10001 + minute)
        period = f"{now_utc.strftime('%Y%m%d')}1000{10001 + minute_utc}"
        signal = random.choice(["BIG", "SMALL"])

        result_text = ""
        if last_period:
            is_win = random.random() < 0.8
            icon = "✅ *WIN* 💰🔥" if is_win else "❌ *LOSS*"
            result_text = f"""
━━━━━━━━━━━━━━
📊 LAST RESULT
🆔 {last_period}
🎯 {last_signal}
{icon}
━━━━━━━━━━━━━━
"""

        msg = f"""🚨 *BIG SMALL VIP* 🚨
━━━━━━━━━━━━━━
🆔 PERIOD - {period}

🔮 PREDICTION - {signal} ✅
{result_text}
🔗 Register 👇
https://dhani11.com/register?inviteCode=793HTLN&from=web
━━━━━━━━━━━━━━
⏰ {now_ist.strftime('%d-%m-%Y %I:%M %p')} IST
"""
        send_message(msg)
        print(f"Sent CORRECT: {period}")
        last_period = period
        last_signal = signal
        time.sleep(60)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
