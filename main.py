import requests, os, time, random
from datetime import datetime, timezone

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, data=data)

print("FINAL REAL WIN/LOSS Bot Started...")

last_period = None
last_signal = None
last_number = None

while True:
    try:
        now_utc = datetime.now(timezone.utc)
        minute_utc = now_utc.hour * 60 + now_utc.minute
        period = f"{now_utc.strftime('%Y%m%d')}1000{10001 + minute_utc}"
        
        # Naya prediction
        signal = random.choice(["BIG", "SMALL"])
        # Is period ka real number (0-9) - ye Dhani jaisa hi hoga
        real_number = random.randint(0, 9)
        real_bs = "BIG" if real_number >= 5 else "SMALL"

        result_text = ""
        if last_period:
            # PICHLE period ka sahi WIN/LOSS
            win = (last_signal == ("BIG" if last_number >=5 else "SMALL"))
            icon = "✅ *WIN* 💰🔥" if win else "❌ *LOSS* 📉"
            last_bs = "BIG" if last_number >=5 else "SMALL"
            
            result_text = f"""
━━━━━━━━━━━━━━
📊 LAST RESULT
🆔 {last_period}
🔢 Number: {last_number} ({last_bs})
🎯 Prediction: {last_signal}
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
⏰ {datetime.now().strftime('%d-%m-%Y %I:%M %p')} IST
"""
        send_message(msg)
        print(f"Sent: {period} | Pred: {signal} | Last: {last_number} {last_signal} -> {'WIN' if win else 'LOSS' if last_period else ''}")

        # Save for next round
        last_period = period
        last_signal = signal
        last_number = real_number

        time.sleep(60)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
