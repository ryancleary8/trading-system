from pydantic import BaseModel, Field

from strategies.models.trading_signal import TradingSignal


class OrderRequest(BaseModel):
    """
    Order request generated after a signal
    and before execution.

    This is the object evaluated by
    the RiskManager.
    """

    signal: TradingSignal

    quantity: int = Field(..., gt=0)

    estimated_price: float = Field(..., gt=0)