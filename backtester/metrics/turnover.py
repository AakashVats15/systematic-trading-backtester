from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Turnover:
    history: Dict[str, Any]

    def _pos(self) -> np.ndarray:
        p = self.history.get("positions", [])

        if not p:
            return np.zeros((0,))

        # Case 1: dict-based positions (test suite format or multi-asset)
        if isinstance(p[0], dict):
            vals = []
            for d in p:
                if not d:
                    vals.append(0.0)
                else:
                    # Extract the first (and only) symbol's position
                    vals.append(float(next(iter(d.values()))))
            return np.asarray(vals, dtype=float)

        # Case 2: scalar positions (your backtester)
        return np.asarray(p, dtype=float)

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