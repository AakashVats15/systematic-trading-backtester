from __future__ import annotations

import logging


def get_logger(name: str) -> logging.Logger:
    l = logging.getLogger(name)
    if not l.handlers:
        h = logging.StreamHandler()
        f = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        h.setFormatter(f)
        l.addHandler(h)
        l.setLevel(logging.INFO)
    return l