from pathlib import Path
from datetime import datetime, timedelta
import os

import pandas as pd
from dotenv import load_dotenv

from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.enums import DataFeed


DATA_DIR = Path("data/raw/daily")
UNIVERSE_FILE = Path("config/universe_etfs.txt")


def load_symbols() -> list[str]:
    with open(UNIVERSE_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]


def create_client() -> StockHistoricalDataClient:
    load_dotenv()

    api_key = os.getenv("ALPACA_API_KEY")
    secret_key = os.getenv("ALPACA_SECRET_KEY")

    if not api_key or not secret_key:
        raise ValueError("Missing Alpaca credentials in .env")

    return StockHistoricalDataClient(
        api_key=api_key,
        secret_key=secret_key,
    )


def download_symbol(
    client: StockHistoricalDataClient,
    symbol: str,
) -> None:
    end = datetime.utcnow()
    start = end - timedelta(days=365 * 5)

    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Day,
        start=start,
        end=end,
        feed=DataFeed.IEX,
    )

    bars = client.get_stock_bars(request)

    df = bars.df

    if len(df) == 0:
        print(f"[WARNING] No data returned for {symbol}")
        return

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_file = DATA_DIR / f"{symbol}.parquet"

    df.to_parquet(output_file)

    print(
        f"[SUCCESS] {symbol}: "
        f"{len(df):,} rows saved -> {output_file}"
    )


def main() -> None:
    symbols = load_symbols()

    print(f"Downloading data for {len(symbols)} ETFs...")

    client = create_client()

    for symbol in symbols:
        download_symbol(client, symbol)

    print("\nDownload complete.")


if __name__ == "__main__":
    main()