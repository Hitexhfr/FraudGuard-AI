import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import joblib
import pandas as pd
import json
import hashlib
import sqlite3
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List

from risk_scoring import RiskScoringEngine
from explainability import FraudExplainer
from agent import FraudInvestigatorAgent

# Initialize FastAPI App
app = FastAPI(
    title="FraudGuard AI - Enterprise Risk Platform API",
    version="2.0.0"
)

# Global instances
risk_engine = None
explainer = None
investigator = None
DB_PATH = "fraud_audit.db"

# SQLite DB Initialization
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            transaction_hash TEXT PRIMARY KEY,
            account_id TEXT,
            dest_account_id TEXT,
            amount REAL,
            risk_score REAL,
            risk_band TEXT,
            recommended_action TEXT,
            analyst_status TEXT DEFAULT 'PENDING_REVIEW',
            analyst_notes TEXT DEFAULT '',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

class TransactionRequest(BaseModel):
    step: int = Field(..., example=1)
    type: str = Field(..., example="TRANSFER")
    amount: float = Field(..., example=181.0)
    nameOrig: str = Field(..., example="C1305486145")
    oldbalanceOrg: float = Field(..., example=181.0)
    newbalanceOrig: float = Field(..., example=0.0)
    nameDest: str = Field(..., example="C553264065")
    oldbalanceDest: float = Field(..., example=0.0)
    newbalanceDest: float = Field(..., example=0.0)

class AnalystOverrideRequest(BaseModel):
    transaction_hash: str
    status: str  # CONFIRMED_FRAUD, FALSE_POSITIVE, REJECTED
    notes: str

@app.on_event("startup")
def load_models():
    global risk_engine, explainer, investigator
    model_path = "models/best_model_random_forest.pkl"
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model artifact missing at path: {model_path}")
    
    risk_engine = RiskScoringEngine(supervised_model_path=model_path)
    explainer = FraudExplainer(model_path=model_path)
    investigator = FraudInvestigatorAgent()
    
    from ingestion import DataIngestion
    from cleaning import DataCleaner
    from features import FeatureEngineer
    
    raw_df = DataIngestion("data/raw/PS_20174371424001719_log.csv").load_data()
    clean_df = DataCleaner(raw_df).filter_relevant_types()
    featured_df = FeatureEngineer(clean_df).create_features()
    drop_cols = ["step", "nameOrig", "nameDest", "isFraud", "isFlaggedFraud"]
    X = featured_df.drop(columns=drop_cols)
    
    risk_engine.fit_anomaly_detector(X.sample(n=10000, random_state=42))

def generate_tx_hash(data_dict: dict) -> str:
    payload_str = f"{data_dict['nameOrig']}_{data_dict['nameDest']}_{data_dict['amount']}_{data_dict['step']}"
    return hashlib.sha256(payload_str.encode()).hexdigest()

@app.get("/")
def health_check():
    return {"status": "HEALTHY", "version": "2.0.0"}

@app.post("/v1/assess-fraud")
def predict_fraud(transaction: TransactionRequest) -> Dict[str, Any]:
    try:
        data_dict = transaction.dict()
        tx_hash = generate_tx_hash(data_dict)

        error_orig = data_dict["newbalanceOrig"] + data_dict["amount"] - data_dict["oldbalanceOrg"]
        error_dest = data_dict["oldbalanceDest"] + data_dict["amount"] - data_dict["newbalanceDest"]
        hour = data_dict["step"] % 24
        is_zero_old_orig = 1 if data_dict["oldbalanceOrg"] == 0 else 0
        type_transfer = 1 if data_dict["type"] == "TRANSFER" else 0

        feature_dict = {
            "amount": [data_dict["amount"]],
            "oldbalanceOrg": [data_dict["oldbalanceOrg"]],
            "newbalanceOrig": [data_dict["newbalanceOrig"]],
            "oldbalanceDest": [data_dict["oldbalanceDest"]],
            "newbalanceDest": [data_dict["newbalanceDest"]],
            "errorBalanceOrig": [error_orig],
            "errorBalanceDest": [error_dest],
            "hour": [hour],
            "isZeroOldOrig": [is_zero_old_orig],
            "type_TRANSFER": [type_transfer],
        }

        X_single = pd.DataFrame(feature_dict)
        scoring_res = risk_engine.calculate_risk_score(X_single)
        explanation = explainer.explain_transaction(X_single, top_n=3)

        base_payload = {
            "account_id": data_dict["nameOrig"],
            "transaction_amount": data_dict["amount"],
            "assessment": scoring_res,
            "explainability": explanation
        }

        agent_report = investigator.evaluate_case(base_payload)

        # Log to SQLite DB
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO audit_logs 
            (transaction_hash, account_id, dest_account_id, amount, risk_score, risk_band, recommended_action)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            tx_hash,
            data_dict["nameOrig"],
            data_dict["nameDest"],
            data_dict["amount"],
            scoring_res["final_risk_score"],
            scoring_res["risk_band"],
            agent_report["action"]
        ))
        conn.commit()
        conn.close()

        return {
            "transaction_hash": tx_hash,
            "account_id": data_dict["nameOrig"],
            "dest_account_id": data_dict["nameDest"],
            "transaction_amount": data_dict["amount"],
            "assessment": scoring_res,
            "explainability": explanation,
            "investigation_report": agent_report,
            "cached": False
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/audit-logs")
def get_audit_logs():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT 50")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"logs": rows}

@app.post("/v1/analyst-override")
def analyst_override(payload: AnalystOverrideRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE audit_logs 
        SET analyst_status = ?, analyst_notes = ? 
        WHERE transaction_hash = ?
    """, (payload.status, payload.notes, payload.transaction_hash))
    conn.commit()
    conn.close()
    return {"status": "SUCCESS", "updated_hash": payload.transaction_hash}

from fastapi.responses import FileResponse
from pdf_generator import generate_compliance_pdf

@app.post("/v1/download-case-pdf")
def download_case_pdf(transaction: TransactionRequest):
    try:
        res_data = predict_fraud(transaction)
        pdf_filename = f"case_{res_data['transaction_hash'][:10]}.pdf"
        pdf_path = os.path.join(os.getcwd(), pdf_filename)
        
        generate_compliance_pdf(pdf_path, res_data)
        
        return FileResponse(
            path=pdf_path,
            filename=pdf_filename,
            media_type="application/pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))