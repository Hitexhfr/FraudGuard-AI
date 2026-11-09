import joblib
import pandas as pd
import numpy as np
import shap
from typing import Dict, Any


class FraudExplainer:

    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)
        # TreeExplainer is optimized for Tree-based models like Random Forest
        self.explainer = shap.TreeExplainer(self.model)

    def explain_transaction(
        self, X_single: pd.DataFrame, top_n: int = 3
    ) -> Dict[str, Any]:
        """Calculates SHAP values for a single transaction and returns top risk drivers."""
        shap_values = self.explainer.shap_values(X_single)

        # Handle output format differences across scikit-learn/SHAP versions
        if isinstance(shap_values, list):
            # Binary classification list: index 1 corresponds to Fraud class
            vals = shap_values[1][0]
        elif len(shap_values.shape) == 3:
            vals = shap_values[0, :, 1]
        else:
            vals = shap_values[0]

        feature_names = X_single.columns
        contributions = dict(zip(feature_names, vals))

        # Sort features by highest positive contribution to fraud score
        sorted_features = sorted(
            contributions.items(), key=lambda x: x[1], reverse=True
        )

        top_drivers = [
            {"feature": feat, "shap_value": round(val, 4)}
            for feat, val in sorted_features[:top_n]
        ]

        return {"top_risk_drivers": top_drivers}


if __name__ == "__main__":
    from ingestion import DataIngestion
    from cleaning import DataCleaner
    from features import FeatureEngineer

    raw_df = DataIngestion("data/raw/PS_20174371424001719_log.csv").load_data()
    clean_df = DataCleaner(raw_df).filter_relevant_types()
    featured_df = FeatureEngineer(clean_df).create_features()

    drop_cols = ["step", "nameOrig", "nameDest", "isFraud", "isFlaggedFraud"]
    X = featured_df.drop(columns=drop_cols)

    explainer = FraudExplainer("models/best_model_random_forest.pkl")
    explanation = explainer.explain_transaction(X.iloc[[0]])

    print("\n=== Top SHAP Risk Drivers for Sample Transaction ===")
    print(explanation)