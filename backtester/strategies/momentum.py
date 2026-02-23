from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Iterable

from backtester.core.event import SignalEvent, Side
from .base_strategy import BaseStrategy


@dataclass
class MomentumStrategy(BaseStrategy):
    lookback: int

    def on_market(self, event) -> Iterable[SignalEvent]:
        p = event.payload["close"]
        h = event.meta.get("history", None) if event.meta else None
        if h is None:
            return []
        x = h[-self.lookback:] if len(h) >= self.lookback else None
        if x is None:
            return []
        r = np.sign(p - x[0])
        if r > 0:
            yield SignalEvent.of(self.symbol, event.ts, Side.LONG, 1.0)
        elif r < 0:
            yield SignalEvent.of(self.symbol, event.ts, Side.SHORT, 1.0)