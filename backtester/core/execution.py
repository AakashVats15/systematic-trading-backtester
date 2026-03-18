from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Dict, Any

from .event import OrderEvent, FillEvent, Side
from backtester.utils.config import ExecutionConfig


@dataclass
class RealisticExecutionModel:
    spread_pct: float
    proportional_commission_pct: float
    fixed_commission: float
    slippage_volatility_coeff: float

    @staticmethod
    def from_config(cfg: ExecutionConfig) -> "RealisticExecutionModel":
        return RealisticExecutionModel(
            spread_pct=cfg.spread_pct,
            proportional_commission_pct=cfg.proportional_commission_pct,
            fixed_commission=cfg.fixed_commission,
            slippage_volatility_coeff=cfg.slippage_volatility_coeff,
        )

    def execute(
        self,
        order: OrderEvent,
        mid_price: float,
        volatility: float,
    ) -> FillEvent:
        direction = 1 if order.side is Side.LONG else -1

        spread_price = mid_price * self.spread_pct
        slippage_price = volatility * self.slippage_volatility_coeff * mid_price

        fill_price = mid_price + direction * (spread_price + slippage_price)

        notional = mid_price * order.quantity
        commission_cost = (
            self.proportional_commission_pct * notional
            + self.fixed_commission
        )

        spread_cost = spread_price * order.quantity
        slippage_cost = slippage_price * order.quantity
        total_cost = commission_cost + spread_cost + slippage_cost

        return FillEvent(
            symbol=order.symbol,
            ts=order.ts,
            side=order.side,
            quantity=order.quantity,
            fill_price=fill_price,
            commission_cost=commission_cost,
            slippage_cost=slippage_cost,
            spread_cost=spread_cost,
            total_cost=total_cost,
            meta={"mid_price": mid_price, "volatility": volatility},
        )