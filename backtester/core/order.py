from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from .event import Side, OrderType, OrderEvent


@dataclass(frozen=True)
class Order:
    symbol: str
    ts: Any
    side: Side
    quantity: int
    order_type: OrderType
    limit_price: Optional[float] = None
    meta: Optional[Dict[str, Any]] = None

    @staticmethod
    def market(symbol: str, ts: Any, side: Side, quantity: int, meta: Optional[Dict[str, Any]] = None) -> "Order":
        return Order(symbol=symbol, ts=ts, side=side, quantity=quantity, order_type=OrderType.MARKET, limit_price=None, meta=meta)

    @staticmethod
    def limit(
        symbol: str,
        ts: Any,
        side: Side,
        quantity: int,
        limit_price: float,
        meta: Optional[Dict[str, Any]] = None,
    ) -> "Order":
        return Order(symbol=symbol, ts=ts, side=side, quantity=quantity, order_type=OrderType.LIMIT, limit_price=limit_price, meta=meta)

    def to_event(self) -> OrderEvent:
        return OrderEvent(
            kind=OrderEvent.__mro__[1].kind,  # EventKind.ORDER via inheritance chain
            symbol=self.symbol,
            ts=self.ts,
            side=self.side,
            quantity=self.quantity,
            order_type=self.order_type,
            limit_price=self.limit_price,
            meta=self.meta,
        )
