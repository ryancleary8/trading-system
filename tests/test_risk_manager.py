from datetime import datetime

from risk.models.order_request import OrderRequest
from risk.risk_manager import RiskManager
from strategies.models.trading_signal import TradingSignal
from strategies.signals.signal import Signal


def make_order(quantity: int = 100) -> OrderRequest:
    signal = TradingSignal(
        symbol="SPY",
        timestamp=datetime.utcnow(),
        signal=Signal.BUY,
        price=754.68,
        strategy_name="moving_average_cross",
    )

    return OrderRequest(
        signal=signal,
        quantity=quantity,
        estimated_price=754.68,
    )


def test_risk_manager_approves_valid_order():
    risk_manager = RiskManager(max_position_size=1000)

    decision = risk_manager.approve_order(make_order(quantity=100))

    assert decision.approved is True
    assert decision.reason == "Order approved"


def test_risk_manager_rejects_large_position():
    risk_manager = RiskManager(max_position_size=1000)

    decision = risk_manager.approve_order(make_order(quantity=5000))

    assert decision.approved is False
    assert decision.reason == "Maximum position size exceeded"


def test_risk_manager_rejects_when_trading_halted():
    risk_manager = RiskManager()
    risk_manager.halt_trading()

    decision = risk_manager.approve_order(make_order(quantity=100))

    assert decision.approved is False
    assert decision.reason == "Trading halted"


def test_risk_manager_rejects_max_open_positions():
    risk_manager = RiskManager(max_open_positions=2)

    decision = risk_manager.approve_order(
        make_order(quantity=100),
        current_open_positions=2,
    )

    assert decision.approved is False
    assert decision.reason == "Maximum open positions reached"


def test_risk_manager_can_resume_trading():
    risk_manager = RiskManager()
    risk_manager.halt_trading()
    risk_manager.resume_trading()

    decision = risk_manager.approve_order(make_order(quantity=100))

    assert decision.approved is True