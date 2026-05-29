from datetime import datetime

from execution.models.fill import Fill
from risk.models.order_request import OrderRequest


class ExecutionSimulator:
    """
    Simple execution simulator.

    Models:
    - Commission
    - Spread
    - Slippage
    """

    def __init__(
        self,
        commission_per_order: float = 1.00,
        spread_bps: float = 1.0,
        slippage_bps: float = 2.0,
    ) -> None:
        self.commission_per_order = commission_per_order
        self.spread_bps = spread_bps
        self.slippage_bps = slippage_bps

    def execute(
        self,
        order: OrderRequest,
    ) -> Fill:
        """
        Simulate execution and return a Fill.
        """

        base_price = order.estimated_price

        spread_cost = base_price * (self.spread_bps / 10000)
        slippage_cost = base_price * (self.slippage_bps / 10000)

        fill_price = (
            base_price
            + spread_cost
            + slippage_cost
        )

        notional = fill_price * order.quantity

        return Fill(
            symbol=order.signal.symbol,
            timestamp=datetime.utcnow(),
            signal=order.signal.signal,
            quantity=order.quantity,
            fill_price=fill_price,
            commission=self.commission_per_order,
            slippage=slippage_cost,
            notional=notional,
        )