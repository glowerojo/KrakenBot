def market_ok(price, ema, rsi):

    if price < ema:
        return False

    if rsi < 52:
        return False

    if rsi > 70:
        return False

    return True