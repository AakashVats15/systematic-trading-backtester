from __future__ import annotations

import pandas as pd
from dataclasses import dataclass
from typing import Optional, Dict, Any

from .event import MarketEvent, EventKind


@dataclass
class CSVDataHandler:
    symbol: str
    path: str

    def __post_init__(self) -> None:
        df = pd.read_csv(self.path)
        df.columns = [c.lower() for c in df.columns]
        self._ts = df.index
        self._df = df
        self._i = 0
        self._n = len(df)

    def has_next(self) -> bool:
        return self._i < self._n

    def _slice(self) -> Dict[str, Any]:
        r = self._df.iloc[self._i]
        return {
            "open": float(r["open"]),
            "high": float(r["high"]),
            "low": float(r["low"]),
            "close": float(r["close"]),
            "volume": float(r.get("volume", 0.0)),
        }

    def next(self) -> Optional[MarketEvent]:
        if not self.has_next():
            return None
        ts = self._ts[self._i]
        payload = self._slice()
        self._i += 1
        return MarketEvent.of(self.symbol, ts, payload)