from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Optional


class EventKind(Enum):
    MARKET = auto()
    SIGNAL = auto()
    ORDER = auto()
    FILL = auto()


class Side(Enum):
    LONG = auto()
    SHORT = auto()
    FLAT = auto()


class OrderType(Enum):
    MARKET = auto()
    LIMIT = auto()


@dataclass(frozen=True)
class Event:
    kind: EventKind

    def is_market(self) -> bool:
        return self.kind is EventKind.MARKET

    def is_signal(self) -> bool:
        return self.kind is EventKind.SIGNAL

    def is_order(self) -> bool:
        return self.kind is EventKind.ORDER

    def is_fill(self) -> bool:
        return self.kind is EventKind.FILL


@dataclass(frozen=True)
class MarketEvent(Event):
    symbol: str
    ts: Any
    payload: Dict[str, Any]

    def __init__(
        self,
        symbol: str,
        ts: Any,
        price: float = None,
        payload: Dict[str, Any] = None,
        kind: EventKind = EventKind.MARKET,
    ):
        # Backward compatibility for tests using price=
        if payload is None:
            if price is None:
                raise ValueError("MarketEvent requires either price or payload")
            payload = {
                "open": price,
                "high": price,
                "low": price,
                "close": price,
                "volume": 0.0,
            }

        object.__setattr__(self, "kind", kind)
        object.__setattr__(self, "symbol", symbol)
        object.__setattr__(self, "ts", ts)
        object.__setattr__(self, "payload", payload)

    @property
    def price(self) -> float:
        return self.payload.get("close")

    @staticmethod
    def of(symbol: str, ts: Any, payload: Dict[str, Any]) -> "MarketEvent":
        return MarketEvent(symbol=symbol, ts=ts, payload=payload)


@dataclass(frozen=True)
class SignalEvent(Event):
    symbol: str
    ts: Any
    side: Side
    strength: float

    def __init__(
        self,
        symbol: str,
        ts: Any,
        side: Side,
        strength: float,
        kind: EventKind = EventKind.SIGNAL,
    ):
        object.__setattr__(self, "kind", kind)
        object.__setattr__(self, "symbol", symbol)
        object.__setattr__(self, "ts", ts)
        object.__setattr__(self, "side", side)
        object.__setattr__(self, "strength", strength)

    @staticmethod
    def of(symbol: str, ts: Any, side: Side, strength: float) -> "SignalEvent":
        return SignalEvent(
            symbol=symbol,
            ts=ts,
            side=side,
            strength=strength,
            kind=EventKind.SIGNAL,
        )


@dataclass(frozen=True)
class OrderEvent(Event):
    symbol: str
    ts: Any
    side: Side
    quantity: int
    order_type: OrderType
    limit_price: Optional[float] = None
    meta: Optional[Dict[str, Any]] = None

    @staticmethod
    def market(
        symbol: str,
        ts: Any,
        side: Side,
        quantity: int,
        meta: Optional[Dict[str, Any]] = None,
    ) -> "OrderEvent":
        return OrderEvent(
            kind=EventKind.ORDER,
            symbol=symbol,
            ts=ts,
            side=side,
            quantity=quantity,
            order_type=OrderType.MARKET,
            limit_price=None,
            meta=meta,
        )

    @staticmethod
    def limit(
        symbol: str,
        ts: Any,
        side: Side,
        quantity: int,
        limit_price: float,
        meta: Optional[Dict[str, Any]] = None,
    ) -> "OrderEvent":
        return OrderEvent(
            kind=EventKind.ORDER,
            symbol=symbol,
            ts=ts,
            side=side,
            quantity=quantity,
            order_type=OrderType.LIMIT,
            limit_price=limit_price,
            meta=meta,
        )


# ============================================================
# NEW COST-AWARE FILL EVENT
# ============================================================

@dataclass(frozen=True)
class FillEvent(Event):
    symbol: str
    ts: Any
    side: Side
    quantity: int

    # Execution price after spread + slippage
    fill_price: float

    # Cost components
    commission_cost: float
    slippage_cost: float
    spread_cost: float

    # Aggregated cost
    total_cost: float

    # Optional metadata
    meta: Optional[Dict[str, Any]] = None

    def __init__(
        self,
        symbol: str,
        ts: Any,
        side: Side,
        quantity: int,
        fill_price: float,
        commission_cost: float,
        slippage_cost: float,
        spread_cost: float,
        total_cost: float,
        meta: Optional[Dict[str, Any]] = None,
        kind: EventKind = EventKind.FILL,
    ):
        object.__setattr__(self, "kind", kind)
        object.__setattr__(self, "symbol", symbol)
        object.__setattr__(self, "ts", ts)
        object.__setattr__(self, "side", side)
        object.__setattr__(self, "quantity", quantity)

        object.__setattr__(self, "fill_price", fill_price)

        object.__setattr__(self, "commission_cost", commission_cost)
        object.__setattr__(self, "slippage_cost", slippage_cost)
        object.__setattr__(self, "spread_cost", spread_cost)
        object.__setattr__(self, "total_cost", total_cost)

        object.__setattr__(self, "meta", meta)

    @property
    def gross(self) -> float:
        """Value of the trade ignoring costs."""
        direction = 1 if self.side is Side.LONG else -1
        return self.fill_price * self.quantity * direction

    @property
    def net(self) -> float:
        """Value of the trade after all costs."""
        return self.gross - self.total_cost

    @staticmethod
    def of(
        symbol: str,
        ts: Any,
        side: Side,
        quantity: int,
        fill_price: float,
        commission_cost: float,
        slippage_cost: float,
        spread_cost: float,
        total_cost: float,
        meta: Optional[Dict[str, Any]] = None,
    ) -> "FillEvent":
        return FillEvent(
            symbol=symbol,
            ts=ts,
            side=side,
            quantity=quantity,
            fill_price=fill_price,
            commission_cost=commission_cost,
            slippage_cost=slippage_cost,
            spread_cost=spread_cost,
            total_cost=total_cost,
            meta=meta,
            kind=EventKind.FILL,
        )