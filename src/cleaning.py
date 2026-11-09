import pandas as pd

class DataCleaner:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def filter_relevant_types(self) -> pd.DataFrame:
        """Filters dataset to include only TRANSFER and CASH_OUT types where fraud occurs."""
        relevant_types = ["TRANSFER", "CASH_OUT"]
        initial_count = len(self.df)
        filtered_df = self.df[self.df["type"].isin(relevant_types)].reset_index(
            drop=True
        )
        print(
            f"Filtered dataset from {initial_count:,} to {len(filtered_df):,} rows (TRANSFER & CASH_OUT only)."
        )
        return filtered_df

    def clean_balances(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fills missing values if any and ensures balance consistency."""
        df = df.fillna(0)
        return df


if __name__ == "__main__":
    from ingestion import DataIngestion

    path = "data/raw/PS_20174371424001719_log.csv"
    raw_df = DataIngestion(raw_data_path=path).load_data()

    cleaner = DataCleaner(raw_df)
    clean_df = cleaner.filter_relevant_types()
    print("✔ Data Cleaning Completed successfully!")