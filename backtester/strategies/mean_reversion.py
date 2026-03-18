from __future__ import annotations

from dataclasses import dataclass

from backtester.strategies.base_strategy import BaseStrategy


@dataclass
class MeanReversionStrategy(BaseStrategy):
    lookback: int = 20
    threshold: float = 0.0

    def generate_signals(self, event):
        if len(self.prices) < self.lookback:
            return None

        window = list(self.prices)[-self.lookback:]
        mean = sum(window) / len(window)
        deviation = window[-1] - mean

        # No signal if deviation is too small
        if abs(deviation) < self.threshold:
            return None

        # If price is above mean → short
        if deviation > 0:
            return self.short(event)

        # If price is below mean → long
        return self.long(event)