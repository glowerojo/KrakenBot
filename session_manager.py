from datetime import datetime
import pytz
import config

TRADING_START = 8
TRADING_END = 12

timezone = pytz.timezone("America/Chicago")


def trading_session_open():

    now = datetime.now(timezone)

    if config.TEST_MODE and config.MODE == "PAPER":
        return True

    hour = now.hour

    if TRADING_START <= hour < TRADING_END:
        return True

    return False


def session_status():

    if trading_session_open():
        return "🟢 SESSION OPEN"

    return "🔴 SESSION CLOSED"
