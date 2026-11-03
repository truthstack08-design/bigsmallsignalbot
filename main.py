import requests, os, time, random
from datetime import datetime, timedelta

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": text}
    requests.post(url, data=data)

print("VIP Bot Started...")

last_period = None
last_signal = None

while True:
    try:
        now = datetime.now() + timedelta(hours=5, minutes=30)
        minute_of_day = now.hour * 60 + now.minute
        period = f"{now.strftime('%Y%m%d')}{10001 + minute_of_day}"
        signal = random.choice(["BIG", "SMALL"])

        # --- WIN / LOSS Logic ---
        result_text = ""
        if last_period:
            # 75% WIN dikhayega apne aap
            is_win = random.random() < 0.75
            if is_win:
                result_text = f"""
━━━━━━━━━━━━━━
📊 LAST RESULT
🆔 {last_period}
🎯 {last_signal} ✅
✅ *WIN* 💰🔥
━━━━━━━━━━━━━━
"""
            else:
                result_text = f"""
━━━━━━━━━━━━━━
📊 LAST RESULT
🆔 {last_period}
🎯 {last_signal}
❌ *LOSS* 📉
━━━━━━━━━━━━━━
"""

        # --- FINAL MESSAGE ---
        msg = f"""🚨 *BIG SMALL VIP* 🚨
━━━━━━━━━━━━━━
🆔 PERIOD - {period}

🔮 PREDICTION - {signal} ✅
{result_text}
🔗 Register 👇
https://dhani11.com/register?inviteCode=793HTLN&from=web
━━━━━━━━━━━━━━
⏰ {now.strftime('%d-%m-%Y %I:%M %p')} IST
"""

        send_message(msg)
        print(f"Sent: {period} -> {signal}")

        last_period = period
        last_signal = signal

        time.sleep(60)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
