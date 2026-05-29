from risk.models.order_request import OrderRequest
from risk.risk_manager import RiskManager
from execution.execution_simulator import ExecutionSimulator
from data.market_data import MarketData
from models.features.feature_engine import FeatureEngine
from strategies.examples.moving_average_cross import MovingAverageCrossStrategy
from strategies.models.trading_signal import TradingSignal
from strategies.signals.signal import Signal


def test_end_to_end_workflow_generates_approved_fill():
    market_data = MarketData()
    feature_engine = FeatureEngine()
    strategy = MovingAverageCrossStrategy()
    risk_manager = RiskManager()
    execution_simulator = ExecutionSimulator()

    bars = market_data.get_bars("SPY", "daily")
    features = feature_engine.add_features(bars)
    signals = strategy.generate_signals(features)

    latest = signals.iloc[-1]

    trading_signal = TradingSignal(
        symbol="SPY",
        timestamp=latest.name[1],
        signal=latest["signal"],
        price=latest["close"],
        strategy_name="moving_average_cross",
    )

    assert trading_signal.signal in {Signal.BUY, Signal.SELL, Signal.HOLD}

    order = OrderRequest(
        signal=trading_signal,
        quantity=10,
        estimated_price=trading_signal.price,
    )

    decision = risk_manager.approve_order(order)

    assert decision.approved is True

    fill = execution_simulator.execute(order)

    assert fill.symbol == "SPY"
    assert fill.quantity == 10
    assert fill.fill_price > 0
    assert fill.notional > 0