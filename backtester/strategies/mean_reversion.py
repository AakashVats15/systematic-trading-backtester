from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from backtester.core.event import SignalEvent, Side


@dataclass
class MeanReversionStrategy:
    symbol: str
    lookback: int
    threshold: float

    def __post_init__(self):
        self.prices = []

    def on_bar(self, event) -> Optional[SignalEvent]:
        price = event.payload["close"]
        self.prices.append(price)
        if len(self.prices) < self.lookback:
            return None
        w = self.prices[-self.lookback:]
        mean = sum(w) / len(w)
        dev = w[-1] - mean
        if abs(dev) < self.threshold:
            return None
        side = Side.SHORT if dev > 0 else Side.LONG
        return SignalEvent(
            symbol=self.symbol,
            ts=event.ts,
            side=side,
            strength=1.0,
        )