import pandas as pd
from pathlib import Path


DATA_PATH = Path("data/sales.csv")
REPORTS_PATH = Path("reports/sales_report.xlsx")


def load_data(file_path: Path) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: file not found at {file_path}")
        return pd.DataFrame()


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df["total"] = df["quantity"] * df["price"]
    return df


def generate_report(df: pd.DataFrame):
    total_revenue = df["total"].sum()
    avg_ticket = df["total"].sum() / df["quantity"].sum()
    revenue_by_category = df.groupby("category")["total"].sum()
    top_product = df.groupby("product")["total"].sum().idxmax()

    print("\n=== SALES REPORT ===")
    print(f"Total Revenue: {total_revenue}")
    print(f"Average Ticket: {avg_ticket:.2f}")
    print("\nRevenue by Category:")
    print(revenue_by_category)
    print(f"\nTop Product: {top_product}")


def export_to_excel(df: pd.DataFrame):
    REPORTS_PATH.parent.mkdir(exist_ok=True)

    summary = {
        "Total Revenue": df["total"].sum(),
        "Total Units": df["quantity"].sum(),
        "Average Ticket": df["total"].sum() / df["quantity"].sum(),
        "Top Product": df.groupby("product")["total"].sum().idxmax()
    }

    revenue_by_category = df.groupby("category")["total"].sum().reset_index()

    with pd.ExcelWriter(REPORTS_PATH) as writer:
        df.to_excel(writer, sheet_name="data", index=False)
        revenue_by_category.to_excel(writer, sheet_name="revenue_by_category", index=False)
        pd.DataFrame([summary]).to_excel(writer, sheet_name="summary", index=False)

    print(f"\nReport exported to {REPORTS_PATH}")

def main():
    df = load_data(DATA_PATH)

    if df.empty:
        print("No data loaded.")
        return

    df = transform_data(df)
    generate_report(df)
    export_to_excel(df)


if __name__ == "__main__":
    main()
