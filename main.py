import requests, os, time, json, urllib.parse
from datetime import datetime, timezone

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"})

def get_real_dhani_history():
    # Direct + 2 proxy try karega
    payload = {
        "pageSize": 10,
        "pageNo": 1,
        "typeId": 1,
        "language": 0
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }
    targets = [
        "https://dhaniwin4.com/api/webapi/GetNoaverageEmerdList",
        "https://dhani11.com/api/webapi/GetNoaverageEmerdList"
    ]
    # 1. Direct try
    for t in targets:
        try:
            r = requests.post(t, json=payload, headers=headers, timeout=8)
            data = r.json()
            if data.get('code') == 0 and data.get('data',{}).get('list'):
                return data['data']['list']
        except Exception as e:
            print(f"Direct fail {t}: {e}")

    # 2. Proxy se try - GitHub block bypass
    for t in targets:
        try:
            proxy_url = f"https://corsproxy.io/?{urllib.parse.quote(t, safe='')}"
            r = requests.post(proxy_url, json=payload, headers=headers, timeout=12)
            print(f"Proxy trying: {proxy_url} status {r.status_code}")
            data = r.json()
            # corsproxy kabhi kabhi direct list deta hai
            if isinstance(data, dict) and data.get('code') == 0:
                if data.get('data',{}).get('list'):
                    return data['data']['list']
        except Exception as e:
            print(f"Proxy fail: {e}")
            
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
            print(f"History result: {history}")
            real_num = None
            real_bs = None
            if history:
                for item in history:
                    if str(item.get('issueNumber')) == str(last['period']):
                        real_num = int(item.get('number'))
                        real_bs = "BIG" if real_num >=5 else "SMALL"
                        break
                # Agar exact period na mile to latest ka result le le last ke liye
                if real_num is None and len(history)>0:
                    # latest history ka first item last period se pehle ka hoga, usko use nahi karna
                    pass

            if real_num is not None:
                win = (last['signal'] == real_bs)
                icon = "✅ *WIN* 💰" if win else "❌ *LOSS* 📉"
                result_text = f"""
━━━━━━━━━━━━━━
📊 LAST RESULT
🆔 {last['period']}
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
⏳ Official result updating...
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
