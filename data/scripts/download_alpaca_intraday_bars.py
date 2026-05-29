from pathlib import Path
from datetime import datetime, timedelta, timezone
import os

import pandas as pd
from dotenv import load_dotenv

from alpaca.data.enums import DataFeed
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame


MINUTE_1_DIR = Path("data/raw/minute_1")
MINUTE_5_DIR = Path("data/raw/minute_5")
UNIVERSE_FILE = Path("config/universe_etfs.txt")


def load_symbols() -> list[str]:
    with open(UNIVERSE_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]


def create_client() -> StockHistoricalDataClient:
    load_dotenv(".env")

    api_key = os.getenv("ALPACA_API_KEY")
    secret_key = os.getenv("ALPACA_SECRET_KEY")

    if not api_key or not secret_key:
        raise ValueError("Missing Alpaca credentials")

    return StockHistoricalDataClient(
        api_key=api_key,
        secret_key=secret_key,
    )


def download_intraday(
    client: StockHistoricalDataClient,
    symbol: str,
) -> None:
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=7)

    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Minute,
        start=start,
        end=end,
        feed=DataFeed.IEX,
    )

    bars = client.get_stock_bars(request)

    df = bars.df

    if len(df) == 0:
        print(f"[WARNING] No data returned for {symbol}")
        return

    MINUTE_1_DIR.mkdir(parents=True, exist_ok=True)
    MINUTE_5_DIR.mkdir(parents=True, exist_ok=True)

    minute_1_file = MINUTE_1_DIR / f"{symbol}.parquet"
    df.to_parquet(minute_1_file)

    df_5 = (
        df.reset_index()
        .set_index("timestamp")
        .groupby("symbol")
        .resample("5min")
        .agg(
            {
                "open": "first",
                "high": "max",
                "low": "min",
                "close": "last",
                "volume": "sum",
                "trade_count": "sum",
                "vwap": "mean",
            }
        )
        .dropna()
    )

    minute_5_file = MINUTE_5_DIR / f"{symbol}.parquet"
    df_5.to_parquet(minute_5_file)

    print(
        f"[SUCCESS] {symbol} | "
        f"1m rows={len(df):,} | "
        f"5m rows={len(df_5):,}"
    )


def main() -> None:
    symbols = load_symbols()

    client = create_client()

    for symbol in symbols:
        download_intraday(client, symbol)

    print("\nIntraday download complete.")


if __name__ == "__main__":
    main()