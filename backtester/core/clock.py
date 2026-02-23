from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, Any, Optional


@dataclass
class Clock:
    timeline: Sequence[Any]
    i: int = 0

    def has_next(self) -> bool:
        return self.i < len(self.timeline)

    def next(self) -> Optional[Any]:
        if not self.has_next():
            return None
        t = self.timeline[self.i]
        self.i += 1
        return t

    def now(self) -> Optional[Any]:
        if self.i == 0:
            return None
        return self.timeline[self.i - 1]

    def reset(self) -> None:
        self.i = 0