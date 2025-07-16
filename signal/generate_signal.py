import pandas as pd
import os

def generate_signals(df):
    df = df.copy()
    df['buy_signal'] = 0

    condition = (
        (df['rsi14'] < 50) &  # Slightly relaxed RSI threshold
        (df['MACD_12_26_9'] > df['MACDs_12_26_9']) &
        (df['MACD_12_26_9'].shift(1) < df['MACDs_12_26_9'].shift(1))
    )
    df.loc[condition, 'buy_signal'] = 1
    return df

def set_targets(df, risk_reward_ratio=2.0, stop_loss_pct=0.02):
    df = df.copy()
    df['target'] = None
    df['stop_loss'] = None

    for i in range(len(df)):
        if df.loc[i, 'buy_signal'] == 1:
            entry = df.loc[i, 'close']
            stop_loss = entry * (1 - stop_loss_pct)
            target = entry + (entry - stop_loss) * risk_reward_ratio

            df.loc[i, 'stop_loss'] = round(stop_loss, 2)
            df.loc[i, 'target'] = round(target, 2)
    return df

def process_all_signals(input_folder="data/processed", output_folder="data/signals"):
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(input_folder):
        if file.endswith("_indicators.csv"):
            input_path = os.path.join(input_folder, file)
            df = pd.read_csv(input_path)
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            df = generate_signals(df)
            df = set_targets(df)

            symbol = file.replace("_indicators.csv", "")
            output_path = os.path.join(output_folder, f"{symbol}_signals.csv")
            df.to_csv(output_path, index=False)
            print(f"Signal created: {output_path}")

if __name__ == "__main__":
    process_all_signals()
