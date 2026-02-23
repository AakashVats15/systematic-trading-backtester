import pytest

from backtester.metrics.performance import Performance
from backtester.metrics.drawdown import Drawdown
from backtester.metrics.turnover import Turnover


def test_performance_summary():
    h = {"equity": [100, 105, 110]}
    p = Performance(h)
    s = p.summary()

    assert s["cumulative"] > 0
    assert s["volatility"] >= 0
    assert "sharpe" in s


def test_drawdown_summary():
    h = {"equity": [100, 120, 90, 95]}
    d = Drawdown(h)
    s = d.summary()

    assert s["max_drawdown"] < 0
    assert s["duration"] >= 0


def test_turnover_summary():
    h = {"positions": [{"TEST": 0}, {"TEST": 5}, {"TEST": 10}]}
    t = Turnover(h)
    s = t.summary()

    assert s["total_turnover"] > 0
    assert s["average_turnover"] > 0