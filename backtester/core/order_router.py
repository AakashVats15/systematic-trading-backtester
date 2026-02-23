from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .event import SignalEvent, OrderEvent, OrderType, Side


@dataclass
class OrderRouter:
    def on_signal(self, event: SignalEvent) -> Iterable[OrderEvent]:
        y = int(event.strength)
        if y <= 0:
            return []
        yield OrderEvent(
            kind=OrderEvent.__mro__[1].kind,
            symbol=event.symbol,
            ts=event.ts,
            side=event.side,
            quantity=y,
            order_type=OrderType.MARKET,
            limit_price=None,
            meta=event.meta,
        )