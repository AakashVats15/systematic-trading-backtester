from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol

from backtester.core.event import MarketEvent, SignalEvent


class Strategy(Protocol):
    def on_market(self, event: MarketEvent) -> Iterable[SignalEvent]: ...


@dataclass
class BaseStrategy:
    symbol: str

    def on_market(self, event: MarketEvent) -> Iterable[SignalEvent]:
        raise NotImplementedError