from risk.models.order_request import OrderRequest
from risk.models.risk_decision import RiskDecision


class RiskManager:
    """
    Central risk control engine.

    Phase 2 controls:

    - Maximum position size
    - Maximum open positions
    - Trading halt (kill switch)
    """

    def __init__(
        self,
        max_position_size: int = 1000,
        max_open_positions: int = 10,
        trading_halted: bool = False,
    ) -> None:
        self.max_position_size = max_position_size
        self.max_open_positions = max_open_positions
        self.trading_halted = trading_halted

    def approve_order(
        self,
        order: OrderRequest,
        current_open_positions: int = 0,
    ) -> RiskDecision:
        """
        Evaluate an order request.
        """

        if self.trading_halted:
            return RiskDecision(
                approved=False,
                reason="Trading halted",
            )

        if order.quantity > self.max_position_size:
            return RiskDecision(
                approved=False,
                reason="Maximum position size exceeded",
            )

        if current_open_positions >= self.max_open_positions:
            return RiskDecision(
                approved=False,
                reason="Maximum open positions reached",
            )

        return RiskDecision(
            approved=True,
            reason="Order approved",
        )

    def halt_trading(self) -> None:
        """
        Activate kill switch.
        """
        self.trading_halted = True

    def resume_trading(self) -> None:
        """
        Disable kill switch.
        """
        self.trading_halted = False