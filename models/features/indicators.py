import numpy as np
import pandas as pd


def sma(
    series: pd.Series,
    window: int,
) -> pd.Series:
    """
    Simple Moving Average.
    """
    return series.rolling(window=window).mean()


def ema(
    series: pd.Series,
    span: int,
) -> pd.Series:
    """
    Exponential Moving Average.
    """
    return series.ewm(span=span, adjust=False).mean()


def rolling_volume_average(
    volume: pd.Series,
    window: int,
) -> pd.Series:
    """
    Rolling average volume.
    """
    return volume.rolling(window=window).mean()


def vwap(
    df: pd.DataFrame,
) -> pd.Series:
    """
    Volume Weighted Average Price.

    Uses:
        typical_price = (high + low + close) / 3
    """
    typical_price = (
        df["high"] +
        df["low"] +
        df["close"]
    ) / 3

    cumulative_value = (
        typical_price * df["volume"]
    ).cumsum()

    cumulative_volume = df["volume"].cumsum()

    return cumulative_value / cumulative_volume


def rsi(
    series: pd.Series,
    period: int = 14,
) -> pd.Series:
    """
    Relative Strength Index.
    """
    delta = series.diff()

    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)

    avg_gain = gains.rolling(period).mean()
    avg_loss = losses.rolling(period).mean()

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))


def atr(
    df: pd.DataFrame,
    period: int = 14,
) -> pd.Series:
    """
    Average True Range.
    """

    high_low = df["high"] - df["low"]

    high_close = np.abs(
        df["high"] - df["close"].shift(1)
    )

    low_close = np.abs(
        df["low"] - df["close"].shift(1)
    )

    true_range = pd.concat(
        [
            high_low,
            high_close,
            low_close,
        ],
        axis=1,
    ).max(axis=1)

    return true_range.rolling(period).mean()