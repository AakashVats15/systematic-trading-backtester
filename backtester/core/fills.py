from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from .event import Side, FillEvent


@dataclass(frozen=True)
class Fill:
    symbol: str
    ts: Any
    side: Side
    quantity: int
    price: float
    commission: float
    slippage: float = 0.0
    meta: Optional[Dict[str, Any]] = None

    @property
    def gross(self) -> float:
        s = 1 if self.side is Side.LONG else -1
        return self.price * self.quantity * s

    @property
    def net(self) -> float:
        return self.gross - self.commission - self.slippage

    def to_event(self) -> FillEvent:
        return FillEvent.of(
            symbol=self.symbol,
            ts=self.ts,
            side=self.side,
            quantity=self.quantity,
            price=self.price,
            commission=self.commission,
            slippage=self.slippage,
            meta=self.meta,
        )