import pandas as pd
from backtester import run_backtest


data = {
    "close": [
        100,
        101,
        103,
        105,
        108,
        110,
        107,
        106,
        112,
        115
    ],

    "rsi": [
        45,
        52,
        55,
        60,
        65,
        68,
        45,
        50,
        55,
        60
    ],

    "ema": [
        99,
        100,
        101,
        102,
        104,
        106,
        108,
        109,
        110,
        112
    ],
    
    "volume":[
        900,
        1200,
        1300,
        1500,
        1700,
        1800,
        800,
        900,
        1600,
        2000
    ]
}


df = pd.DataFrame(data)


print("\n🤖 KrakenBot Backtest Started")
print("----------------------------")


run_backtest(df)
