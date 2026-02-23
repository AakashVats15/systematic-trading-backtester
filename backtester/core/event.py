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

    @staticmethod
    def of(symbol: str, ts: Any, payload: Dict[str, Any]) -> "MarketEvent":
        return MarketEvent(kind=EventKind.MARKET, symbol=symbol, ts=ts, payload=payload)


@dataclass(frozen=True)
class SignalEvent(Event):
    symbol: str
    ts: Any
    side: Side
    strength: float

    @staticmethod
    def of(symbol: str, ts: Any, side: Side, strength: float) -> "SignalEvent":
        return SignalEvent(kind=EventKind.SIGNAL, symbol=symbol, ts=ts, side=side, strength=strength)


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
    def market(symbol: str, ts: Any, side: Side, quantity: int, meta: Optional[Dict[str, Any]] = None) -> "OrderEvent":
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


@dataclass(frozen=True)
class FillEvent(Event):
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
        return self.price * self.quantity * (1 if self.side is Side.LONG else -1)

    @property
    def net(self) -> float:
        return self.gross - self.commission - self.slippage

    @staticmethod
    def of(
        symbol: str,
        ts: Any,
        side: Side,
        quantity: int,
        price: float,
        commission: float,
        slippage: float = 0.0,
        meta: Optional[Dict[str, Any]] = None,
    ) -> "FillEvent":
        return FillEvent(
            kind=EventKind.FILL,
            symbol=symbol,
            ts=ts,
            side=side,
            quantity=quantity,
            price=price,
            commission=commission,
            slippage=slippage,
            meta=meta,
        )