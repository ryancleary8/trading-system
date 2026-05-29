from pathlib import Path

import pandas as pd


MINUTE_1_DIR = Path("data/raw/minute_1")
MINUTE_5_DIR = Path("data/raw/minute_5")


def validate_directory(data_dir: Path, label: str) -> bool:
    files = sorted(data_dir.glob("*.parquet"))

    if not files:
        print(f"[FAIL] No files found in {data_dir}")
        return False

    passed = 0

    print(f"\n=== Validating {label} Data ===")

    for file_path in files:
        df = pd.read_parquet(file_path)

        print(f"\n{file_path.name}")

        if df.empty:
            print("[FAIL] Empty dataset")
            continue

        if df.isnull().sum().sum() > 0:
            print("[FAIL] Null values detected")
            continue

        if (df["high"] < df["low"]).any():
            print("[FAIL] High < Low detected")
            continue

        if (df["volume"] < 0).any():
            print("[FAIL] Negative volume detected")
            continue

        print(f"[PASS] Rows: {len(df):,}")

        if "timestamp" in df.index.names:
            print(
                f"[PASS] Range: "
                f"{df.index.get_level_values('timestamp').min()} -> "
                f"{df.index.get_level_values('timestamp').max()}"
            )

        passed += 1

    print(f"\n{label}: {passed}/{len(files)} files passed")

    return passed == len(files)


def main() -> None:
    minute_1_ok = validate_directory(MINUTE_1_DIR, "1-Minute")
    minute_5_ok = validate_directory(MINUTE_5_DIR, "5-Minute")

    print("\n========================")

    if minute_1_ok and minute_5_ok:
        print("ALL INTRADAY VALIDATION PASSED")
    else:
        print("VALIDATION FAILED")

    print("========================")


if __name__ == "__main__":
    main()