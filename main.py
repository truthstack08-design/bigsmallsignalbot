import requests, os, time, json, hashlib
from datetime import datetime, timezone

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"})

def get_real_dhani_history():
    # Try multiple domains + without signature
    domains = ["https://dhaniwin4.com", "https://dhani11.com", "https://dhaniwin1.com"]
    for domain in domains:
        try:
            url = f"{domain}/api/webapi/GetNoaverageEmerdList"
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "application/json",
                "Origin": domain,
                "Referer": f"{domain}/"
            }
            # Signature ke bina simple payload - zyada kaam karta hai
            payload = {
                "pageSize": 10,
                "pageNo": 1,
                "typeId": 1,
                "language": 0
            }
            r = requests.post(url, json=payload, headers=headers, timeout=10)
            print(f"Trying {domain}: {r.status_code} {r.text[:200]}")
            data = r.json()
            if data.get('code') == 0 and data.get('data', {}).get('list'):
                print(f"SUCCESS from {domain}")
                return data['data']['list']
        except Exception as e:
            print(f"Fail {domain}: {e}")
            continue
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

        import random
        signal = random.choice(["BIG","SMALL"])

        last = load_last()
        result_text = ""

        if last:
            history = get_real_dhani_history()
            real_num = None
            real_bs = None
            real_period = last['period']

            if history:
                for item in history:
                    if str(item['issueNumber']) == str(last['period']):
                        real_num = int(item['number'])
                        real_bs = "BIG" if real_num >=5 else "SMALL"
                        real_period = item['issueNumber']
                        break
            
            if real_num is not None:
                win = (last['signal'] == real_bs)
                icon = "✅ *WIN* 💰" if win else "❌ *LOSS* 📉"
                result_text = f"""
━━━━━━━━━━━━━━
📊 LAST RESULT
🆔 {real_period}
🔢 Number: {real_num} ({real_bs})
🎯 Prediction: {last['signal']}
{icon}
━━━━━━━━━━━━━━
"""
            else:
                result_text = f"""
━━━━━━━━━━━━━━
📊 LAST RESULT
🆔 {last['period']}
🎯 Prediction: {last['signal']}
⏳ Result: Waiting for official...
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
