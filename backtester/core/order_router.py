from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .event import SignalEvent, OrderEvent, OrderType, Side, EventKind


@dataclass
class OrderRouter:
    def on_signal(self, event: SignalEvent) -> Iterable[OrderEvent]:
        y = int(event.strength)
        if y <= 0:
            return []
        yield OrderEvent(
            kind=EventKind.ORDER,
            symbol=event.symbol,
            ts=event.ts,
            side=event.side,
            quantity=y,
            order_type=OrderType.MARKET,
            limit_price=None,
        )
