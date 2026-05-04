"""
02_build_euro_factor.py

Construct the European inflation factor using PCA.

Steps:
1. Load cleaned inflation panel
2. Select Euro Area countries (exclude Ukraine)
3. Standardize the data
4. Run PCA
5. Extract first principal component
6. Save the factor
"""

from pathlib import Path
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "data_processed" / "inflation_panel.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "data_processed" / "euro_inflation_factor.csv"


def main():

    # Step 1. Load cleaned inflation panel
    print("\nStep 1 - Loading cleaned inflation panel")
    df = pd.read_csv(DATA_PATH, parse_dates=["date"], index_col="date")
    print("[Data] Shape:", df.shape)
    print("[Data] Preview:\n", df.head())

    # Step 2. Select Euro Area countries (exclude Ukraine)
    print("\nStep 2 - Selecting Euro Area countries")
    euro_df = df.drop(columns=["UKR"])
    print("[Euro] Shape:", euro_df.shape)
    print("[Euro] Columns:", list(euro_df.columns))

    # Step 3. Standardize the data
    print("\nStep 3 - Standardizing the data")
    scaler = StandardScaler()
    euro_scaled = scaler.fit_transform(euro_df)

    # Step 4. Run PCA
    print("\nStep 4 - Running PCA")
    pca = PCA(n_components=1)
    factor = pca.fit_transform(euro_scaled)
    explained_variance = pca.explained_variance_ratio_[0]
    print(f"[PCA] Explained variance (component 1): {explained_variance:.4f}")

    # Step 5. Extract first principal component
    print("\nStep 5 - Extracting first principal component")
    factor_df = pd.DataFrame(
        factor,
        index=euro_df.index,
        columns=["EURO_FACTOR"]
    )
    print("[Factor] Preview:\n", factor_df.head())

    # Step 6. Save the factor
    print("\nStep 6 - Saving the factor")
    factor_df.to_csv(OUTPUT_PATH)
    print(f"Saved Euro inflation factor to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()