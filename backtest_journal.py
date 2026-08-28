import csv
from datetime import datetime


FILE = "backtest_trades.csv"


def log_trade(
    pair,
    entry,
    exit_price,
    result,
    profit,
    score,
    rsi,
    ema,
    trend
):

    file_exists = False

    try:
        with open(FILE, "r"):
            file_exists = True
    except FileNotFoundError:
        pass


    with open(FILE, "a", newline="") as file:

        writer = csv.writer(file)


        if not file_exists:
            writer.writerow([
                "date",
                "pair",
                "entry",
                "exit",
                "result",
                "profit",
                "score",
                "rsi",
                "ema",
                "trend"
            ])


        writer.writerow([
            datetime.now(),
            pair,
            entry,
            exit_price,
            result,
            round(profit,2),
            score,
            round(rsi,2),
            round(ema,2),
            trend
        ])