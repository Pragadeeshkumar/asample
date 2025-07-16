import pandas as pd
import joblib
import os

signal_folder = r"C:\Users\praga\OneDrive\Desktop\Trading Bot\data\signals"
prediction_folder = r"C:\Users\praga\OneDrive\Desktop\Trading Bot\data\prediction"
model_folder = r"C:\Users\praga\OneDrive\Desktop\Trading Bot\ml_model"
os.makedirs(prediction_folder, exist_ok=True)

features = ['rsi14', 'ema20', 'MACD_12_26_9', 'MACDs_12_26_9']

for file in os.listdir(signal_folder):
    if file.endswith("_signals.csv"):
        symbol = file.replace("_signals.csv", "")
        print(f"🔍 Predicting for {symbol}...")

        signal_path = os.path.join(signal_folder, file)
        model_path = os.path.join(model_folder, f"{symbol}_model.pkl")

        if not os.path.exists(model_path):
            print(f"⚠️ No model found for {symbol}, skipping.")
            continue

        try:
            df = pd.read_csv(signal_path)
            df = df.dropna()

            model = joblib.load(model_path)
            df['ml_prediction'] = model.predict(df[features])

            # Save predictions
            output_path = os.path.join(prediction_folder, f"{symbol}_predictions.csv")
            df.to_csv(output_path, index=False)
            print(f"✅ Predictions saved for {symbol} → {output_path}\n")

        except Exception as e:
            print(f"🔥 Error for {symbol}: {e}")
