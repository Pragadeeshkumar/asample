import os
import time
import pandas as pd
import requests

PREDICTION_FOLDER = "data/prediction"
CHECK_INTERVAL = 60  # seconds

# 🔔 Telegram Setup — Replace with your values
BOT_TOKEN = "7646260085:AAHlSmPz4pKyJxv6Sx7ANbfMmKj-4oujSp0"
CHAT_ID = "-4929540622"  # Group or user chat ID

# Track last notified timestamp per symbol
last_buy_signal_time = {}

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print("⚠️ Telegram send failed:", response.text)
    except Exception as e:
        print("❌ Error sending Telegram message:", e)

def print_buy_signals():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"📡 BUY SIGNALS (updated: {time.strftime('%H:%M:%S')})\n")

    found = False

    for file in os.listdir(PREDICTION_FOLDER):
        if file.endswith("_predictions.csv"):
            symbol = file.replace("_predictions.csv", "")
            path = os.path.join(PREDICTION_FOLDER, file)

            try:
                df = pd.read_csv(path).dropna()
                if df.empty or 'ml_prediction' not in df.columns:
                    continue

                latest = df.iloc[-1]
                if int(latest['ml_prediction']) == 1:
                    timestamp = latest['timestamp']
                    found = True
                    print(f"🟢 {symbol.upper()} — BUY")
                    print(f"   Time       : {timestamp}")
                    print(f"   Close      : {latest['close']}")
                    print(f"   Target     : {latest.get('target', '-')}")
                    print(f"   Stop Loss  : {latest.get('stop_loss', '-')}\n")

                    # Notify only if this is a new signal
                    if last_buy_signal_time.get(symbol) != timestamp:

                        msg = f"""🚨 <b>NEW BUY SIGNAL</b>
<b>{symbol.upper()}</b>
Time: {timestamp}
Close: {latest['close']}
Target: {latest.get('target', '-')}
Stop Loss: {latest.get('stop_loss', '-')}"""

                        send_telegram(msg)
                        last_buy_signal_time[symbol] = timestamp

            except Exception as e:
                print(f"⚠️ Error processing {file}: {e}")

    if not found:
        print("❌ No BUY signals at this time.\n")

# Run forever
if __name__ == "__main__":
    while True:
        print_buy_signals()
        time.sleep(CHECK_INTERVAL)
