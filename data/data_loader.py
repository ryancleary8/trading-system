from typing import Optional

import pandas as pd

from data.providers.parquet_provider import ParquetDataProvider


class DataLoader:
    def __init__(self, provider: Optional[ParquetDataProvider] = None) -> None:
        self.provider = provider or ParquetDataProvider()

    def get_daily(self, symbol: str) -> pd.DataFrame:
        return self.provider.get_bars(symbol=symbol, timeframe="daily")

    def get_1m(self, symbol: str) -> pd.DataFrame:
        return self.provider.get_bars(symbol=symbol, timeframe="1m")

    def get_5m(self, symbol: str) -> pd.DataFrame:
        return self.provider.get_bars(symbol=symbol, timeframe="5m")

    def get_range(
        self,
        symbol: str,
        timeframe: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> pd.DataFrame:
        return self.provider.get_range(symbol=symbol, timeframe=timeframe, start=start, end=end)

    def get_latest_bar(self, symbol: str, timeframe: str) -> pd.Series:
        return self.provider.get_latest_bar(symbol=symbol, timeframe=timeframe)

    def list_symbols(self, timeframe: str) -> list[str]:
        return self.provider.list_symbols(timeframe=timeframe)
