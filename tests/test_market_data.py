import pytest

from data.market_data import MarketData


def test_market_data_lists_daily_symbols():
    market_data = MarketData()

    symbols = market_data.list_symbols("daily")

    assert "SPY" in symbols
    assert "QQQ" in symbols
    assert len(symbols) >= 10


def test_market_data_loads_daily_bars():
    market_data = MarketData()

    df = market_data.get_bars("SPY", "daily")

    assert not df.empty
    assert {"open", "high", "low", "close", "volume"}.issubset(df.columns)


def test_market_data_gets_latest_bar():
    market_data = MarketData()

    latest = market_data.get_latest_bar("SPY", "daily")

    assert latest["close"] > 0
    assert latest["volume"] >= 0


def test_market_data_gets_date_range():
    market_data = MarketData()

    df = market_data.get_range(
        symbol="SPY",
        timeframe="daily",
        start="2025-01-01",
        end="2025-03-01",
    )

    assert not df.empty
    assert len(df) == 39


def test_market_data_rejects_invalid_timeframe():
    market_data = MarketData()

    with pytest.raises(ValueError):
        market_data.get_bars("SPY", "bad_timeframe")