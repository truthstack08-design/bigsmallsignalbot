import requests, os, time, json, random
from datetime import datetime, timezone

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"})

def load_last():
    try:
        with open("last.json","r") as f:
            return json.load(f)
    except:
        return None

def save_last(d):
    with open("last.json","w") as f:
        json.dump(d,f)

print("Bot Started...")
while True:
    try:
        now = datetime.now(timezone.utc)
        mins = now.hour*60 + now.minute
        period = f"{now.strftime('%Y%m%d')}1000{10001+mins}"
        signal = random.choice(["BIG","SMALL"])
        
        last = load_last()
        result_text = ""
        
        if last:
            # TUMHARI WALI LOGIC
            # Pichli baar jo bola tha uska random result banao
            real_num = random.randint(0, 9)
            real_bs = "BIG" if real_num >= 5 else "SMALL"
            
            if last['signal'] == real_bs:
                icon = "✅ *WIN* 💰"
            else:
                icon = "❌ *LOSS* 📉"
            
            result_text = f"""
━━━━━━━━━━━━━━
📊 LAST RESULT
🆔 {last['period']}
🔢 Number: {real_num} ({real_bs})
🎯 Prediction: {last['signal']}
{icon}
━━━━━━━━━━━━━━
"""
            # SMALL bola SMALL aaya = WIN
            # SMALL bola BIG aaya = LOSS

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
        send(msg)
        save_last({"period": period, "signal": signal})
        print(f"Sent {period} {signal}")
        time.sleep(60)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
