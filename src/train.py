import os
import joblib
import pandas as pd
import mlflow
import mlflow.sklearn
import mlflow.xgboost

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, average_precision_score, recall_score, precision_score

from ingestion import DataIngestion
from cleaning import DataCleaner
from features import FeatureEngineer


def train_and_evaluate():
    # Set MLflow experiment name
    mlflow.set_experiment("FraudGuard_Fraud_Detection")

    print("--- 1. Pipeline Execution ---")
    raw_df = DataIngestion("data/raw/PS_20174371424001719_log.csv").load_data()
    clean_df = DataCleaner(raw_df).filter_relevant_types()
    featured_df = FeatureEngineer(clean_df).create_features()

    drop_cols = ["step", "nameOrig", "nameDest", "isFraud", "isFlaggedFraud"]
    X = featured_df.drop(columns=drop_cols)
    y = featured_df["isFraud"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Train Shape: {X_train.shape}, Test Shape: {X_test.shape}")

    models = {
        "Logistic_Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random_Forest": RandomForestClassifier(n_estimators=50, max_depth=12, random_state=42, n_jobs=-1),
        "XGBoost": XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, scale_pos_weight=99, random_state=42, n_jobs=-1)
    }

    best_pr_auc = 0.0
    best_model_name = ""
    best_model_obj = None

    for name, model in models.items():
        with mlflow.start_run(run_name=name):
            print(f"\n--- Training {name} ---")
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1]

            pr_auc = average_precision_score(y_test, y_prob)
            rec = recall_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred)

            print(f"[{name}] PR-AUC: {pr_auc:.4f} | Recall: {rec:.4f} | Precision: {prec:.4f}")

            # Log metrics to MLflow
            mlflow.log_param("model_type", name)
            mlflow.log_metric("pr_auc", pr_auc)
            mlflow.log_metric("recall", rec)
            mlflow.log_metric("precision", prec)

            if pr_auc > best_pr_auc:
                best_pr_auc = pr_auc
                best_model_name = name
                best_model_obj = model

    print(f"\n🏆 Best Model: {best_model_name} with PR-AUC = {best_pr_auc:.4f}")
    os.makedirs("models", exist_ok=True)
    joblib.dump(best_model_obj, f"models/best_model_{best_model_name.lower()}.pkl")
    print(f"✔ Saved Best Model to models/best_model_{best_model_name.lower()}.pkl")


if __name__ == "__main__":
    train_and_evaluate()