from pathlib import Path
from typing import Optional

import pandas as pd


class ParquetDataProvider:
    """
    Low-level market data provider backed by local Parquet files.

    This class is responsible only for loading and filtering data.
    It does not contain strategy, feature, risk, or execution logic.
    """

    TIMEFRAME_PATHS = {
        "daily": Path("data/raw/daily"),
        "1m": Path("data/raw/minute_1"),
        "5m": Path("data/raw/minute_5"),
    }

    def __init__(self) -> None:
        pass

    def get_bars(
        self,
        symbol: str,
        timeframe: str,
    ) -> pd.DataFrame:
        """
        Load all bars for a symbol/timeframe.
        """
        file_path = self._get_file_path(symbol, timeframe)

        if not file_path.exists():
            raise FileNotFoundError(
                f"No data found for symbol={symbol}, timeframe={timeframe}"
            )

        return pd.read_parquet(file_path)

    def get_range(
        self,
        symbol: str,
        timeframe: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Load bars within a date range.
        """
        df = self.get_bars(symbol, timeframe)

        timestamps = df.index.get_level_values("timestamp")

        if start is not None:
            df = df[timestamps >= self._to_utc_timestamp(start)]

        if end is not None:
            timestamps = df.index.get_level_values("timestamp")
            df = df[timestamps <= self._to_utc_timestamp(end)]

        return df

    def get_latest_bar(
        self,
        symbol: str,
        timeframe: str,
    ) -> pd.Series:
        """
        Return the most recent bar.
        """
        df = self.get_bars(symbol, timeframe)

        if df.empty:
            raise ValueError(
                f"No bars available for symbol={symbol}, timeframe={timeframe}"
            )

        return df.iloc[-1]

    def list_symbols(
        self,
        timeframe: str,
    ) -> list[str]:
        """
        List available symbols for a timeframe.
        """
        data_dir = self._get_data_directory(timeframe)

        return sorted(
            file.stem
            for file in data_dir.glob("*.parquet")
        )

    def _to_utc_timestamp(self, value: str) -> pd.Timestamp:
        timestamp = pd.Timestamp(value)
        if timestamp.tzinfo is None:
            return timestamp.tz_localize("UTC")
        return timestamp.tz_convert("UTC")

    def _get_file_path(
        self,
        symbol: str,
        timeframe: str,
    ) -> Path:
        data_dir = self._get_data_directory(timeframe)

        return data_dir / f"{symbol}.parquet"

    def _get_data_directory(
        self,
        timeframe: str,
    ) -> Path:
        if timeframe not in self.TIMEFRAME_PATHS:
            raise ValueError(
                f"Unsupported timeframe '{timeframe}'. "
                f"Supported: {list(self.TIMEFRAME_PATHS.keys())}"
            )

        return self.TIMEFRAME_PATHS[timeframe]