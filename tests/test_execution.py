import pytest
from backtester.core.execution import ExecutionHandler
from backtester.core.event import OrderEvent, EventKind, Side, OrderType


def test_execution_produces_fill_event():
    ex = ExecutionHandler(slippage=0.0, commission=0.0)
    o = OrderEvent(
        kind=EventKind.ORDER,
        symbol="TEST",
        ts=1,
        side=Side.LONG,
        quantity=5,
        order_type=OrderType.MARKET,
        limit_price=None,
        meta=None,
    )
    f = ex.execute(o)

    assert f.symbol == "TEST"
    assert f.quantity == 5
    assert f.price is not None