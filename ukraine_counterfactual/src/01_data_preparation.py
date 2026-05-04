"""
01_data_preparation.py

Prepare the clean inflation panel for Part B.

Steps:
1. Load the ECB HICP panel
2. Load the raw Ukraine CPI file
3. Convert Ukraine monthly CPI index into YoY inflation
4. Align dates with the ECB panel
5. Save the final clean dataset
"""

from pathlib import Path
import pandas as pd


# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "data_raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "data_processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def find_date_column(df: pd.DataFrame) -> str:
    """Find the most likely date column."""
    candidates = ["date", "Date", "TIME_PERIOD", "time_period", "month", "Month"]
    for col in candidates:
        if col in df.columns:
            return col
    raise ValueError(f"Could not find a date column. Columns found: {list(df.columns)}")


def load_ecb_panel(file_path: Path) -> pd.DataFrame:
    """Load the ECB inflation panel."""
    print("\nStep 1 - Loading ECB panel")

    df = pd.read_csv(file_path)
    print("[ECB] Raw columns:", list(df.columns))

    date_col = find_date_column(df)
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.rename(columns={date_col: "date"})
    df = df.set_index("date").sort_index()

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    print("[ECB] Shape:", df.shape)
    print("[ECB] Preview:\n", df.head())
    return df


def load_ukraine_cpi(file_path: Path) -> pd.DataFrame:
    """Load the raw Ukraine CPI file and keep the useful column."""
    print("\nStep 2 - Loading Ukraine CPI")

    df = pd.read_csv(file_path)
    print("[UKR CPI] Raw columns:", list(df.columns))
    print("[UKR CPI] Raw shape:", df.shape)

    if "OBS_VALUE" not in df.columns:
        raise ValueError("Column 'OBS_VALUE' was not found in the Ukraine CPI file.")

    df = df[["OBS_VALUE"]].copy()
    df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce")

    # The exam statement indicates a monthly series from Feb 2005 to Dec 2025.
    df.index = pd.date_range(start="2005-02-01", periods=len(df), freq="MS")
    df.index.name = "date"

    print("[UKR CPI] Cleaned shape:", df.shape)
    print("[UKR CPI] Preview:\n", df.head())
    return df


def convert_monthly_index_to_yoy_inflation(df: pd.DataFrame) -> pd.DataFrame:
    """Convert monthly CPI index (previous month = 100) into YoY inflation."""
    print("\nStep 3 - Converting Ukraine CPI to YoY inflation")

    monthly_factor = df["OBS_VALUE"] / 100.0
    yoy_factor = monthly_factor.rolling(window=12).apply(lambda x: x.prod(), raw=True)
    yoy_inflation = (yoy_factor - 1.0) * 100.0

    out = pd.DataFrame({"UKR": yoy_inflation}, index=df.index)

    print("[UKR YoY] Preview:\n", out.head(15))
    return out


def merge_and_clean(df_ecb: pd.DataFrame, df_ukr: pd.DataFrame) -> pd.DataFrame:
    """Merge ECB data with Ukraine inflation and drop missing values."""
    print("\nStep 4 - Merging and cleaning")

    df = df_ecb.join(df_ukr, how="inner")
    print("[Merged] Shape before dropna:", df.shape)

    df = df.dropna()
    print("[Merged] Shape after dropna:", df.shape)
    print("[Merged] Preview:\n", df.head())
    print("[Merged] Last rows:\n", df.tail())

    return df


def save_output(df: pd.DataFrame, output_path: Path) -> None:
    """Save the final panel to CSV."""
    print("\nStep 5 - Saving output")

    df.to_csv(output_path)
    print(f"Saved clean inflation panel to: {output_path}")


def main() -> None:
    ecb_path = RAW_DIR / "data_ecb_hicp_panel.csv"
    ukr_path = RAW_DIR / "data_ukraine_cpi_raw.csv"
    output_path = PROCESSED_DIR / "inflation_panel.csv"

    if not ecb_path.exists():
        raise FileNotFoundError(f"Missing file: {ecb_path}")
    if not ukr_path.exists():
        raise FileNotFoundError(f"Missing file: {ukr_path}")

    df_ecb = load_ecb_panel(ecb_path)
    df_ukr_raw = load_ukraine_cpi(ukr_path)
    df_ukr_yoy = convert_monthly_index_to_yoy_inflation(df_ukr_raw)
    df_final = merge_and_clean(df_ecb, df_ukr_yoy)
    print("\nExtra check - final panel preview:")
    print(df_final.head(20))
   
    save_output(df_final, output_path)


if __name__ == "__main__":
    main()


print(df.head(20))
print(df[["TIME_PERIOD", "OBS_VALUE"]].head(20))
print(df[["TIME_PERIOD", "OBS_VALUE"]].tail(20))