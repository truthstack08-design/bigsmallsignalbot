import requests, os, time, random
from datetime import datetime, timedelta

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, data=data)

# Period number generate karna
def get_period():
    now = datetime.now()
    # Jaise 20261103-001
    date_str = now.strftime("%Y%m%d")
    minute_of_day = now.hour * 60 + now.minute
    period_no = f"{date_str}{10001 + minute_of_day}"
    return period_no

print("Pro Bot Started...")
while True:
    try:
        now = datetime.now()
        period = get_period()
        
        # Signal Logic
        signal = random.choice(["BIG", "SMALL"])
        confidence = random.randint(90, 97)
        
        # Next period ka time
        next_time = (now + timedelta(minutes=1)).strftime("%I:%M:%S %p")
        expiry = (now + timedelta(minutes=1)).strftime("%I:%M %p")
        
        msg = f"""🚨 *BIG SMALL VIP SIGNAL* 🚨
━━━━━━━━━━━━━━━━━
🆔 *PERIOD:* `{period}`

🔮 *PREDICTION:* *{signal}* ✅
📊 *Confidence:* {confidence}%
⏰ *Time:* {now.strftime("%d-%m-%Y %I:%M:%S %p")}

━━━━━━━━━━━━━━━━━
💰 *BET:* {signal}
🛡️ *Backup:* 1 Level Only
⏳ *Valid Till:* {expiry}

⚡ Next Signal: {next_time}
👉 Join: @parasbigsmallvipsignal24h
"""

        send_message(msg)
        print(f"Sent: {period} -> {signal}")
        time.sleep(60) # Har 1 min

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
