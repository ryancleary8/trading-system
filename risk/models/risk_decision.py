from pydantic import BaseModel, Field


class RiskDecision(BaseModel):
    """
    Result of risk evaluation.

    Produced by:
        RiskManager

    Consumed by:
        ExecutionSimulator
    """

    approved: bool

    reason: str = Field(..., min_length=1)