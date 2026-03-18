from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .event import SignalEvent, OrderEvent, EventKind
from .event import Side
from .event import FillEvent


@dataclass
class OrderRouter:
    data_handler: any
    execution_model: any

    def on_signal(self, event: SignalEvent) -> Iterable[OrderEvent]:
        qty = int(event.strength)
        if qty <= 0:
            return []
        yield OrderEvent(
            kind=EventKind.ORDER,
            symbol=event.symbol,
            ts=event.ts,
            side=event.side,
            quantity=qty,
            order_type=event.order_type if hasattr(event, "order_type") else None,
            limit_price=None,
        )

    def on_order(self, order: OrderEvent) -> FillEvent:
        mid = self.data_handler.get_latest_mid_price(order.symbol)
        vol = self.data_handler.get_latest_volatility(order.symbol)
        return self.execution_model.execute(order, mid, vol)
