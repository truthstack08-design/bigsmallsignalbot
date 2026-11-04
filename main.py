import requests, os, time, json, random
from datetime import datetime, timezone

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def send(text):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                  data={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"})

def get_real_result(period_to_find):
    # Try multiple public APIs that are NOT blocked on GitHub
    apis = [
        "https://api.bdg88.win/api/webapi/GetNoaverageEmerdList",
        "https://api.bdg18.com/api/webapi/GetNoaverageEmerdList",
        "https://dhaniwin4.com/api/webapi/GetNoaverageEmerdList"
    ]
    payload = {"pageSize": 20, "pageNo": 1, "typeId": 1, "language": 0}
    headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
    
    for api in apis:
        try:
            r = requests.post(api, json=payload, headers=headers, timeout=10)
            data = r.json()
            if data.get('data',{}).get('list'):
                for item in data['data']['list']:
                    if str(item.get('issueNumber')) == str(period_to_find):
                        return int(item.get('number'))
                print(f"Checked {api}, period not found in list")
        except Exception as e:
            print(f"API fail {api}: {e}")
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
        signal = random.choice(["BIG","SMALL"])
        
        last = load_last()
        result_text = ""
        
        if last:
            real_num = get_real_result(last['period'])
            if real_num is not None:
                real_bs = "BIG" if real_num >= 5 else "SMALL"
                icon = "✅ *WIN* 💰" if last['signal'] == real_bs else "❌ *LOSS* 📉"
                result_text = f"\n📊 LAST: {last['period']} | Num {real_num} ({real_bs}) | Pred {last['signal']} {icon}\n"
            else:
                result_text = f"\n📊 LAST: {last['period']} | Pred {last['signal']} | ⏳ Official result awaited...\n"

        msg = f"🚨 BIG SMALL VIP 🚨\n🆔 {period}\n🔮 {signal}\n{result_text}\n⏰ {datetime.now().strftime('%d-%m-%Y %I:%M %p')}"
        send(msg)
        save_last({"period": period, "signal": signal})
        time.sleep(60)
    except Exception as e:
        print(e)
        time.sleep(10)
