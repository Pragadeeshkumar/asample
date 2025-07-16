import requests
import pandas as pd
import os
import pytz

def get_binance_ohlcv(symbol="BTCUSDT", interval="1m", limit=1000):
    url = f"https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'num_trades',
        'taker_buy_base_vol', 'taker_buy_quote_vol', 'ignore'
    ])

    # Convert timestamp to IST
    utc = pytz.utc
    ist = pytz.timezone('Asia/Kolkata')
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms').dt.tz_localize(utc).dt.tz_convert(ist)

    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)

    return df

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    coins = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT","XRPUSDT","SUIUSDT","AVAXUSDT","TRXUSDT","TONUSDT"]
    
    for coin in coins:
        df = get_binance_ohlcv(coin)
        file_path = f"data/{coin.lower()}_ohlcv.csv"
        df.to_csv(file_path, index=False)
        print(f"Saved: {file_path}")
