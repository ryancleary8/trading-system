from typing import Optional

import pandas as pd

from data.data_loader import DataLoader


class MarketData:
    """
    Public market data interface.

    This is the only data access class that strategies,
    features, backtests, and execution systems should use.

    The underlying storage implementation should remain hidden.
    """

    def __init__(
        self,
        data_loader: Optional[DataLoader] = None,
    ) -> None:
        self.data_loader = data_loader or DataLoader()

    def get_bars(
        self,
        symbol: str,
        timeframe: str,
    ) -> pd.DataFrame:
        """
        Return all available bars.
        """
        return self.data_loader.provider.get_bars(
            symbol=symbol,
            timeframe=timeframe,
        )

    def get_latest_bar(
        self,
        symbol: str,
        timeframe: str,
    ) -> pd.Series:
        """
        Return most recent bar.
        """
        return self.data_loader.get_latest_bar(
            symbol=symbol,
            timeframe=timeframe,
        )

    def get_range(
        self,
        symbol: str,
        timeframe: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Return bars inside a date range.
        """
        return self.data_loader.get_range(
            symbol=symbol,
            timeframe=timeframe,
            start=start,
            end=end,
        )

    def list_symbols(
        self,
        timeframe: str,
    ) -> list[str]:
        """
        List symbols available for a timeframe.
        """
        return self.data_loader.list_symbols(
            timeframe=timeframe,
        )