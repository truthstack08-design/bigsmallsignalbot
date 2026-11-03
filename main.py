import requests, os, time, json, hashlib
from datetime import datetime, timezone

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"})

def get_real_dhani_history():
    # Dhani ka real API - ye asli number deta hai
    try:
        url = "https://dhaniwin4.com/api/webapi/GetNoaverageEmerdList"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json",
            "Origin": "https://dhaniwin4.com",
            "Referer": "https://dhaniwin4.com/"
        }
        payload = {
            "pageSize": 10,
            "pageNo": 1,
            "typeId": 1,
            "language": 0,
            "random": "f1a3c2d4e5b6a7c8",
            "signature": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
        }
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        data = r.json()
        if data['code'] == 0:
            return data['data']['list']  # ye list me 10 real results honge
    except Exception as e:
        print("API fail:", e)
    return None

def load_last():
    try:
        with open("last.json","r") as f:
            return json.load(f)
    except:
        return None

def save_last(d):
    with open("last.json","w") as f:
        json.dump(d,f)

while True:
    try:
        now = datetime.now(timezone.utc)
        mins = now.hour*60 + now.minute
        period = f"{now.strftime('%Y%m%d')}1000{10001+mins}"

        # Naya prediction
        import random
        signal = random.choice(["BIG","SMALL"])

        last = load_last()
        result_text = ""

        if last:
            # Asli history se check karo
            history = get_real_dhani_history()
            real_num = None
            real_bs = None
            real_period = last['period']

            if history:
                for item in history:
                    if item['issueNumber'] == last['period']:
                        real_num = int(item['number'])
                        real_bs = "BIG" if real_num >=5 else "SMALL"
                        real_period = item['issueNumber']
                        break
            
            # Agar API se mila to asli, warna pichla wala hi
            if real_num is not None:
                win = (last['signal'] == real_bs)
                icon = "✅ *WIN* 💰" if win else "❌ *LOSS* 📉"
                result_text = f"""
━━━━━━━━━━━━━━
📊 LAST RESULT
🆔 {real_period}
🔢 Number: {real_num} ({real_bs})  <- Dhani ka asli
🎯 Prediction: {last['signal']}
{icon}
━━━━━━━━━━━━━━
"""
            else:
                result_text = f"""
━━━━━━━━━━━━━━
📊 LAST RESULT (API fail)
🆔 {last['period']}
🎯 Prediction: {last['signal']}
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
        save_last({"period": period, "signal": signal})
        time.sleep(60)

    except Exception as e:
        print(e)
        time.sleep(10)
