import pytest
from backtester.core.portfolio import Portfolio
from backtester.core.event import FillEvent, Side


def test_portfolio_updates_equity_and_positions():
    p = Portfolio(cash=100000.0)
    f = FillEvent(
        symbol="TEST",
        ts=1,
        side=Side.LONG,
        quantity=10,
        price=100.0,
        commission=0.0,
        slippage=0.0,
        meta=None,
    )
    p.on_fill(f)

    assert p.positions["TEST"] == 10
    assert p.history["equity"][-1] == 100000.0 + 10 * 100.0
    assert isinstance(p.snapshot(), dict)