import time
import subprocess

def run_fetch():
    print("🔁 Running prediction script...")
    subprocess.run(["python", r"C:\Users\praga\OneDrive\Desktop\Trading Bot\fetch_data.py"])
    subprocess.run(["python", r"C:\Users\praga\OneDrive\Desktop\Trading Bot\indicators\calculate_indicators.py"])
    subprocess.run(["python", r"C:\Users\praga\OneDrive\Desktop\Trading Bot\signal\generate_signal.py"])
    subprocess.run(["python", r"C:\Users\praga\OneDrive\Desktop\Trading Bot\ml_model\predict.py"])

print("⏱️ Starting 60-second loop...")
while True:
    run_fetch()
    time.sleep(60)