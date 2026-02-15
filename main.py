import pandas as pd
from pathlib import Path


DATA_PATH = Path("data/sales.csv")


def load_data(file_path: Path) -> pd.DataFrame:
    """Load sales data from CSV file."""
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: file not found at {file_path}")
        return pd.DataFrame()


def main():
    df = load_data(DATA_PATH)

    if df.empty:
        print("No data loaded.")
        return

    print("Data loaded successfully!")
    print(df.head())


if __name__ == "__main__":
    main()
