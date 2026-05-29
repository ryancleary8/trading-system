from pydantic import BaseModel, Field


class DataSettings(BaseModel):
    daily_path: str = "data/raw/daily"
    minute_1_path: str = "data/raw/minute_1"
    minute_5_path: str = "data/raw/minute_5"


class RiskSettings(BaseModel):
    max_position_size: int = 1000
    max_open_positions: int = 10
    max_daily_loss: float = 5000.0


class ExecutionSettings(BaseModel):
    commission_per_order: float = 1.0
    spread_bps: float = 1.0
    slippage_bps: float = 2.0


class StrategySettings(BaseModel):
    default_strategy: str = "moving_average_cross"


class BrokerSettings(BaseModel):
    paper_trading: bool = True


class Settings(BaseModel):
    data: DataSettings = Field(default_factory=DataSettings)
    risk: RiskSettings = Field(default_factory=RiskSettings)
    execution: ExecutionSettings = Field(default_factory=ExecutionSettings)
    strategy: StrategySettings = Field(default_factory=StrategySettings)
    broker: BrokerSettings = Field(default_factory=BrokerSettings)


settings = Settings()
