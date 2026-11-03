import requests, os, time, random, json
from datetime import datetime, timezone

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, data=data)

def load_last():
    try:
        with open("last_result.json", "r") as f:
            return json.load(f)
    except:
        return None

def save_last(data):
    with open("last_result.json", "w") as f:
        json.dump(data, f)

print("FINAL PERSISTENT Bot Started...")

while True:
    try:
        now_utc = datetime.now(timezone.utc)
        minute_utc = now_utc.hour * 60 + now_utc.minute
        period = f"{now_utc.strftime('%Y%m%d')}1000{10001 + minute_utc}"
        
        signal = random.choice(["BIG", "SMALL"])
        current_number = random.randint(0, 9)

        # Pichla data file se lo
        last_data = load_last()
        result_text = ""
        
        if last_data:
            last_period = last_data['period']
            last_signal = last_data['signal']
            last_number = last_data['number']
            last_bs = "BIG" if last_number >=5 else "SMALL"
            
            win = (last_signal == last_bs)
            icon = "✅ *WIN* 💰🔥" if win else "❌ *LOSS* 📉"
            
            result_text = f"""
━━━━━━━━━━━━━━
📊 LAST RESULT
🆔 {last_period}
🔢 Number: {last_number} ({last_bs})
🎯 Prediction: {last_signal}
{icon}
━━━━━━━━━━━━━━
"""
        else:
            result_text = """
━━━━━━━━━━━━━━
📊 Starting New Session...
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
        print(f"Sent: {period} | Pred: {signal}")

        # Current ko save karo next ke liye
        save_last({"period": period, "signal": signal, "number": current_number})

        time.sleep(60)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
