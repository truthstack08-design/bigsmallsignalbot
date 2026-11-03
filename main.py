import requests, os, time, random
from datetime import datetime, timezone

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, data=data)

def get_real_result():
    """Dhani ka asli result lene ki koshish"""
    try:
        # DhaniWin ka common API pattern
        url = "https://dhaniwin4.com/api/webapi/GetNoaverageEmerdList"
        payload = {
            "pageSize": 10,
            "pageNo": 1,
            "typeId": 1,
            "language": 0,
            "random": "4a0522c6ecd8410496260e9b7ff4e346",
            "signature": "D94CC2DD92A812B26D56A3D9065A1834"
        }
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json",
            "Origin": "https://dhaniwin4.com"
        }
        r = requests.post(url, json=payload, headers=headers, timeout=5)
        data = r.json()
        if data and 'data' in data and 'list' in data['data']:
            last = data['data']['list'][0]
            # last = {'issueNumber': '20261103100010937', 'number': 9, ...}
            num = int(last.get('number', 0))
            period = last.get('issueNumber', '')
            big_small = "BIG" if num >= 5 else "SMALL"
            return period, num, big_small
    except Exception as e:
        print(f"API Error: {e}")
    return None, None, None

print("REAL RESULT Bot Started...")

last_prediction_period = None
last_prediction_signal = None

while True:
    try:
        now_utc = datetime.now(timezone.utc)
        minute_utc = now_utc.hour * 60 + now_utc.minute
        period = f"{now_utc.strftime('%Y%m%d')}1000{10001 + minute_utc}"
        signal = random.choice(["BIG", "SMALL"])

        # Asli result check karo
        result_text = ""
        if last_prediction_period:
            real_period, real_num, real_bs = get_real_result()
            if real_period:
                # Agar real result mil gaya to sahi WIN/LOSS
                if real_bs == last_prediction_signal:
                    result_text = f"""
━━━━━━━━━━━━━━
📊 LAST RESULT - {real_period}
🔢 Number: {real_num} ({real_bs})
🎯 Prediction: {last_prediction_signal}
✅ *WIN* 💰🔥
━━━━━━━━━━━━━━
"""
                else:
                    result_text = f"""
━━━━━━━━━━━━━━
📊 LAST RESULT - {real_period}
🔢 Number: {real_num} ({real_bs})
🎯 Prediction: {last_prediction_signal}
❌ *LOSS* 📉
━━━━━━━━━━━━━━
"""
            else:
                # API fail ho to bina WIN/LOSS ke sirf result dikhao
                result_text = f"""
━━━━━━━━━━━━━━
📊 LAST PERIOD: {last_prediction_period}
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
        print(f"Sent: {period} -> {signal}")

        last_prediction_period = period
        last_prediction_signal = signal

        time.sleep(60)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
