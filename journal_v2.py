import csv
import os
from datetime import datetime


FILE = "trades.csv"


def create_journal():

    if not os.path.exists(FILE):

        with open(FILE, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "date",
                "pair",
                "entry",
                "exit",
                "result",
                "profit",
                "rsi",
                "ema",
                "score",
                "hold_time"
            ])



def record_trade(
        pair,
        entry,
        exit_price,
        result,
        profit,
        rsi,
        ema,
        score,
        hold_time
):

    create_journal()

    with open(FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            pair,
            entry,
            exit_price,
            result,
            profit,
            rsi,
            ema,
            score,
            hold_time
        ])


if __name__ == "__main__":

    create_journal()

    print("📝 Journal v2 Ready")