import pandas as pd

from strategies.base.base_strategy import BaseStrategy
from strategies.signals.signal import Signal


class MovingAverageCrossStrategy(BaseStrategy):
    """
    Simple moving average crossover strategy.

    BUY:
        sma_20 > ema_20

    SELL:
        sma_20 < ema_20

    HOLD:
        otherwise
    """

    def generate_signals(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:

        df = data.copy()

        df["signal"] = Signal.HOLD

        df.loc[
            df["sma_20"] > df["ema_20"],
            "signal",
        ] = Signal.BUY

        df.loc[
            df["sma_20"] < df["ema_20"],
            "signal",
        ] = Signal.SELL

        return df