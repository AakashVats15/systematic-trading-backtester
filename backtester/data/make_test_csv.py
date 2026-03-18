import pandas as pd

df = pd.DataFrame({
    "open":  [100, 101, 102, 103],
    "high":  [101, 102, 103, 104],
    "low":   [99, 100, 101, 102],
    "close": [100, 101, 102, 103],
    "volume": [1000, 1000, 1000, 1000],
})

df.to_csv(
    r"E:\Personal\GitHub\Python Code Repo\systematic-trading-backtester\backtester\data\test.csv",
    index=False
)
