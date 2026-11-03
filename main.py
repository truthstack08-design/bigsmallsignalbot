import requests, os, time, random, json
from datetime import datetime, timezone

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, data=data)

def get_real_result():
    """Dhani ka real result - 3 API try karega"""
    apis = [
        "https://dhaniwin4.com/api/webapi/GetNoaverageEmerdList",
        "https://bdg88zf.com/api/webapi/GetNoaverageEmerdList",
        "https://dhaniwin4.com/api/webapi/GetGameIssue"
    ]
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://dhaniwin4.com",
        "Referer": "https://dhaniwin4.com/"
    }
    payload = {"pageSize":10,"pageNo":1,"typeId":1,"language":0,"random":"6b3e8f8a1c9d4e2f","signature":"E7B8F9A0C1D2E3F4A5B6C7D8E9F0A1B2"}
    
    for api_url in apis:
        try:
            r = requests.post(api_url, json=payload, headers=headers, timeout=6)
            j = r.json()
            # Try to parse
            if j.get('data') and j['data'].get('list'):
                lst = j['data']['list'][0]
                num = int(lst.get('number', lst.get('lottery', 0)))
                period = lst.get('issueNumber', lst.get('issue', ''))
                bs = "BIG" if num >=5 else "SMALL"
                return period, num, bs
            if j.get('data') and j['data'].get('issueNumber'):
                d = j['data']
                num = int(d.get('number', 0))
                period = d.get('issueNumber', '')
                bs = "BIG" if num >=5 else "SMALL"
                return period, num, bs
        except:
            continue
    return None, None, None

print("FINAL Bot Started...")

last_pred_period = None
last_pred_signal = None

while True:
    try:
        now_utc = datetime.now(timezone.utc)
        minute_utc = now_utc.hour * 60 + now_utc.minute
        period = f"{now_utc.strftime('%Y%m%d')}1000{10001 + minute_utc}"
        signal = random.choice(["BIG", "SMALL"])

        result_text = ""
        if last_pred_period:
            real_p, real_n, real_bs = get_real_result()
            
            # Agar real result mila
            if real_p and real_n is not None:
                win = (real_bs == last_pred_signal)
                icon = "✅ *WIN* 💰🔥" if win else "❌ *LOSS* 📉"
                result_text = f"""
━━━━━━━━━━━━━━
📊 LAST RESULT
🆔 {real_p}
🔢 Number: {real_n} ({real_bs})
🎯 My Prediction: {last_pred_signal}
{icon}
━━━━━━━━━━━━━━
"""
            else:
                # API fail bhi ho to bhi WIN/LOSS dikhega - random nahi, last prediction ka status
                # Yahan hum show karenge ki result aane wala hai
                result_text = f"""
━━━━━━━━━━━━━━
📊 LAST RESULT
🆔 {last_pred_period}
🎯 Prediction: {last_pred_signal}
⏳ Result Updating...
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
        print(f"Sent: {period}")

        last_pred_period = period
        last_pred_signal = signal
        time.sleep(60)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
