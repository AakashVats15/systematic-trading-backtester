from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Performance:
    history: Dict[str, Any]

    def _arr(self) -> np.ndarray:
        return np.asarray(self.history["equity"], dtype=float)

    def returns(self) -> np.ndarray:
        x = self._arr()
        if len(x) < 2:
            return np.zeros(0)
        return np.diff(x) / x[:-1]

    def cumulative(self) -> float:
        r = self.returns()
        return float(np.prod(1 + r) - 1)

    def volatility(self) -> float:
        r = self.returns()
        return float(np.std(r)) if len(r) > 1 else 0.0

    def sharpe(self, rf: float = 0.0) -> float:
        r = self.returns()
        if len(r) < 2:
            return 0.0
        ex = r - rf
        s = np.std(ex)
        return float(np.mean(ex) / s) if s > 0 else 0.0

    def summary(self) -> Dict[str, float]:
        return {
            "cumulative": self.cumulative(),
            "volatility": self.volatility(),
            "sharpe": self.sharpe(),
        }