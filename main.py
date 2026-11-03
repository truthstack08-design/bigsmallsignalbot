import os, time, random, requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=data)
        print(r.text)
    except Exception as e:
        print(e)

print("BOT STARTED")
send("✅ <b>Big Small Bot Started!</b>\nAb har 1 min me signal aayega...")

while True:
    signal = random.choice(["BIG 🟢", "SMALL 🔴"])
    num = random.randint(0, 9)
    msg = f"📊 <b>BIG SMALL SIGNAL</b>\n\n🎯 Signal: <b>{signal}</b>\n🔢 Number: {num}\n⏰ {time.strftime('%I:%M:%S %p')}"
    send(msg)
    print(f"Sent: {signal}")
    time.sleep(60)
