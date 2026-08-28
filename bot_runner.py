import schedule
import time
from datetime import datetime
import pytz
import subprocess


TRADING_START = 8
TRADING_END = 12

timezone = pytz.timezone("America/Chicago")


def run_bot():

    now = datetime.now(timezone)
    hour = now.hour

    if TRADING_START <= hour < TRADING_END:

        print("\n⏰ Trading window active")
        print(now.strftime("%Y-%m-%d %H:%M"))

        subprocess.run(
            ["python3", "main_bot.py"]
        )

    else:

        print("\n⏸ Outside trading hours")
        print(now.strftime("%Y-%m-%d %H:%M"))


# Run immediately once
run_bot()


# Then every 15 minutes
schedule.every(15).minutes.do(run_bot)


print("\n🤖 KrakenBot Runner Started")
print("Trading window: 8 AM - 12 PM Central")


while True:

    schedule.run_pending()

    time.sleep(1)
