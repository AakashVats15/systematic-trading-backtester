from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Iterable

from backtester.core.event import SignalEvent, Side
from .base_strategy import BaseStrategy


@dataclass
class MeanReversionStrategy(BaseStrategy):
    lookback: int
    threshold: float

    def on_market(self, event) -> Iterable[SignalEvent]:
        p = event.payload["close"]
        h = event.meta.get("history", None) if event.meta else None
        if h is None:
            return []
        x = h[-self.lookback:] if len(h) >= self.lookback else None
        if x is None:
            return []
        z = (p - np.mean(x)) / (np.std(x) + 1e-12)
        if z > self.threshold:
            yield SignalEvent.of(self.symbol, event.ts, Side.SHORT, abs(z))
        elif z < -self.threshold:
            yield SignalEvent.of(self.symbol, event.ts, Side.LONG, abs(z))