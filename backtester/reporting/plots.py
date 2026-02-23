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

    def positions(self):
        p = self.history["positions"]

        # Single-asset: p is a list of ints
        if isinstance(p[0], int):
            plt.figure(figsize=(10, 4))
            plt.plot(p, label="position")
            plt.title("Positions")
            plt.xlabel("Time")
            plt.ylabel("Position")
            plt.legend()
            plt.show()
            return self

        # Multi-asset fallback (original behavior)
        keys = sorted({k for d in p for k in d})
        plt.figure(figsize=(10, 4))
        for k in keys:
            plt.plot([d.get(k, 0) for d in p], label=k)
        plt.title("Positions")
        plt.xlabel("Time")
        plt.ylabel("Position")
        plt.legend()
        plt.show()
        return self