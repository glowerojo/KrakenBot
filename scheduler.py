import schedule
import time
from datetime import datetime
from strategy import analyze_market

def trading_session():
    now = datetime.now()

    hour = now.hour

    # Trade only between 8 AM and 12 PM
    if 8 <= hour < 12:
        print("\n🔎 Scanning market...")
        analyze_market("XBTUSD")
        analyze_market("ETHUSD")
    else:
        print("⏸ Outside trading hours")

# Run every 15 minutes
schedule.every(15).minutes.do(trading_session)

print("🤖 KrakenBot started")
print("Trading window: 8:00 AM - 12:00 PM")

while True:
    schedule.run_pending()
    time.sleep(1)