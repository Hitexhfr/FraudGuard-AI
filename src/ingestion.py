import os
import pandas as pd
from typing import Optional


class DataIngestion:

    def __init__(self, raw_data_path: str):
        self.raw_data_path = raw_data_path

    def load_data(self) -> pd.DataFrame:
        """Loads transaction data from CSV file into DataFrame."""
        if not os.path.exists(self.raw_data_path):
            raise FileNotFoundError(
                f"Dataset not found at path: {self.raw_data_path}"
            )

        print(f"Loading data from {self.raw_data_path}...")
        df = pd.read_csv(self.raw_data_path)
        print(f"Successfully loaded dataset with shape: {df.shape}")
        return df

    def get_sample(
        self, df: pd.DataFrame, sample_ratio: float = 0.1
    ) -> pd.DataFrame:
        """Creates a balanced sample for fast local model prototyping."""
        df_fraud = df[df["isFraud"] == 1]
        df_legit = df[df["isFraud"] == 0].sample(
            frac=sample_ratio, random_state=42
        )

        sampled_df = (
            pd.concat([df_fraud, df_legit])
            .sample(frac=1, random_state=42)
            .reset_index(drop=True)
        )
        print(f"Created sample dataset with shape: {sampled_df.shape}")
        return sampled_df


if __name__ == "__main__":
    path = "data/raw/PS_20174371424001719_log.csv"
    ingestion = DataIngestion(raw_data_path=path)
    data = ingestion.load_data()