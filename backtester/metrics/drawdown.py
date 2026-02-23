from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Drawdown:
    history: Dict[str, Any]

    def _arr(self) -> np.ndarray:
        return np.asarray(self.history["equity"], dtype=float)

    def series(self) -> np.ndarray:
        x = self._arr()
        if len(x) == 0:
            return np.zeros(0)
        peak = np.maximum.accumulate(x)
        return (x - peak) / peak

    def max(self) -> float:
        d = self.series()
        return float(np.min(d)) if len(d) else 0.0

    def duration(self) -> int:
        d = self.series()
        if len(d) == 0:
            return 0
        below = d < 0
        if not np.any(below):
            return 0
        idx = np.where(below)[0]
        gaps = np.diff(idx)
        runs = np.split(idx, np.where(gaps != 1)[0] + 1)
        return max(len(r) for r in runs)

    def summary(self) -> Dict[str, float]:
        return {
            "max_drawdown": self.max(),
            "duration": float(self.duration()),
        }