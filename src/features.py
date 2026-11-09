import pandas as pd
import numpy as np


class FeatureEngineer:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def create_features(self) -> pd.DataFrame:
        """Engineers domain-specific financial features for fraud detection."""
        # 1. Error in Originator Balance calculation
        # Expected: newbalanceOrig should equal (oldbalanceOrg - amount)
        self.df["errorBalanceOrig"] = (
            self.df["newbalanceOrig"] + self.df["amount"] - self.df["oldbalanceOrg"]
        )

        # 2. Error in Destination Balance calculation
        # Expected: newbalanceDest should equal (oldbalanceDest + amount)
        self.df["errorBalanceDest"] = (
            self.df["oldbalanceDest"] + self.df["amount"] - self.df["newbalanceDest"]
        )

        # 3. Cyclical time features (hour of day derived from 'step')
        self.df["hour"] = self.df["step"] % 24

        # 4. Binary flag for zero original balance transactions
        self.df["isZeroOldOrig"] = (self.df["oldbalanceOrg"] == 0).astype(int)

        # 5. One-Hot Encoding for transaction type ('TRANSFER' vs 'CASH_OUT')
        self.df = pd.get_dummies(
            self.df, columns=["type"], drop_first=True, dtype=int
        )

        return self.df


if __name__ == "__main__":
    from ingestion import DataIngestion
    from cleaning import DataCleaner

    raw_df = DataIngestion("data/raw/PS_20174371424001719_log.csv").load_data()
    clean_df = DataCleaner(raw_df).filter_relevant_types()

    fe = FeatureEngineer(clean_df)
    featured_df = fe.create_features()
    print(f"✔ Features created successfully! Columns count: {featured_df.shape[1]}")