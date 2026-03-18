from __future__ import annotations

from dataclasses import dataclass

from backtester.strategies.base_strategy import BaseStrategy


@dataclass
class MomentumStrategy(BaseStrategy):
    lookback: int = 20

    def generate_signals(self, event):
        if len(self.prices) < self.lookback:
            return None

        window = list(self.prices)[-self.lookback:]
        if window[-1] > window[0]:
            return self.long(event)
        else:
            return self.short(event)
