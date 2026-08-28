import pandas as pd
from strategy_engine import analyze_setup
from backtest_journal import log_trade

STARTING_BALANCE = 100


def run_backtest(data):

    balance = STARTING_BALANCE
    trades = 0
    wins = 0
    losses = 0

    position = None

    for index, row in data.iterrows():

        price = row["close"]
        rsi = row["rsi"]
        ema = row["ema"]

        # STRATEGY DECISION
        setup = analyze_setup(
            "BACKTEST",
            price,
            ema,
            rsi,
            row["volume"] if "volume" in row else 0,
            data["volume"].mean() if "volume" in data else 0
        )

        # BUY RULE
        if position is None:

            if setup["signal"] == "BUY":

                position = {
                    "price": price,
                    "score": setup["score"],
                    "rsi": rsi,
                    "ema": ema,
                    "trend": setup["trend"]
                }

                trades += 1

                print("🟢 BUY")
                print("Entry:", price)
                print("Score:", setup["score"])
                print("Trend:", setup["trend"])

        # SELL RULE
        else:

            target = position["price"] * 1.02
            stop = position["price"] * 0.99

            if price >= target:

                profit = (
                    (price - position["price"])
                    / position["price"]
                    * balance
                )

                balance += profit
                wins += 1

                print("🟢 WIN:", round(profit, 2))

                log_trade(
                    "BACKTEST",
                    position["price"],
                    price,
                    "WIN",
                    profit,
                    position["score"],
                    position["rsi"],
                    position["ema"],
                    position["trend"]
                )

                position = None

            elif price <= stop:

                loss = (
                    (price - position["price"])
                    / position["price"]
                    * balance
                )

                balance += loss
                losses += 1

                print("🔴 LOSS:", round(loss, 2))

                log_trade(
                    "BACKTEST",
                    position["price"],
                    price,
                    "LOSS",
                    loss,
                    position["score"],
                    position["rsi"],
                    position["ema"],
                    position["trend"]
                )

                position = None

    print("\n📊 BACKTEST RESULTS")
    print("------------------")

    print("Starting Balance:", STARTING_BALANCE)
    print("Ending Balance:", round(balance, 2))
    print("Trades:", trades)
    print("Wins:", wins)
    print("Losses:", losses)