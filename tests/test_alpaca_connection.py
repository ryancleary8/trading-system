from dotenv import load_dotenv
from alpaca.trading.client import TradingClient

import os


def main():
    load_dotenv()

    api_key = os.getenv("ALPACA_API_KEY")
    secret_key = os.getenv("ALPACA_SECRET_KEY")

    if not api_key or not secret_key:
        raise ValueError("Missing Alpaca credentials in .env")

    client = TradingClient(
        api_key=api_key,
        secret_key=secret_key,
        paper=True,
    )

    account = client.get_account()

    print("\n=== ALPACA CONNECTION SUCCESSFUL ===")
    print(f"Account Status: {account.status}")
    print(f"Buying Power : {account.buying_power}")
    print(f"Equity       : {account.equity}")


if __name__ == "__main__":
    main()