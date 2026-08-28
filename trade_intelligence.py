import csv
from collections import defaultdict


def load_trades():

    trades = []

    try:
        with open("trades.csv", "r") as file:

            reader = csv.DictReader(file)

            for row in reader:
                trades.append(row)

    except FileNotFoundError:
        print("No trade history found.")

    return trades



def analyze_intelligence():

    trades = load_trades()

    if not trades:
        print("No trades available.")
        return


    coin_stats = defaultdict(lambda: {
        "trades": 0,
        "wins": 0,
        "profit": 0
    })


    for trade in trades:

        pair = trade.get("pair", "Unknown")
        profit = float(trade.get("profit", 0))


        coin_stats[pair]["trades"] += 1
        coin_stats[pair]["profit"] += profit


        if profit > 0:
            coin_stats[pair]["wins"] += 1


    print("\n🧠 KrakenBot Trade Intelligence")
    print("------------------------------")


    for pair, stats in coin_stats.items():

        win_rate = (
            stats["wins"] / stats["trades"]
        ) * 100


        print(f"\n{pair}")
        print(f"Trades: {stats['trades']}")
        print(f"Wins: {stats['wins']}")
        print(f"Win Rate: {win_rate:.1f}%")
        print(f"Profit: ${stats['profit']:.2f}")


if __name__ == "__main__":
    analyze_intelligence()