"""
derived_metrics.py

Reproduces every derived metric used in the report that isn't a raw
column in financial_statements_cleaned.csv. Unlike data_cleaning.py,
every function here has been run against the actual cleaned dataset
and its output checked against the numbers quoted in README.md.

Run directly to print all figures referenced in the report:
    python derived_metrics.py
"""

import pandas as pd

DATA_FILE = "../data/financial_statements_cleaned.csv"


def load(path: str = DATA_FILE) -> pd.DataFrame:
    return pd.read_csv(path)


def cagr(start_value: float, end_value: float, years: int) -> float:
    """Compound annual growth/decline rate."""
    return (end_value / start_value) ** (1 / years) - 1


def revenue_index(df: pd.DataFrame) -> pd.DataFrame:
    """Index each company's revenue to its own first year = 100."""
    df = df.sort_values(["Company", "Year"]).copy()
    first_year_revenue = df.groupby("Company")["Revenue"].transform("first")
    df["Revenue_Index"] = df["Revenue"] / first_year_revenue * 100
    return df


def cash_flow_to_net_income_ratio(df: pd.DataFrame) -> pd.DataFrame:
    """Average CFO / average Net Income, per company, across all years."""
    grouped = df.groupby("Company").agg(
        Avg_CFO=("Cash Flow from Operating", "mean"),
        Avg_Net_Income=("Net Income", "mean"),
    )
    grouped["CFO_to_NI_Ratio"] = grouped["Avg_CFO"] / grouped["Avg_Net_Income"]
    return grouped


def implied_shares_outstanding(df: pd.DataFrame) -> pd.DataFrame:
    """Net Income / EPS = implied shares outstanding (millions)."""
    df = df.copy()
    df["Implied_Shares_Outstanding"] = df["Net Income"] / df["Earning Per Share"]
    return df


def revenue_per_employee(df: pd.DataFrame) -> pd.DataFrame:
    """Average revenue per employee across all available years per company
    (full-period average, not a single-year snapshot — see README
    Limitations for why)."""
    tmp = df.copy()
    tmp["Rev_per_Employee_K"] = (tmp["Revenue"] * 1_000_000) / tmp["Number of Employees"] / 1000
    return tmp.groupby("Company")["Rev_per_Employee_K"].mean().sort_values(ascending=False)


def sears_three_line_index(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue, Gross Margin %, and Current Ratio indexed to
    SHLDQ's first year = 100."""
    s = df[df["Company"] == "SHLDQ"].sort_values("Year").copy()
    s["Gross_Margin_%"] = s["Gross Profit"] / s["Revenue"] * 100

    for col, label in [
        ("Revenue", "Revenue_Index"),
        ("Gross_Margin_%", "Gross_Margin_Index"),
        ("Current Ratio", "Current_Ratio_Index"),
    ]:
        base = s[col].iloc[0]
        s[label] = s[col] / base * 100

    return s[["Year", "Revenue_Index", "Gross_Margin_Index", "Current_Ratio_Index"]]


if __name__ == "__main__":
    df = load()

    print("=== Cash Flow to Net Income Ratio (Finding 1: PG&E) ===")
    print(cash_flow_to_net_income_ratio(df).round(2))

    print("\n=== McDonald's Implied Shares Outstanding (Finding 2) ===")
    mcd = implied_shares_outstanding(df[df["Company"] == "MCD"])
    print(mcd[["Year", "Net Income", "Share Holder Equity", "Implied_Shares_Outstanding"]].round(1).to_string(index=False))

    print("\n=== Sears Implied Shares Outstanding (Finding 2, ruling out buybacks) ===")
    shldq = implied_shares_outstanding(df[df["Company"] == "SHLDQ"])
    print(shldq[["Year", "Net Income", "Share Holder Equity", "Implied_Shares_Outstanding"]].round(1).to_string(index=False))

    print("\n=== Sears Three-Line Index (Finding 2) ===")
    print(sears_three_line_index(df).round(1).to_string(index=False))

    print("\n=== Revenue per Employee, full-period average (KPI screening) ===")
    print(revenue_per_employee(df).round(1))

    print("\n=== McDonald's Share Buyback Pace vs Equity Collapse Timing ===")
    mcd_shares = implied_shares_outstanding(df[df["Company"] == "MCD"]).set_index("Year")["Implied_Shares_Outstanding"]
    for start, end in [(2009, 2013), (2013, 2016), (2016, 2019), (2019, 2022)]:
        rate = (mcd_shares[end] / mcd_shares[start] - 1) * 100
        print(f"{start}-{end}: {rate:.1f}%")
