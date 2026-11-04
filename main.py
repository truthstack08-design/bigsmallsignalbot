import requests, os, time, json, random
from datetime import datetime, timezone

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"})

def get_real_dhani_history():
    payload = {"pageSize": 10, "pageNo": 1, "typeId": 1, "language": 0}
    headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
    try:
        r = requests.post("https://dhaniwin4.com/api/webapi/GetNoaverageEmerdList", json=payload, headers=headers, timeout=8)
        data = r.json()
        if data.get('code') == 0:
            return data['data']['list']
    except:
        pass
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
            history = get_real_dhani_history()
            real_num = None
            real_bs = None

            # 1. Dhani ka real number dhoondo
            if history:
               
