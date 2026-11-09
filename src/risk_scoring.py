import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from typing import Dict, Any


class RiskScoringEngine:

    def __init__(self, supervised_model_path: str):
        self.supervised_model = joblib.load(supervised_model_path)
        self.iso_forest = IsolationForest(
            n_estimators=100, contamination=0.01, random_state=42, n_jobs=-1
        )
        self.is_iso_fitted = False

    def fit_anomaly_detector(self, X_train: pd.DataFrame):
        """Fits unsupervised Isolation Forest model on transaction features."""
        print("Training Unsupervised Isolation Forest Anomaly Detector...")
        self.iso_forest.fit(X_train)
        self.is_iso_fitted = True
        print("✔ Isolation Forest fitted successfully!")

    def calculate_risk_score(self, X_single: pd.DataFrame) -> Dict[str, Any]:
        """Calculates combined Fraud Risk Score (0 to 100) and assigns Risk Band."""
        if not self.is_iso_fitted:
            raise ValueError("Anomaly Detector must be fitted before scoring!")

        # 1. Supervised Fraud Probability (Weight: 70%)
        sup_prob = float(self.supervised_model.predict_proba(X_single)[:, 1][0])

        # 2. Unsupervised Anomaly Score (Weight: 30%)
        raw_anomaly = float(self.iso_forest.decision_function(X_single)[0])
        anomaly_prob = float(1 / (1 + np.exp(raw_anomaly * 10)))

        # 3. Composite Risk Score (Scale: 0 - 100)
        final_risk_score = round((0.70 * sup_prob + 0.30 * anomaly_prob) * 100, 2)

        # Risk Band Classification
        if final_risk_score >= 80:
            risk_band = "CRITICAL"
        elif final_risk_score >= 50:
            risk_band = "HIGH"
        elif final_risk_score >= 25:
            risk_band = "MEDIUM"
        else:
            risk_band = "LOW"

        return {
            "supervised_probability": round(sup_prob, 4),
            "anomaly_probability": round(anomaly_prob, 4),
            "final_risk_score": final_risk_score,
            "risk_band": risk_band,
        }


if __name__ == "__main__":
    from ingestion import DataIngestion
    from cleaning import DataCleaner
    from features import FeatureEngineer

    raw_df = DataIngestion("data/raw/PS_20174371424001719_log.csv").load_data()
    clean_df = DataCleaner(raw_df).filter_relevant_types()
    featured_df = FeatureEngineer(clean_df).create_features()

    drop_cols = ["step", "nameOrig", "nameDest", "isFraud", "isFlaggedFraud"]
    X = featured_df.drop(columns=drop_cols)

    engine = RiskScoringEngine(
        supervised_model_path="models/best_model_random_forest.pkl"
    )
    engine.fit_anomaly_detector(X.sample(n=50000, random_state=42))

    sample_transaction = X.iloc[[0]]
    result = engine.calculate_risk_score(sample_transaction)
    print("\n=== Single Transaction Risk Assessment Result ===")
    print(result)