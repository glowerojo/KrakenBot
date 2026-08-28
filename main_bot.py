import config

from decision import trade_decision
from paper_trader import open_trade
from risk_manager import can_trade
from session_manager import trading_session_open, session_status
from strategy_context import save_context

WATCHLIST = [
    "XBTUSD",
    "ETHUSD"
]


def run_bot():

    print("\n🤖 KrakenBot Started")
    print("Mode:", config.MODE)

    # Check trading session
    print(session_status())

    if not trading_session_open():
        print("⏸ No new trades allowed.")
        return


    # Check risk permission
    if not can_trade():
        print("🚫 Risk manager blocked trading.")
        return


    # Analyze markets
    for pair in WATCHLIST:

        print("\n", pair)

        setup = trade_decision(pair)

        if setup["score"] >= 3:

            print(f"🟢 BUY SIGNAL: {pair}")
            open_trade(pair, setup["price"])

            # Your paper trader handles execution
            # here

        else:

            print(f"{pair}: No trade")


    print("\nBalance check complete")


if __name__ == "__main__":
    run_bot()
