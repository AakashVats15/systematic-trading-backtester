from __future__ import annotations

from dataclasses import dataclass

from backtester.strategies.base_strategy import BaseStrategy


@dataclass
class TestStrategy(BaseStrategy):
    lookback: int = 5

    def generate_signals(self, event):
        # Not enough data yet
        if len(self.prices) < self.lookback:
            return None

        window = list(self.prices)[-self.lookback:]
        mean_price = sum(window) / len(window)
        last_price = window[-1]

        # Store internal state for debugging or advanced logic
        self.state["mean"] = mean_price
        self.state["last_price"] = last_price
        self.state["deviation"] = last_price - mean_price

        # Simple logic: long if price above mean, short if below
        if last_price > mean_price:
            return self.long(event)
        else:
            return self.short(event)
