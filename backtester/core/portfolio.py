from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any

from .event import FillEvent, Side


@dataclass
class Portfolio:
    cash: float
    positions: Dict[str, int] = field(default_factory=dict)
    last_price: Dict[str, float] = field(default_factory=dict)
    history: Dict[str, Any] = field(default_factory=lambda: {"equity": [], "positions": []})

    def _update_position(self, symbol: str, qty: int, price: float, side: Side) -> None:
        s = 1 if side is Side.LONG else -1
        self.positions[symbol] = self.positions.get(symbol, 0) + s * qty
        self.last_price[symbol] = price

    def _update_cash(self, event: FillEvent) -> None:
        self.cash -= event.net

    def _equity(self) -> float:
        v = self.cash
        for sym, qty in self.positions.items():
            p = self.last_price.get(sym)
            if p is not None:
                v += qty * p
        return v

    def on_fill(self, event: FillEvent) -> None:
        self._update_position(event.symbol, event.quantity, event.price, event.side)
        self._update_cash(event)
        self.history["equity"].append(self._equity())
        self.history["positions"].append(self.positions.get(event.symbol, 0))  # <-- FIXED

    def snapshot(self) -> Dict[str, Any]:
        return {
            "cash": self.cash,
            "positions": dict(self.positions),
            "equity": self.history["equity"][-1] if self.history["equity"] else self.cash,
            "history": self.history,
        }