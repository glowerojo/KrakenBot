def calculate_score(price, ema, rsi, volume, avg_volume):

    score = 0


    # Trend
    if price > ema:
        score += 1


    # Momentum
    if 50 < rsi < 70:
        score += 1


    # Volume
    if volume > avg_volume:
        score += 1


    return score



def analyze_setup(
    pair,
    price,
    ema,
    rsi,
    volume,
    avg_volume
):

    score = calculate_score(
        price,
        ema,
        rsi,
        volume,
        avg_volume
    )


    trend = (
        "Bullish"
        if price > ema
        else "Bearish"
    )


    return {
        "pair": pair,
        "price": price,
        "ema": ema,
        "rsi": rsi,
        "score": score,
        "trend": trend,
        "signal": (
            "BUY"
            if score >= 3
            else "WAIT"
        )
    }