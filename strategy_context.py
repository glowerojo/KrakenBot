current_trade = {
    "pair": "",
    "rsi": 0,
    "ema": 0,
    "score": 0,
    "trend": "",
    "entry_time": None
}


def save_context(pair, rsi, ema, score, trend):

    global current_trade

    current_trade = {
        "pair": pair,
        "rsi": rsi,
        "ema": ema,
        "score": score,
        "trend": trend,
        "entry_time": None
    }


def get_context():
    return current_trade