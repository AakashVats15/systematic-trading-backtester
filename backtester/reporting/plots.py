from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Plots:
    history: Dict[str, Any]

    def _arr(self) -> np.ndarray:
        return np.asarray(self.history["equity"], dtype=float)

    def equity(self) -> None:
        x = self._arr()
        t = np.arange(len(x))
        plt.figure(figsize=(10, 4))
        plt.plot(t, x, color="black")
        plt.title("Equity")
        plt.tight_layout()
        plt.show()

    def drawdown(self) -> None:
        x = self._arr()
        if len(x) == 0:
            return
        peak = np.maximum.accumulate(x)
        d = (x - peak) / peak
        t = np.arange(len(d))
        plt.figure(figsize=(10, 4))
        plt.plot(t, d, color="red")
        plt.title("Drawdown")
        plt.tight_layout()
        plt.show()

    def positions(self) -> None:
        p = self.history.get("positions", [])
        if not p:
            return
        keys = sorted({k for d in p for k in d})
        t = np.arange(len(p))
        plt.figure(figsize=(10, 4))
        for k in keys:
            y = [d.get(k, 0) for d in p]
            plt.plot(t, y, label=k)
        plt.legend()
        plt.title("Positions")
        plt.tight_layout()
        plt.show()