"""
data_cleaning.py

Documents the cleaning steps applied to the raw Kaggle dataset
("Financial Statements of Major Companies, 2009-2023") to produce
financial_statements_cleaned.csv.

IMPORTANT NOTE ON PROVENANCE:
This script reconstructs the cleaning logic from project notes. The
original raw file was not available when this script was written, so
it has NOT been executed end-to-end against the raw source. Treat this
as documentation of what was done, not as a tested pipeline. If you
have the original raw file, run this script and diff the output
against financial_statements_cleaned.csv to confirm it reproduces it
exactly before relying on it.

Steps documented:
1. Strip whitespace from column names (raw file had a trailing space
   in "Company ").
2. Normalize inconsistent casing in the Category field (e.g. "Bank"
   and "BANK" collapsed to one value).
3. Filter to 7 companies selected for contrasting financial
   trajectories: AAPL, AMZN, NVDA, MCD, AIG, PCG, SHLDQ.
4. Add a Story_Tag column labeling each company's financial narrative.
5. Add a Revenue_YoY_Growth_% column, computed per company (first year
   per company is left blank, since there's no prior year to compare).
"""

import pandas as pd

RAW_FILE = "Financial_Statements.xls"  # source file name per project notes; actually CSV-formatted
OUTPUT_FILE = "financial_statements_cleaned.csv"

SELECTED_COMPANIES = ["AAPL", "AMZN", "NVDA", "MCD", "AIG", "PCG", "SHLDQ"]

STORY_TAGS = {
    "AAPL": "High Growth, High & Stable Margin",
    "AMZN": "Hyper Growth, Thin Margin",
    "NVDA": "Cyclical Boom-Bust",
    "MCD": "Mature & Defensive",
    "AIG": "Financial Crisis Recovery",
    "PCG": "Operational Disaster (Wildfire Bankruptcy)",
    "SHLDQ": "Structural Decline to Bankruptcy",
}


def clean(raw_path: str = RAW_FILE) -> pd.DataFrame:
    df = pd.read_csv(raw_path)

    # 1. Strip whitespace from column names
    df.columns = [c.strip() for c in df.columns]

    # 2. Normalize Category casing (merge duplicate labels like Bank/BANK)
    if "Category" in df.columns:
        df["Category"] = df["Category"].str.strip().str.title()

    # 3. Filter to the 7 selected companies
    df = df[df["Company"].str.strip().isin(SELECTED_COMPANIES)].copy()

    # 4. Add Story_Tag
    df["Story_Tag"] = df["Company"].map(STORY_TAGS)

    # 5. Add Revenue YoY Growth %, computed within each company, sorted by year
    df = df.sort_values(["Company", "Year"])
    df["Revenue_YoY_Growth_%"] = (
        df.groupby("Company")["Revenue"].pct_change() * 100
    )

    return df


if __name__ == "__main__":
    cleaned = clean()
    cleaned.to_csv(OUTPUT_FILE, index=False)
    print(f"Wrote {len(cleaned)} rows to {OUTPUT_FILE}")
