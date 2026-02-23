import pytest

from backtester.strategies.momentum import MomentumStrategy
from backtester.strategies.mean_reversion import MeanReversionStrategy
from backtester.core.event import MarketEvent, Side


def test_momentum_strategy_outputs_signal():
    s = MomentumStrategy(symbol="TEST", lookback=3)
    prices = [100, 101, 102]

    sig = None
    for i, p in enumerate(prices):
        sig = s.on_bar(MarketEvent(symbol="TEST", ts=i, price=p))

    assert sig is not None
    assert sig.side in (Side.LONG, Side.SHORT)


def test_mean_reversion_strategy_outputs_signal():
    s = MeanReversionStrategy(symbol="TEST", lookback=3, threshold=1.0)
    prices = [100, 98, 102]

    sig = None
    for i, p in enumerate(prices):
        sig = s.on_bar(MarketEvent(symbol="TEST", ts=i, price=p))

    assert sig is not None
    assert sig.side in (Side.LONG, Side.SHORT)