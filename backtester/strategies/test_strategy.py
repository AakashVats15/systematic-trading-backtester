from dataclasses import dataclass
from backtester.core.event import SignalEvent, Side


@dataclass
class TestStrategy:
    def on_bar(self, event):
        return SignalEvent(
            symbol=event.symbol,
            ts=event.ts,
            side=Side.LONG,
            strength=1.0,
        )