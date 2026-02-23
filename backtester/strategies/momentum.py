from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from backtester.core.event import SignalEvent, Side


@dataclass
class MomentumStrategy:
    symbol: str
    lookback: int

    def __post_init__(self):
        self.prices = []

    def on_bar(self, event) -> Optional[SignalEvent]:
        self.prices.append(event.price)
        if len(self.prices) < self.lookback:
            return None
        w = self.prices[-self.lookback:]
        side = Side.LONG if w[-1] > w[0] else Side.SHORT
        return SignalEvent(
            symbol=self.symbol,
            ts=event.ts,
            side=side,
            strength=1.0,
        )