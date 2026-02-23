from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, Iterable, Protocol, Optional

from .event import Event, EventKind, MarketEvent, SignalEvent, OrderEvent, FillEvent


class DataHandler(Protocol):
    def has_next(self) -> bool: ...
    def next(self) -> Optional[MarketEvent]: ...


class Strategy(Protocol):
    def on_market(self, event: MarketEvent) -> Iterable[SignalEvent]: ...


class OrderRouter(Protocol):
    def on_signal(self, event: SignalEvent) -> Iterable[OrderEvent]: ...


class ExecutionHandler(Protocol):
    def on_order(self, event: OrderEvent) -> Iterable[FillEvent]: ...


class Portfolio(Protocol):
    def on_fill(self, event: FillEvent) -> None: ...
    def snapshot(self) -> dict: ...


@dataclass
class Engine:
    data: DataHandler
    strategy: Strategy
    router: OrderRouter
    execution: ExecutionHandler
    portfolio: Portfolio

    def __post_init__(self) -> None:
        self._q: Deque[Event] = deque()
        self._running: bool = False

    def _enqueue(self, e: Event) -> None:
        self._q.append(e)

    def _dequeue(self) -> Optional[Event]:
        return self._q.popleft() if self._q else None

    def _pump_data(self) -> None:
        if not self.data.has_next():
            self._running = False
            return
        m = self.data.next()
        if m is not None:
            self._enqueue(m)

    def _dispatch_market(self, e: MarketEvent) -> None:
        for s in self.strategy.on_market(e):
            self._enqueue(s)

    def _dispatch_signal(self, e: SignalEvent) -> None:
        for o in self.router.on_signal(e):
            self._enqueue(o)

    def _dispatch_order(self, e: OrderEvent) -> None:
        for f in self.execution.on_order(e):
            self._enqueue(f)

    def _dispatch_fill(self, e: FillEvent) -> None:
        self.portfolio.on_fill(e)

    def _step(self) -> None:
        if not self._q:
            self._pump_data()
        e = self._dequeue()
        if e is None:
            return
        if e.kind is EventKind.MARKET:
            self._dispatch_market(e)  # type: ignore[arg-type]
        elif e.kind is EventKind.SIGNAL:
            self._dispatch_signal(e)  # type: ignore[arg-type]
        elif e.kind is EventKind.ORDER:
            self._dispatch_order(e)  # type: ignore[arg-type]
        elif e.kind is EventKind.FILL:
            self._dispatch_fill(e)  # type: ignore[arg-type]

    def run(self) -> dict:
        self._running = True
        while self._running:
            self._step()
        return self.portfolio.snapshot()