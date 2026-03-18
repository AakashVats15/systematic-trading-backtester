from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Optional, Protocol, Deque, Dict, Any
from collections import deque

from backtester.core.event import MarketEvent, SignalEvent, Side


class Strategy(Protocol):
    def on_market(self, event: MarketEvent) -> Iterable[SignalEvent]: ...


@dataclass
class BaseStrategy:
    symbol: str
    window: int = 20
    prices: Deque[float] = field(default_factory=lambda: deque(maxlen=500))
    state: Dict[str, Any] = field(default_factory=dict)

    def on_market(self, event: MarketEvent) -> Iterable[SignalEvent]:
        self._update(event)
        sig = self.generate_signals(event)
        if sig is None:
            return []
        if isinstance(sig, SignalEvent):
            return [sig]
        return list(sig)

    def _update(self, event: MarketEvent) -> None:
        self.prices.append(event.payload["close"])

    def generate_signals(self, event: MarketEvent) -> Optional[Iterable[SignalEvent]]:
        return None

    def long(self, event: MarketEvent, strength: float = 1.0) -> SignalEvent:
        return SignalEvent(
            symbol=self.symbol,
            ts=event.ts,
            side=Side.LONG,
            strength=strength,
        )

    def short(self, event: MarketEvent, strength: float = 1.0) -> SignalEvent:
        return SignalEvent(
            symbol=self.symbol,
            ts=event.ts,
            side=Side.SHORT,
            strength=strength,
        )