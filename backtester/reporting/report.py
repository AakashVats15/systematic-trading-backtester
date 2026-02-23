from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

from backtester.metrics.performance import Performance
from backtester.metrics.drawdown import Drawdown
from backtester.metrics.turnover import Turnover
from backtester.reporting.plots import Plots


@dataclass
class Report:
    history: Dict[str, Any]

    def performance(self) -> Dict[str, float]:
        return Performance(self.history).summary()

    def drawdown(self) -> Dict[str, float]:
        return Drawdown(self.history).summary()

    def turnover(self) -> Dict[str, float]:
        return Turnover(self.history).summary()

    def plots(self) -> Plots:
        return Plots(self.history)

    def summary(self) -> Dict[str, Any]:
        return {
            "performance": self.performance(),
            "drawdown": self.drawdown(),
            "turnover": self.turnover(),
        }