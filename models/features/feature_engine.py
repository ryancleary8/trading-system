import pandas as pd

from models.features.indicators import (
    atr,
    ema,
    rolling_volume_average,
    rsi,
    sma,
    vwap,
)


class FeatureEngine:
    """
    Centralized feature generation engine.

    All strategies should consume features generated here
    rather than calculating indicators independently.

    This ensures consistency across:
    - backtests
    - research
    - live trading
    """

    def __init__(
        self,
        sma_window: int = 20,
        ema_window: int = 20,
        rsi_period: int = 14,
        atr_period: int = 14,
        volume_window: int = 20,
    ) -> None:
        self.sma_window = sma_window
        self.ema_window = ema_window
        self.rsi_period = rsi_period
        self.atr_period = atr_period
        self.volume_window = volume_window

    def add_features(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Return a new dataframe containing engineered features.
        """
        features = df.copy()

        features[f"sma_{self.sma_window}"] = sma(
            features["close"],
            self.sma_window,
        )

        features[f"ema_{self.ema_window}"] = ema(
            features["close"],
            self.ema_window,
        )

        features[f"rsi_{self.rsi_period}"] = rsi(
            features["close"],
            self.rsi_period,
        )

        features[f"atr_{self.atr_period}"] = atr(
            features,
            self.atr_period,
        )

        features["feature_vwap"] = vwap(features)

        features[f"volume_avg_{self.volume_window}"] = (
            rolling_volume_average(
                features["volume"],
                self.volume_window,
            )
        )

        return features