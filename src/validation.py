import pandas as pd
from typing import Tuple, Dict, Any


class DataValidation:

    EXPECTED_COLUMNS = [
        "step",
        "type",
        "amount",
        "nameOrig",
        "oldbalanceOrg",
        "newbalanceOrig",
        "nameDest",
        "oldbalanceDest",
        "newbalanceDest",
        "isFraud",
        "isFlaggedFraud",
    ]

    VALID_TYPES = {"CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"}

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def validate_schema(self) -> bool:
        """Verifies if all expected columns exist in the DataFrame."""
        missing_cols = set(self.EXPECTED_COLUMNS) - set(self.df.columns)
        if missing_cols:
            raise ValueError(
                f"Schema Validation Failed! Missing columns: {missing_cols}"
            )
        print("✔ Schema Validation Passed!")
        return True

    def validate_data_integrity(self) -> Tuple[bool, Dict[str, Any]]:
        """Checks for missing values, negative amounts, and invalid transaction types."""
        report = {}

        # 1. Null value check
        null_count = self.df.isnull().sum().sum()
        report["total_nulls"] = int(null_count)

        # 2. Negative transaction amount check
        negative_amounts = (self.df["amount"] < 0).sum()
        report["negative_amounts"] = int(negative_amounts)

        # 3. Invalid transaction types check
        invalid_types = set(self.df["type"].unique()) - self.VALID_TYPES
        report["invalid_types"] = list(invalid_types)

        if null_count > 0 or negative_amounts > 0 or len(invalid_types) > 0:
            print("⚠ Data Integrity Check Warnings Found:", report)
            return False, report

        print("✔ Data Integrity Check Passed!")
        return True, report


if __name__ == "__main__":
    from ingestion import DataIngestion

    path = "data/raw/PS_20174371424001719_log.csv"
    ingestion = DataIngestion(raw_data_path=path)
    df = ingestion.load_data()

    validator = DataValidation(df)
    validator.validate_schema()
    validator.validate_data_integrity()