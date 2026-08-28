import csv


def load_trades():

    trades = []

    try:
        with open("trades.csv", "r") as file:

            reader = csv.reader(file)

            for row in reader:
                trades.append(row)

    except FileNotFoundError:
        print("No trade history found.")

    return trades



def analyze():

    trades = load_trades()

    if len(trades) == 0:
        print("No trades to analyze.")
        return


    total_profit = 0
    wins = 0
    losses = 0
    profits = []


    for trade in trades:

        profit = float(trade[5])

        total_profit += profit
        profits.append(profit)


        if profit > 0:
            wins += 1
        else:
            losses += 1


    total_trades = len(trades)

    win_rate = (wins / total_trades) * 100

    average = total_profit / total_trades

    best = max(profits)

    worst = min(profits)


    print("\n📊 KrakenBot Trade Analyzer")
    print("--------------------------")
    print(f"Trades: {total_trades}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Win Rate: {win_rate:.1f}%")
    print()
    print(f"Total Profit: ${total_profit:.2f}")
    print(f"Average Trade: ${average:.2f}")
    print(f"Best Trade: ${best:.2f}")
    print(f"Worst Trade: ${worst:.2f}")


if __name__ == "__main__":
    analyze()