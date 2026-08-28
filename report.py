import json


STARTING_BALANCE = 100.00


def load_account():

    with open("account.json", "r") as file:
        return json.load(file)


def show_report():

    account = load_account()

    balance = account["balance"]
    trades = account["trades"]
    wins = account["wins"]
    losses = account["losses"]
    profit = account["total_profit"]

    if trades > 0:
        win_rate = (wins / trades) * 100
    else:
        win_rate = 0

    return_percent = ((balance - STARTING_BALANCE) / STARTING_BALANCE) * 100


    print("\n🤖 KrakenBot Performance Report")
    print("-----------------------------")
    print(f"Balance: ${balance:.2f}")
    print(f"Return: {return_percent:.2f}%")
    print()
    print(f"Trades: {trades}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Win Rate: {win_rate:.1f}%")
    print()
    print(f"Total Profit: ${profit:.2f}")


if __name__ == "__main__":
    show_report()