"""Superstore sales analysis: data cleaning, KPIs and dashboard data export.

Run: python analysis-1-fixed.py
Keep the Superstore CSV in the same folder as this script.
"""
import json
import sys
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent


def find_csv():
    """Find the Superstore CSV next to this script."""
    candidates = sorted(
        p for p in BASE.glob("*.csv")
        if "superstore" in p.name.lower() and "cleaned" not in p.name.lower()
    )
    if not candidates:
        sys.exit(
            "ERROR: Superstore CSV not found. Put 'Sample_-_Superstore.csv' "
            f"in this folder: {BASE}"
        )
    return candidates[0]


def normalise_columns(df):
    df.columns = [
        str(c).strip().replace(" ", "_").replace("-", "_")
        for c in df.columns
    ]
    # Handle common variations in column names.
    aliases = {
        "Order_Date": ("Order_Date", "OrderDate"),
        "Ship_Date": ("Ship_Date", "ShipDate"),
        "Order_ID": ("Order_ID", "Order_Id", "OrderID"),
        "Customer_ID": ("Customer_ID", "Customer_Id", "CustomerID"),
        "Sub_Category": ("Sub_Category", "SubCategory"),
        "Product_Name": ("Product_Name", "ProductName"),
    }
    rename = {}
    for wanted, variants in aliases.items():
        for variant in variants:
            if variant in df.columns:
                rename[variant] = wanted
                break
    return df.rename(columns=rename)


def parse_dates(series):
    # format='mixed' is available in newer pandas versions only.
    try:
        return pd.to_datetime(series, format="mixed", errors="coerce")
    except (TypeError, ValueError):
        return pd.to_datetime(series, errors="coerce")


def load_and_clean(path):
    try:
        df = pd.read_csv(path, encoding="latin1")
    except (OSError, pd.errors.ParserError, UnicodeError) as exc:
        sys.exit(f"ERROR: Could not read CSV file '{path.name}': {exc}")

    df = normalise_columns(df)
    required = [
        "Order_Date", "Ship_Date", "Sales", "Profit", "Order_ID",
        "Customer_ID", "Quantity", "Discount", "Category", "Region",
        "Segment", "Sub_Category", "Product_Name", "State",
    ]
    missing = [column for column in required if column not in df.columns]
    if missing:
        sys.exit(
            "ERROR: CSV is missing required columns: "
            + ", ".join(missing)
            + ". Please check that you are using the Superstore dataset."
        )

    df["Order_Date"] = parse_dates(df["Order_Date"])
    df["Ship_Date"] = parse_dates(df["Ship_Date"])
    df = df.dropna(subset=["Order_Date", "Ship_Date"]).drop_duplicates()

    for column in ["Sales", "Profit", "Quantity", "Discount"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(subset=["Sales", "Profit", "Quantity", "Discount"])
    df["Year"] = df["Order_Date"].dt.year
    df["Month"] = df["Order_Date"].dt.strftime("%Y-%m")
    df["Profit_Margin"] = df["Profit"].div(df["Sales"].where(df["Sales"].ne(0)))
    df["Ship_Days"] = (df["Ship_Date"] - df["Order_Date"]).dt.days
    return df


def summarise(df, by):
    grouped = df.groupby(by, observed=True, dropna=False).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique"),
        Qty=("Quantity", "sum"),
    ).reset_index()
    grouped["Margin"] = (
        grouped["Profit"].div(grouped["Sales"].where(grouped["Sales"].ne(0))) * 100
    )
    return grouped.round(2)


def main():
    csv_path = find_csv()
    print(f"Reading: {csv_path.name}")
    df = load_and_clean(csv_path)

    if df.empty:
        sys.exit("ERROR: No valid data rows remain after cleaning the CSV.")

    df.to_csv(BASE / "cleaned_superstore.csv", index=False)

    df["Disc_Band"] = pd.cut(
        df["Discount"],
        bins=[-0.000001, 0, 0.2, 0.4, 1.000001],
        labels=["0%", "1-20%", "21-40%", ">40%"],
        include_lowest=True,
    ).astype("string").fillna("Unknown")

    total_sales = float(df["Sales"].sum())
    total_profit = float(df["Profit"].sum())
    order_count = int(df["Order_ID"].nunique())

    out = {
        "kpi": {
            "sales": round(total_sales, 2),
            "profit": round(total_profit, 2),
            "orders": order_count,
            "customers": int(df["Customer_ID"].nunique()),
            "margin": round(total_profit / total_sales * 100, 2) if total_sales else 0,
            "aov": round(total_sales / order_count, 2) if order_count else 0,
        },
        "monthly": summarise(df, "Month").to_dict("records"),
        "yearly": summarise(df, "Year").to_dict("records"),
        "category": summarise(df, "Category").to_dict("records"),
        "region": summarise(df, "Region").to_dict("records"),
        "segment": summarise(df, "Segment").to_dict("records"),
        "subcat": summarise(df, "Sub_Category").sort_values("Profit").to_dict("records"),
        "top_products": summarise(df, "Product_Name").nlargest(10, "Sales").to_dict("records"),
        "state": summarise(df, "State").sort_values("Profit").head(8).to_dict("records"),
        "discount": summarise(df, "Disc_Band").to_dict("records"),
    }

    discount_order = {"0%": 0, "1-20%": 1, "21-40%": 2, ">40%": 3, "Unknown": 4}
    out["discount"].sort(key=lambda row: discount_order.get(row["Disc_Band"], 99))

    output_json = BASE / "dashboard_data.json"
    output_json.write_text(
        json.dumps(out, ensure_ascii=False, allow_nan=False, indent=2),
        encoding="utf-8",
    )

    kpi = out["kpi"]
    print(
        f"Rows: {len(df):,} | Sales: ${kpi['sales']:,.0f} | "
        f"Profit: ${kpi['profit']:,.0f} | Margin: {kpi['margin']}%"
    )
    print("Saved: cleaned_superstore.csv, dashboard_data.json")


if __name__ == "__main__":
    main()
