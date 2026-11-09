# ⚡ FraudGuard OPS — Enterprise AI Risk & Compliance Platform

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-005571?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/mit)

**FraudGuard OPS** is a production-grade, full-stack financial fraud detection and regulatory compliance platform. Designed for enterprise risk operations centers, the platform combines supervised risk scoring, unsupervised anomaly detection, explainable AI (XAI), human-in-the-loop audit workflows, and automated compliance reporting.

---

## 🏗️ System Architecture

```text
┌──────────────────────────────┐       REST API JSON       ┌──────────────────────────────┐
│                              │  (POST /v1/assess-fraud)  │                              │
│   Streamlit Frontend Console │ ─────────────────────────>│     FastAPI Core Engine      │
│   • ChaiCode Dark Theme      │                           │   • Multi-Model Scoring      │
│   • Live TPS / Latency HUD   │<───────────────────────── │   • SHAP Explainability      │
│   • PyVis Topology Graph     │     Audit Persistence     │   • SQLite Audit Workbench   │
└──────────────────────────────┘       & PDF Reports       └──────────────────────────────┘

```

---

## 🚀 Key Modules & Capabilities

### 1. Hybrid Machine Learning Scoring Engine

* **Supervised Learning (Random Forest):** Trained on financial transaction datasets to predict transaction risk probabilities.
* **Unsupervised Learning (Isolation Forest):** Identifies behavioral anomalies, structural outliers, and coordinated financial drain attempts.
* **Composite Risk Index:** Outputs a normalized score (0–100) mapped to clear operational risk bands (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).

### 2. Explainable AI (XAI) via SHAP

* Every transaction evaluation includes real-time SHAP feature attributions.
* Visualizes top risk drivers (e.g., balance deviations, transaction amounts, velocity spikes) directly in the dashboard UI.

### 3. Automated AI Case Investigator Agent

* Generates contextual investigation summaries for flagged transactions.
* Recommends immediate system actions (`AUTO_APPROVE`, `FLAG_FOR_REVIEW`, `IMMEDIATE_BLOCK`) based on threat telemetry.

### 4. Human-in-the-Loop Audit Workbench

* Backed by a persistent **SQLite** database (`fraud_audit.db`).
* Allows risk analysts to review historical audit logs, examine SHA-256 transaction hashes, and log manual override decisions (`CONFIRMED_FRAUD`, `FALSE_POSITIVE`, `FLAGGED_FOR_LEGAL`).

### 5. Entity Network Topology Visualizer

* Powered by **PyVis**, generating an interactive node-link graph.
* Maps relationship flows between origin accounts, destination targets, and known suspicious mule hubs.

### 6. Real-Time Transaction Streaming Simulator

* Simulates high-throughput streaming events to test system performance under load.
* Features a live **TPS (Transactions Per Second)** counter, sub-100ms **P99 API Latency** profile chart, and a dynamic threat alert ticker.

### 7. Automated Compliance PDF Exporter

* Built with **ReportLab**.
* Compiles case metadata, SHA-256 verification hashes, SHAP score breakdowns, and investigator notes into an audit-ready PDF document with a single click.

---

## 🛠️ Tech Stack

* **Backend API:** FastAPI, Uvicorn, Pydantic, SQLite
* **Frontend Console:** Streamlit, Plotly, PyVis (Network Graph)
* **AI / ML Core:** Scikit-Learn, SHAP, Joblib, Pandas, NumPy
* **Utilities:** Faker (Synthetic Streaming Data), ReportLab (PDF Case Reports)

---

## ⚙️ Local Installation & Setup

1. **Clone the repository:**
```bash
git clone [https://github.com/Hitexhfr/FraudGuard-AI.git](https://github.com/Hitexhfr/FraudGuard-AI.git)
cd FraudGuard-AI

```


2. **Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows PowerShell/CMD: venv\Scripts\activate

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```


4. **Start the FastAPI Backend:**
```bash
uvicorn src.app:app --reload --port 8000

```


*(The backend API will be live at `http://127.0.0.1:8000`)*
5. **Launch the Streamlit Operations Console:**
Open a **second terminal tab**, activate your virtual environment, and run:
```bash
streamlit run src/ui.py

```


*(The UI dashboard will open automatically at `http://localhost:8501`)*

---

## 📂 Project Directory Structure

```text
FraudGuard-AI/
├── models/                  # Serialized ML models (.pkl)
├── notebooks/               # Exploratory data analysis Jupyter notebooks
├── src/
│   ├── app.py               # FastAPI backend & endpoints
│   ├── ui.py                # Streamlit operations dashboard
│   ├── pdf_generator.py     # ReportLab compliance PDF builder
│   ├── risk_scoring.py      # Core classification logic
│   ├── explainability.py    # SHAP calculation engine
│   └── agent.py             # Automated case investigator agent
├── fraud_audit.db           # SQLite human-in-the-loop audit log
├── requirements.txt         # Project dependencies
└── README.md                # Documentation

```

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

```

```
