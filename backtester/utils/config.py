from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class Config:
    data: Dict[str, Any]

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)


@dataclass(frozen=True)
class ExecutionConfig:
    spread_pct: float
    proportional_commission_pct: float
    fixed_commission: float
    slippage_volatility_coeff: float

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ExecutionConfig":
        return ExecutionConfig(
            spread_pct=d["spread_pct"],
            proportional_commission_pct=d["proportional_commission_pct"],
            fixed_commission=d["fixed_commission"],
            slippage_volatility_coeff=d["slippage_volatility_coeff"],
        )