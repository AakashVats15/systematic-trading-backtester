import pytest
from backtester.reporting.report import Report


def test_report_summary_structure():
    h = {
        "equity": [100, 105, 110],
        "positions": [{"TEST": 0}, {"TEST": 5}, {"TEST": 10}],
    }
    r = Report(h)
    s = r.summary()

    assert "performance" in s
    assert "drawdown" in s
    assert "turnover" in s
    assert isinstance(s["performance"], dict)