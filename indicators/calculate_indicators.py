import pandas as pd
import pandas_ta as ta
import os

def add_indicators(df):
    df = df.copy()
    df['ema20'] = ta.ema(df['close'], length=20)
    df['rsi14'] = ta.rsi(df['close'], length=14)
    macd = ta.macd(df['close'])
    df = pd.concat([df, macd], axis=1)
    return df

def process_all_coins(input_folder="data", output_folder="data/processed"):
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(input_folder):
        if file.endswith("_ohlcv.csv"):
            df = pd.read_csv(os.path.join(input_folder, file))
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = add_indicators(df)
            output_path = os.path.join(output_folder, file.replace("_ohlcv", "_indicators"))
            df.to_csv(output_path, index=False)
            print(f"Processed and saved: {output_path}")

if __name__ == "__main__":
    process_all_coins()