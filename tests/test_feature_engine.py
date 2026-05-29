from data.market_data import MarketData
from models.features.feature_engine import FeatureEngine


def test_feature_engine_adds_expected_columns():
    market_data = MarketData()
    engine = FeatureEngine()

    df = market_data.get_bars("SPY", "daily")
    features = engine.add_features(df)

    expected_columns = {
        "sma_20",
        "ema_20",
        "rsi_14",
        "atr_14",
        "feature_vwap",
        "volume_avg_20",
    }

    assert expected_columns.issubset(features.columns)


def test_feature_engine_preserves_raw_columns():
    market_data = MarketData()
    engine = FeatureEngine()

    df = market_data.get_bars("SPY", "daily")
    features = engine.add_features(df)

    for column in ["open", "high", "low", "close", "volume", "vwap"]:
        assert column in features.columns


def test_feature_engine_does_not_modify_original_dataframe():
    market_data = MarketData()
    engine = FeatureEngine()

    df = market_data.get_bars("SPY", "daily")
    original_columns = set(df.columns)

    _ = engine.add_features(df)

    assert set(df.columns) == original_columns


def test_feature_engine_outputs_non_empty_features():
    market_data = MarketData()
    engine = FeatureEngine()

    df = market_data.get_bars("SPY", "daily")
    features = engine.add_features(df)

    valid_rows = features.dropna()

    assert not valid_rows.empty
    assert valid_rows["sma_20"].iloc[-1] > 0
    assert valid_rows["ema_20"].iloc[-1] > 0
    assert 0 <= valid_rows["rsi_14"].iloc[-1] <= 100
    assert valid_rows["atr_14"].iloc[-1] > 0
    assert valid_rows["volume_avg_20"].iloc[-1] > 0