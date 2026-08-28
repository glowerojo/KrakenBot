import csv


def load_trades():

    trades = []

    try:
        with open("trades.csv", "r") as file:

            reader = csv.reader(file)

            for row in reader:
                trades.append(row)

    except FileNotFoundError:
        pass

    return trades



def show_analytics():

    trades = load_trades()

    total_trades = len(trades)

    if total_trades == 0:
        print("\nNo trades recorded yet.")
        return


    wins = 0
    losses = 0
    total_profit = 0
    total_win = 0
    total_loss = 0


    for trade in trades:

        result = trade[4]
        profit = float(trade[5])

        total_profit += profit

        if profit > 0:
            wins += 1
            total_win += profit
        else:
            losses += 1
            total_loss += profit


    win_rate = (wins / total_trades) * 100

    avg_win = total_win / wins if wins else 0
    avg_loss = total_loss / losses if losses else 0


    print("\n🤖 KrakenBot Analytics")
    print("---------------------")
    print(f"Total Trades: {total_trades}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Win Rate: {win_rate:.1f}%")
    print()
    print(f"Total Profit: ${total_profit:.2f}")
    print(f"Average Win: ${avg_win:.2f}")
    print(f"Average Loss: ${avg_loss:.2f}")



if __name__ == "__main__":
    show_analytics()