from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Turnover:
    history: Dict[str, Any]

    def _pos(self) -> np.ndarray:
        p = self.history.get("positions", [])
        return np.asarray(p, dtype=float) if len(p) else np.zeros((0,))

    def _abs_changes(self) -> np.ndarray:
        x = self._pos()
        if len(x) < 2:
            return np.zeros(0)
        return np.abs(np.diff(x))

    def total(self) -> float:
        c = self._abs_changes()
        return float(np.sum(c)) if len(c) else 0.0

    def average(self) -> float:
        c = self._abs_changes()
        return float(np.mean(c)) if len(c) else 0.0

    def summary(self) -> Dict[str, float]:
        return {
            "total_turnover": self.total(),
            "average_turnover": self.average(),
        }