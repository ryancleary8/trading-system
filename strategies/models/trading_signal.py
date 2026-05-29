from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from strategies.signals.signal import Signal


class TradingSignal(BaseModel):
    """
    Standardized signal object passed between:

    Strategy
        ↓
    Risk Manager
        ↓
    Execution Layer
    """

    symbol: str = Field(..., min_length=1)

    timestamp: datetime

    signal: Signal

    price: float = Field(..., gt=0)

    strategy_name: str = Field(..., min_length=1)

    metadata: Optional[dict] = None