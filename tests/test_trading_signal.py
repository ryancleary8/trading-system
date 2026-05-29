from datetime import datetime

import pytest
from pydantic import ValidationError

from strategies.models.trading_signal import TradingSignal
from strategies.signals.signal import Signal


def test_trading_signal_can_be_created():
    signal = TradingSignal(
        symbol="SPY",
        timestamp=datetime.utcnow(),
        signal=Signal.BUY,
        price=754.68,
        strategy_name="moving_average_cross",
    )

    assert signal.symbol == "SPY"
    assert signal.signal == Signal.BUY
    assert signal.price == 754.68


def test_trading_signal_rejects_negative_price():
    with pytest.raises(ValidationError):
        TradingSignal(
            symbol="SPY",
            timestamp=datetime.utcnow(),
            signal=Signal.BUY,
            price=-1,
            strategy_name="moving_average_cross",
        )


def test_trading_signal_rejects_empty_symbol():
    with pytest.raises(ValidationError):
        TradingSignal(
            symbol="",
            timestamp=datetime.utcnow(),
            signal=Signal.BUY,
            price=100,
            strategy_name="moving_average_cross",
        )