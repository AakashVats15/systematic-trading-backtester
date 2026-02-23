from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Dict, Any

from .event import OrderEvent, FillEvent, Side, EventKind


@dataclass
class ExecutionHandler:
    slippage: float = 0.0
    commission: float = 0.0

    def _price(self, payload: Dict[str, Any]) -> float:
        return float(payload["open"])

    def on_order(self, event: OrderEvent) -> Iterable[FillEvent]:
        p = event.price if hasattr(event, "price") else 0.0
        s = self.slippage
        c = self.commission
        y = event.quantity
        side = event.side
        yield FillEvent(
            kind=EventKind.FILL,
            symbol=event.symbol,
            ts=event.ts,
            side=side,
            quantity=y,
            price=p + s if side is Side.LONG else p - s,
            commission=c,
            slippage=s,
        )

    def execute(self, event: OrderEvent) -> FillEvent:
        return next(self.on_order(event))