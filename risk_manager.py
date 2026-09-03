import json
from datetime import datetime, timedelta

MAX_DAILY_LOSS = 5.00
MAX_DAILY_TRADES = 5
COOLDOWN_MINUTES = 30


def load_account():

    with open("account.json", "r") as file:
        return json.load(file)


def reset_daily_stats(account):

    today = datetime.now().strftime("%Y-%m-%d")

    last_reset = account.get("last_reset", "")

    if last_reset != today:

        account["trades_today"] = 0
        account["daily_loss"] = 0
        account["last_reset"] = today

        save_account(account)

    return account


def save_account(account):

    with open("account.json", "w") as file:
        json.dump(account, file, indent=4)



def can_trade():
    account = reset_daily_stats(load_account())

    # Daily trade limit
    if account.get("trades_today", 0) >= MAX_DAILY_TRADES:
        print("🚫 Daily trade limit reached")
        return False

    # Daily loss limit
    if account.get("daily_loss", 0) >= MAX_DAILY_LOSS:
        print("🚫 Daily loss limit reached")
        return False


    # Cooldown check
    last_trade = account.get("last_trade_time", "")
    if last_trade:
        last_time = datetime.fromisoformat(last_trade)
        if datetime.now() < last_time + timedelta(minutes=COOLDOWN_MINUTES):
            print("⏳ Cooldown active")
            return False


    return True


def record_trade():

    account = reset_daily_stats(load_account())

    current_trades = account.get("trades_today", 0)

    if current_trades >= MAX_DAILY_TRADES:
        print("🚫 Daily trade limit reached")
        return False

    if account.get("daily_loss", 0) >= MAX_DAILY_LOSS:
        print("🚫 Daily loss limit reached")
        return False

    account["trades"] = account.get("trades", 0) + 1

    account["trades_today"] = current_trades + 1

    account["last_trade_time"] = datetime.now().isoformat()

    save_account(account)

    return True
