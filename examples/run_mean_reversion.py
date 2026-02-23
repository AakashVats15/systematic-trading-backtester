from __future__ import annotations

import pandas as pd

from backtester.data.synthetic import MeanReverting
from backtester.core.data_handler import DataFrameDataHandler
from backtester.core.execution import ExecutionHandler
from backtester.core.portfolio import Portfolio
from backtester.core.engine import Engine
from backtester.strategies.mean_reversion import MeanReversionStrategy
from backtester.reporting.report import Report
from backtester.core.order_router import OrderRouter   # <-- ADDED


def main():
    df = MeanReverting(n=500, mean=100.0, speed=0.1, vol=1.0, seed=42).generate()
    data = DataFrameDataHandler(symbol="TEST", df=df)
    exec_handler = ExecutionHandler(slippage=0.0, commission=0.0)
    portfolio = Portfolio(cash=100000.0)
    strat = MeanReversionStrategy(symbol="TEST", lookback=20, threshold=1.0)
    router = OrderRouter()                               # <-- ADDED

    engine = Engine(
        data=data,
        strategy=strat,
        router=router,                                   # <-- FIXED
        execution=exec_handler,
        portfolio=portfolio,
    )

    result = engine.run()

    r = Report(portfolio.history)
    print(r.summary())
    r.plots().equity()
    r.plots().drawdown()
    r.plots().positions()


if __name__ == "__main__":
    main()