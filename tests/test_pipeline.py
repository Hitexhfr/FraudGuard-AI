import pytest
import pandas as pd
import numpy as np
from src.validation import DataValidation


@pytest.fixture
def sample_transaction_data():
    return pd.DataFrame(
        {
            "step": [1, 2],
            "type": ["TRANSFER", "CASH_OUT"],
            "amount": [1000.0, 500.0],
            "nameOrig": ["C123", "C456"],
            "oldbalanceOrg": [1000.0, 500.0],
            "newbalanceOrig": [0.0, 0.0],
            "nameDest": ["C789", "M101"],
            "oldbalanceDest": [0.0, 0.0],
            "newbalanceDest": [1000.0, 500.0],
            "isFraud": [0, 1],
            "isFlaggedFraud": [0, 0],
        }
    )


def test_schema_validation_success(sample_transaction_data):
    validator = DataValidation(sample_transaction_data)
    assert validator.validate_schema() is True


def test_schema_validation_failure():
    invalid_df = pd.DataFrame({"step": [1], "amount": [100.0]})
    validator = DataValidation(invalid_df)
    with pytest.raises(ValueError):
        validator.validate_schema()