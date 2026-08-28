from market_filter import market_ok
from strategy import get_price_data
from strategy_engine import analyze_setup


def trade_decision(pair):

    df = get_price_data(pair)

    if df is None:
        return {
            "pair": pair,
            "price": 0,
            "ema": 0,
            "rsi": 0,
            "score": 0,
            "trend": "UNKNOWN",
            "signal": "NO DATA"
        }

    latest = df.iloc[-1]

    setup = analyze_setup(
        pair,
        float(latest["close"]),
        float(latest["ema"]),
        float(latest["rsi"]),
        float(latest["volume"]),
        float(df["volume"].tail(20).mean())
    )

    if not market_ok(
        setup["price"],
        setup["ema"],
        setup["rsi"]
    ):
        print("🚫 Market filter: BLOCKED")
        setup["signal"] = "BLOCKED"
        return setup

    print("Score:", setup["score"])
    print("Trend:", setup["trend"])
    print("Signal:", setup["signal"])

    return setup
