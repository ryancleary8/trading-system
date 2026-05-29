from data.market_data import MarketData
from models.features.feature_engine import FeatureEngine
from strategies.examples.moving_average_cross import MovingAverageCrossStrategy
from strategies.registry import StrategyRegistry
from strategies.signals.signal import Signal


def test_moving_average_cross_strategy_generates_signal_column():
    market_data = MarketData()
    feature_engine = FeatureEngine()
    strategy = MovingAverageCrossStrategy()

    df = market_data.get_bars("SPY", "daily")
    features = feature_engine.add_features(df)
    signals = strategy.generate_signals(features)

    assert "signal" in signals.columns
    assert not signals.empty


def test_moving_average_cross_strategy_uses_valid_signals():
    market_data = MarketData()
    feature_engine = FeatureEngine()
    strategy = MovingAverageCrossStrategy()

    df = market_data.get_bars("SPY", "daily")
    features = feature_engine.add_features(df)
    signals = strategy.generate_signals(features)

    valid_signals = {Signal.BUY, Signal.SELL, Signal.HOLD}

    assert set(signals["signal"].dropna().unique()).issubset(valid_signals)


def test_strategy_registry_registers_and_retrieves_strategy():
    registry = StrategyRegistry()

    registry.register(
        "moving_average_cross",
        MovingAverageCrossStrategy,
    )

    strategy_class = registry.get("moving_average_cross")

    assert strategy_class is MovingAverageCrossStrategy
    assert registry.list_strategies() == ["moving_average_cross"]