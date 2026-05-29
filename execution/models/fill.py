from datetime import datetime

from pydantic import BaseModel, Field

from strategies.signals.signal import Signal


class Fill(BaseModel):
    """
    Simulated execution result.

    Produced by:
        ExecutionSimulator

    Consumed by:
        Backtests
        Performance analytics
        Portfolio accounting
    """

    symbol: str = Field(..., min_length=1)

    timestamp: datetime

    signal: Signal

    quantity: int = Field(..., gt=0)

    fill_price: float = Field(..., gt=0)

    commission: float = Field(..., ge=0)

    slippage: float = Field(..., ge=0)

    notional: float = Field(..., gt=0)