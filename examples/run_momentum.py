from __future__ import annotations

import pandas as pd

from backtester.data.synthetic import RandomWalk
from backtester.data.loaders import DataFrameLoader
from backtester.core.data_handler import CSVDataHandler
from backtester.core.execution import ExecutionHandler
from backtester.core.portfolio import Portfolio
from backtester.core.engine import Engine
from backtester.strategies.momentum import MomentumStrategy
from backtester.reporting.report import Report


def main():
    df = RandomWalk(n=500, start=100.0, vol=1.0, seed=42).generate()
    loader = DataFrameLoader(df)
    data = CSVDataHandler(symbol="TEST", loader=loader)
    exec_handler = ExecutionHandler(slippage=0.0, commission=0.0)
    portfolio = Portfolio(cash=100000.0)
    strat = MomentumStrategy(symbol="TEST", lookback=20)

    engine = Engine(
        data_handler=data,
        execution_handler=exec_handler,
        portfolio=portfolio,
        strategies=[strat],
    )

    engine.run()

    r = Report(portfolio.history)
    print(r.summary())
    r.plots().equity()
    r.plots().drawdown()
    r.plots().positions()


if __name__ == "__main__":
    main()