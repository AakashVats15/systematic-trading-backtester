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

    def __post_init__(self):
        self.initial_cash = self.cash

    def on_fill(self, fill: FillEvent):
        symbol = fill.symbol
        qty = fill.quantity if fill.side is Side.LONG else -fill.quantity

        self.positions[symbol] = self.positions.get(symbol, 0) + qty
        self.last_price[symbol] = fill.fill_price
        self.cash -= fill.total_cost

        position_value = sum(
            self.positions[s] * self.last_price.get(s, 0.0)
            for s in self.positions
        )
        equity = self.cash + position_value

        self.history["equity"].append(equity)
        self.history["positions"].append(self.positions.copy())

    def snapshot(self) -> Dict[str, Any]:
        equity = self.history["equity"][-1] if self.history["equity"] else self.cash
        return {
            "cash": self.cash,
            "positions": dict(self.positions),
            "equity": equity,
            "history": self.history,
        }