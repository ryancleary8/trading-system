from abc import ABC, abstractmethod

import pandas as pd


class BaseStrategy(ABC):
    """
    Base class for all trading strategies.

    Every strategy must implement generate_signals().

    Strategies consume:
        - market data
        - engineered features

    Strategies produce:
        BUY
        SELL
        HOLD
    """

    @abstractmethod
    def generate_signals(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Generate trading signals.

        Returns a dataframe containing
        at minimum a 'signal' column.
        """
        raise NotImplementedError