# FraudGuard-AI 🛡️

**FraudGuard-AI** is an end-to-end, real-time transaction risk scoring and anomaly detection platform built to catch financial fraud before it happens. Powered by machine learning (XGBoost & Isolation Forest) with explainable AI (SHAP), the system processes high-risk transaction signals and delivers instant risk scores, feature impact attributions, and human-in-the-loop audit logging through a modern console.

---

## 🌟 Key Features

- **Real-Time Risk Scoring**: Sub-second risk evaluation combining supervised model prediction with unsupervised anomaly detection.
- **Explainable AI (XAI)**: SHAP (SHapley Additive exPlanations) visual attribution to break down exactly which features contributed to a transaction's risk score.
- **Automated Fallback Engine**: Built-in data ingestion pipelines capable of handling missing remote datasets gracefully via synthetic distribution fallback.
- **Human-in-the-Loop Workbench**: Integrated audit log system tracking transaction hash records for analyst review.
- **Decoupled Architecture**: Fast, lightweight Streamlit frontend communicating seamlessly with a containerized FastAPI REST backend over HTTPS.

---

## 🏗️ System Architecture

```text
┌─────────────────────────┐         HTTP/REST         ┌────────────────────────┐
│  Streamlit Console UI   │  ──────────────────────>  │   FastAPI Backend API  │
│  (Hosted on Streamlit)  │  <──────────────────────  │   (Hosted on Render)   │
└─────────────────────────┘      JSON Payload         └───────────┬────────────┘
                                                                  │
                                                        ┌─────────┴─────────┐
                                                        │  Inference Engine │
                                                        │  - XGBoost        │
                                                        │  - IsolationForest│
                                                        │  - SHAP Explainer │
                                                        └───────────────────┘

```

---

## 🚀 Live Demos

* **Frontend Console**: [fraudguard-ai-hitesh.streamlit.app](https://www.google.com/search?q=https://fraudguard-ai-hitesh.streamlit.app)
* **REST API Endpoint**: `https://fraudguard-ai-tzcl.onrender.com`

---

## 📂 Project Structure

```text
FraudGuard-AI/
├── data/
│   └── raw/                  # Transaction datasets (CSV)
├── models/                   # Pre-trained ML artifacts & scalar pkls
├── notebooks/                # Model exploration and prototyping
├── src/
│   ├── app.py                # FastAPI server entry point & model loading
│   ├── ingestion.py          # Data ingestion engine with cloud fallbacks
│   ├── risk_scoring.py       # ML risk scoring and SHAP explainability core
│   └── ui.py                 # Streamlit dashboard interface
├── requirements.txt          # Python dependency specifications
└── README.md                 # Project documentation

```

---

## 🛠️ Local Setup & Installation

### Prerequisites

* Python 3.10+
* Git

### 1. Clone the Repository

```bash
git clone [https://github.com/Hitexhfr/FraudGuard-AI.git](https://github.com/Hitexhfr/FraudGuard-AI.git)
cd FraudGuard-AI

```

### 2. Set Up Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

---

## 🏃 Running the Application Locally

### Step 1: Start the FastAPI Backend

```bash
uvicorn src.app:app --host 127.0.0.1 --port 8000 --reload

```

The API docs will be accessible at `http://127.0.0.1:8000/docs`.

### Step 2: Start the Streamlit Dashboard

Open a new terminal window, activate your environment, and run:

```bash
streamlit run src/ui.py

```

The console will launch in your default web browser at `http://localhost:8501`.

---

## 📡 API Reference

### Health Check

`GET /`

```json
{
  "status": "HEALTHY",
  "version": "2.0.0"
}

```

### Predict Risk Signal

`POST /predict`

**Request Body:**

```json
{
  "step": 1,
  "type": "TRANSFER",
  "amount": 500000.0,
  "nameOrig": "C1305486145",
  "oldbalanceOrg": 500000.0,
  "newbalanceOrig": 0.0,
  "nameDest": "C553264065",
  "oldbalanceDest": 0.0,
  "newbalanceDest": 0.0
}

```

---

## 🧰 Tech Stack

* **Machine Learning**: `scikit-learn`, `xgboost`, `shap`, `pandas`, `numpy`
* **Backend API**: `FastAPI`, `uvicorn`, `pydantic`
* **Frontend UI**: `Streamlit`, `plotly`
* **Cloud Infrastructure**: Streamlit Cloud, Render

---

## 👤 Author

**Hitesh Yadav**

* GitHub: [@Hitexhfr](https://github.com/Hitexhfr)

```

```
