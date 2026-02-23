from __future__ import annotations

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Optional


@dataclass
class RandomWalk:
    n: int
    start: float = 100.0
    vol: float = 1.0
    seed: Optional[int] = None

    def generate(self) -> pd.DataFrame:
        if self.seed is not None:
            np.random.seed(self.seed)
        r = np.random.randn(self.n) * self.vol
        x = self.start + np.cumsum(r)
        return pd.DataFrame({"close": x})


@dataclass
class MeanReverting:
    n: int
    mean: float = 100.0
    speed: float = 0.1
    vol: float = 1.0
    seed: Optional[int] = None

    def generate(self) -> pd.DataFrame:
        if self.seed is not None:
            np.random.seed(self.seed)
        x = np.zeros(self.n)
        x[0] = self.mean
        for i in range(1, self.n):
            x[i] = x[i - 1] + self.speed * (self.mean - x[i - 1]) + self.vol * np.random.randn()
        return pd.DataFrame({"close": x})


@dataclass
class Trending:
    n: int
    start: float = 100.0
    drift: float = 0.05
    vol: float = 1.0
    seed: Optional[int] = None

    def generate(self) -> pd.DataFrame:
        if self.seed is not None:
            np.random.seed(self.seed)
        r = self.drift + np.random.randn(self.n) * self.vol
        x = self.start + np.cumsum(r)
        return pd.DataFrame({"close": x})