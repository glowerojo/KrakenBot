

import json
import os
import csv
from datetime import datetime
from journal_v2 import record_trade as journal_record_trade
def load_account():

    if os.path.exists("account.json"):

        with open("account.json", "r") as file:
            return json.load(file)

    return {
        "balance": 100.00,
        "trades": 0,
        "wins": 0,
        "losses": 0,
        "total_profit": 0.00,
        "position": None
    }


def save_account(account):

    with open("account.json", "w") as file:
        json.dump(account, file, indent=4)

def log_trade(pair, entry, exit_price, result, profit):

    with open("trades.csv", "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            pair,
            entry,
            exit_price,
            result,
            round(profit, 2)
        ])

account = load_account()
balance = account["balance"]
position = account.get("position")
trade_log = []

TRADE_SIZE = 50
TAKE_PROFIT = 0.02
STOP_LOSS = 0.01

from risk_manager import record_trade

def open_trade(pair, price, trade_size=50):
    global balance, position

    if position:
        print("Position already open")
        return

    if not record_trade():
        return

    position = {
        "pair": pair,
        "entry": price,
        "amount": trade_size,
        "target": price * (1 + TAKE_PROFIT),
        "stop": price * (1 - STOP_LOSS)
    }

    balance -= trade_size

    print("\n🟢 OPEN TRADE")
    print(pair)
    print("Entry:", price)
    print("Target:", round(position["target"], 2))
    print("Stop:", round(position["stop"], 2))


def check_trade(price):
    global balance, position

    if not position:
        return

    if price >= position["target"]:
        close_trade(price, "TAKE PROFIT")

    elif price <= position["stop"]:
        close_trade(price, "STOP LOSS")


def close_trade(price, reason):
    global balance, position

    change = (price - position["entry"]) / position["entry"]
    profit = position["amount"] * change

    account["trades"] += 1
    account["total_profit"] += profit

    if profit > 0:
        account["wins"] += 1
    else:
        account["losses"] += 1
        account["daily_loss"] = account.get("daily_loss", 0) + abs(profit)

    balance += position["amount"] + profit
    profit = position["amount"] * change

    trade_log.append({
        "pair": position["pair"],
        "result": reason,
        "profit": round(profit, 2)
    })

    log_trade(
        position["pair"],
        position["entry"],
        price,
        reason,
        profit
    )

    print("\n🔴 CLOSED TRADE")
    print(reason)
    print("Profit/Loss:", round(profit, 2))

    journal_record_trade(
        position["pair"],
        position["entry"],
        price,
        reason,
        profit,
        0, 
        0,
        0,
        0
)

    position = None


    account["balance"] = balance
    account["position"] = None
    save_account(account)

def account_status():
    print("\nBalance:", round(balance, 2))
    print("History:", trade_log)


if __name__ == "__main__":
    open_trade("ETHUSD", 1910.89)
    check_trade(1950)
    account_status()
