import requests
import time
import random
import os
import threading
from flask import Flask

app = Flask(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
    except:
        pass

def listen():
    offset = 0
    send("Bot Ready ✅\nAb Period Number bhejo, mai Prediction dunga\nExample: 202611043145")
    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={offset}&timeout=30"
            res = requests.get(url, timeout=35).json()
            for r in res.get("result", []):
                offset = r["update_id"] + 1
                msg = r.get("message", {})
                text = msg.get("text", "").strip()
                # Sirf number aaya to prediction do
                if text.isdigit():
                    try:
                        next_period = str(int(text) + 1)
                    except:
                        next_period = text
                    signal = random.choice(["BIG 🟢", "SMALL 🔴"])
                    send(f"Period: {next_period}\nPrediction: {signal}\nTime: 1 Min\nDhani Win - Next Signal")
        except:
            time.sleep(2)
        time.sleep(1)

@app.route('/')
def home():
    return "Bot is Running!"

threading.Thread(target=listen, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
