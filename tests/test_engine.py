import pytest

from backtester.core.engine import Engine
from backtester.core.event import (
    MarketEvent, SignalEvent, OrderEvent, FillEvent,
    EventKind, Side, OrderType
)


class DummyData:
    def __init__(self):
        self.i = 0
        self.events = [
            MarketEvent(symbol="TEST", ts=1, price=100.0),
            MarketEvent(symbol="TEST", ts=2, price=101.0),
        ]

    def has_next(self):
        return self.i < len(self.events)

    def next(self):
        e = self.events[self.i]
        self.i += 1
        return e


class DummyStrategy:
    def on_bar(self, event):
        return SignalEvent(
            symbol=event.symbol,
            ts=event.ts,
            side=Side.LONG,
            strength=1.0
        )


class DummyRouter:
    def on_signal(self, event):
        yield OrderEvent(
            kind=EventKind.ORDER,
            symbol=event.symbol,
            ts=event.ts,
            side=event.side,
            quantity=1,
            order_type=OrderType.MARKET,
            limit_price=None,
            meta=None,
        )


class DummyExecution:
    def execute(self, order):
        return FillEvent(
            symbol=order.symbol,
            ts=order.ts,
            side=order.side,
            quantity=order.quantity,
            price=100.0,
            commission=0.0,
            slippage=0.0,
            meta=None,
        )


class DummyPortfolio:
    def __init__(self):
        self.fills = []
        self.history = {"equity": [100000.0]}

    def on_fill(self, fill):
        self.fills.append(fill)
        self.history["equity"].append(self.history["equity"][-1] + fill.quantity * fill.price)

    def snapshot(self):
        return self.history


def test_engine_runs():
    e = Engine(
        data=DummyData(),
        strategy=DummyStrategy(),
        router=DummyRouter(),
        execution=DummyExecution(),
        portfolio=DummyPortfolio(),
    )
    result = e.run()
    assert "equity" in result
    assert len(result["equity"]) > 1