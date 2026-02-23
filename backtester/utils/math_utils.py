from __future__ import annotations

import numpy as np


def zscore(x) -> float:
    x = np.asarray(x, dtype=float)
    m = np.mean(x)
    s = np.std(x) + 1e-12
    return float((x[-1] - m) / s)


def pct_change(x) -> float:
    x = np.asarray(x, dtype=float)
    if len(x) < 2:
        return 0.0
    return float((x[-1] - x[-2]) / x[-2])


def normalize(x):
    x = np.asarray(x, dtype=float)
    s = np.sum(np.abs(x)) + 1e-12
    return x / s