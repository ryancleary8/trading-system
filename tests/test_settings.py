from config.settings.settings import (
    DataSettings,
    ExecutionSettings,
    RiskSettings,
    Settings,
    StrategySettings,
)


def test_settings_load():
    settings = Settings()

    assert isinstance(settings.data, DataSettings)
    assert isinstance(settings.risk, RiskSettings)
    assert isinstance(settings.execution, ExecutionSettings)
    assert isinstance(settings.strategy, StrategySettings)


def test_risk_defaults():
    settings = Settings()

    assert settings.risk.max_position_size == 1000
    assert settings.risk.max_open_positions == 10
    assert settings.risk.max_daily_loss == 5000.0


def test_execution_defaults():
    settings = Settings()

    assert settings.execution.commission_per_order == 1.0
    assert settings.execution.spread_bps == 1.0
    assert settings.execution.slippage_bps == 2.0


def test_strategy_defaults():
    settings = Settings()

    assert settings.strategy.default_strategy == "moving_average_cross"