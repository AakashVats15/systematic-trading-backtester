from backtester.core.engine import Engine
from backtester.core.data_handler import CSVDataHandler
from backtester.core.order_router import OrderRouter
from backtester.core.execution import RealisticExecutionModel
from backtester.core.portfolio import Portfolio
from backtester.utils.config import ExecutionConfig
from backtester.strategies.test_strategy import TestStrategy


def main():
    data = CSVDataHandler(
        symbol="TEST",
        path=r"E:\Personal\GitHub\Python Code Repo\systematic-trading-backtester\backtester\data\test.csv",
    )

    cfg = ExecutionConfig(
        spread_pct=0.0005,
        proportional_commission_pct=0.0002,
        fixed_commission=0.5,
        slippage_volatility_coeff=1.0,
    )

    execution = RealisticExecutionModel.from_config(cfg)
    router = OrderRouter(data_handler=data, execution_model=execution)
    portfolio = Portfolio(cash=100000)
    strategy = TestStrategy()

    engine = Engine(
        data=data,
        strategy=strategy,
        router=router,
        portfolio=portfolio,
    )

    result = engine.run()
    print(result)


if __name__ == "__main__":
    main()
