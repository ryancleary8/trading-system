from datetime import datetime

from execution.execution_simulator import ExecutionSimulator
from risk.models.order_request import OrderRequest
from strategies.models.trading_signal import TradingSignal
from strategies.signals.signal import Signal


def make_order(quantity: int = 100, price: float = 100.0) -> OrderRequest:
    signal = TradingSignal(
        symbol="SPY",
        timestamp=datetime.utcnow(),
        signal=Signal.BUY,
        price=price,
        strategy_name="moving_average_cross",
    )

    return OrderRequest(
        signal=signal,
        quantity=quantity,
        estimated_price=price,
    )


def test_execution_simulator_returns_fill():
    simulator = ExecutionSimulator()
    fill = simulator.execute(make_order())

    assert fill.symbol == "SPY"
    assert fill.signal == Signal.BUY
    assert fill.quantity == 100
    assert fill.fill_price > 0
    assert fill.notional > 0


def test_execution_simulator_applies_costs():
    simulator = ExecutionSimulator(
        commission_per_order=1.0,
        spread_bps=1.0,
        slippage_bps=2.0,
    )

    fill = simulator.execute(make_order(price=100.0))

    assert fill.fill_price == 100.03
    assert fill.commission == 1.0
    assert fill.slippage == 0.02
    assert fill.notional == 10003.0


def test_execution_simulator_respects_quantity():
    simulator = ExecutionSimulator()
    fill = simulator.execute(make_order(quantity=25, price=100.0))

    assert fill.quantity == 25
    assert fill.notional == fill.fill_price * 25