from pathlib import Path

import pandas as pd


DATA_DIR = Path("data/raw/daily")


def validate_file(file_path: Path) -> bool:
    df = pd.read_parquet(file_path)

    print(f"\nValidating {file_path.name}")

    required_columns = {
        "open",
        "high",
        "low",
        "close",
        "volume",
        "trade_count",
        "vwap",
    }

    missing = required_columns - set(df.columns)

    if missing:
        print(f"[FAIL] Missing columns: {missing}")
        return False

    if df.empty:
        print("[FAIL] Empty dataset")
        return False

    if df.isnull().sum().sum() > 0:
        print("[FAIL] Null values detected")
        return False

    if (df["high"] < df["low"]).any():
        print("[FAIL] High < Low detected")
        return False

    if (df["volume"] < 0).any():
        print("[FAIL] Negative volume detected")
        return False

    print(f"[PASS] Rows: {len(df):,}")
    print(f"[PASS] Start: {df.index.get_level_values('timestamp').min()}")
    print(f"[PASS] End:   {df.index.get_level_values('timestamp').max()}")

    return True


def main() -> None:
    files = sorted(DATA_DIR.glob("*.parquet"))

    if not files:
        raise FileNotFoundError("No parquet files found")

    passed = 0

    for file_path in files:
        if validate_file(file_path):
            passed += 1

    print("\n========================")
    print(f"Passed: {passed}/{len(files)}")
    print("========================")


if __name__ == "__main__":
    main()