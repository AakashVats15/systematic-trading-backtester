from __future__ import annotations

import pandas as pd

from backtester.data.synthetic import RandomWalk
from backtester.core.data_handler import DataFrameDataHandler
from backtester.core.execution import ExecutionHandler
from backtester.core.portfolio import Portfolio
from backtester.core.engine import Engine
from backtester.strategies.momentum import MomentumStrategy
from backtester.reporting.report import Report


def main():
    df = RandomWalk(n=500, start=100.0, vol=1.0, seed=42).generate()
    data = DataFrameDataHandler(symbol="TEST", df=df)
    exec_handler = ExecutionHandler(slippage=0.0, commission=0.0)
    portfolio = Portfolio(cash=100000.0)
    strat = MomentumStrategy(symbol="TEST", lookback=20)

    engine = Engine(
        data=data,
        strategy=strat,
        router=None,  # engine will attach router internally if needed
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