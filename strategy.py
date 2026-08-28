import krakenex
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

kraken = krakenex.API()

def get_price_data(pair="XBTUSD", interval=15):
    response = kraken.query_public(
        "OHLC",
        {
            "pair": pair,
            "interval": interval
        }
    )

    if response["error"]:
        print(response["error"])
        return None

    result = response["result"]

    # Find the OHLC data key (ignore "last")
    data_key = [key for key in result.keys() if key != "last"][0]

    data = result[data_key]

    df = pd.DataFrame(
        data,
        columns=[
            "time",
            "open",
            "high",
            "low",
            "close",
            "vwap",
            "volume",
            "count"
        ]
    )

    df["close"] = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)
    df["ema"] = EMAIndicator(
        df["close"],
        window=20
    ).ema_indicator()

    df["rsi"] = RSIIndicator(
        df["close"],
        window=14
    ).rsi()

    return df


def analyze_market(pair):
    df = get_price_data(pair)

    if df is None:
        return

    df["ema"] = EMAIndicator(
        df["close"],
        window=20
    ).ema_indicator()

    df["rsi"] = RSIIndicator(
        df["close"],
        window=14
    ).rsi()

    latest = df.iloc[-1]

    print("\nMarket:", pair)
    print("Price:", latest["close"])
    print("EMA:", round(latest["ema"], 2))
    print("RSI:", round(latest["rsi"], 2))

    if latest["close"] > latest["ema"] and latest["rsi"] < 70:
        print("🟢 BUY SETUP")
    elif latest["rsi"] > 70:
        print("🔴 OVERBOUGHT")
    else:
        print("🟡 WAIT")


if __name__ == "__main__":
    analyze_market("XBTUSD")
    analyze_market("ETHUSD")
