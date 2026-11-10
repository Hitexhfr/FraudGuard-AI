import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time
import random
import tempfile
import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from pyvis.network import Network
from faker import Faker

fake = Faker()

st.set_page_config(
    page_title="FraudGuard Console",
    layout="wide",
    initial_sidebar_state="expanded",
)
API_BASE = "https://fraudguard-ai.onrender.com"

# Comprehensive UI Overhaul: Sidebar, Tabs, Inputs, and High-Contrast Theme
st.markdown(
    """
    <style>
    /* 1. Global Reset & Top Padding */
    .stApp {
        background-color: #0D1117;
        color: #F0F6FC;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .block-container {
        padding-top: 2rem !important; 
        padding-bottom: 2rem !important;
    }

    /* 2. Sidebar Readability Fixes */
    [data-testid="stSidebar"] {
        background-color: #161B22 !important;
        border-right: 1px solid #30363D !important;
    }
    [data-testid="stSidebar"] * {
        color: #F0F6FC !important;
    }
    .stTextInput label p, .stNumberInput label p, .stSelectbox label p {
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        margin-bottom: 4px !important;
    }
    
    /* 3. Input Fields & Dropdowns Base Styling */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="select"] > div,
    div[data-baseweb="base-input"] > input,
    textarea {
        background-color: #0D1117 !important;
        color: #FFFFFF !important;
        border: 1px solid #30363D !important;
        border-radius: 6px !important;
        font-size: 0.9rem !important;
    }
    div[data-baseweb="input"] > div:hover, 
    div[data-baseweb="select"] > div:hover {
        border-color: #58A6FF !important;
    }

    /* 4. Tab Navigation Enhancements */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        color: #8B949E !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding-top: 10px !important;
        padding-bottom: 10px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #FF6B00 !important;
        border-bottom: 3px solid #FF6B00 !important;
    }

    /* 5. Top Navbar */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 24px;
        background-color: #161B22;
        border-bottom: 1px solid #30363D;
        border-radius: 8px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .nav-title {
        font-size: 1.3rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.3px;
    }
    .nav-accent {
        color: #FF6B00;
    }
    .nav-badge {
        font-size: 0.75rem;
        background-color: #21262D;
        color: #C9D1D9;
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid #30363D;
        font-family: monospace;
    }

    /* 6. Cards & Badges */
    .content-card {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .card-title {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #FF6B00;
        letter-spacing: 0.5px;
        margin-bottom: 14px;
    }
    .badge-high {
        background-color: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .badge-medium {
        background-color: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.4);
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .badge-low {
        background-color: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.8rem;
    }

    /* 7. Buttons */
    .stButton>button {
        background-color: #FF6B00 !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #E05D00 !important;
        transform: translateY(-1px);
    }
    div[data-testid="stDownloadButton"] > button {
        background-color: #21262D !important;
        color: #58A6FF !important;
        border: 1px solid #30363D !important;
        width: 100%;
    }
    div[data-testid="stDownloadButton"] > button:hover {
        background-color: #30363D !important;
        color: #79C0FF !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

API_BASE = "https://fraudguard-ai.onrender.com"

# Header
st.markdown(
    """
<div class="nav-bar">
    <div class="nav-title">FraudGuard <span class="nav-accent">Console</span></div>
    <div class="nav-badge">v2.1.0-prod | REST API Active</div>
</div>
""",
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4 = st.tabs(
    ["Risk Analysis", "Live Stream Monitor", "Entity Network", "Analyst Workbench"]
)

# Sidebar Manual Inputs
st.sidebar.markdown("<h3 style='color:#FFFFFF; margin-bottom: 20px;'>Manual Injection</h3>", unsafe_allow_html=True)

preset = st.sidebar.selectbox(
    "Scenario Presets",
    ["High-Risk Drain Attack", "Normal Consumer Transfer", "Custom Payload"],
)

if preset == "High-Risk Drain Attack":
    default_type = "TRANSFER"
    default_amount = 500000.0
    default_orig = "C1305486145"
    default_old_orig = 500000.0
    default_new_orig = 0.0
    default_dest = "C553264065"
    default_old_dest = 0.0
    default_new_dest = 0.0
elif preset == "Normal Consumer Transfer":
    default_type = "TRANSFER"
    default_amount = 1500.0
    default_orig = "C998877661"
    default_old_orig = 20000.0
    default_new_orig = 18500.0
    default_dest = "C112233445"
    default_old_dest = 5000.0
    default_new_dest = 6500.0
else:
    default_type = "TRANSFER"
    default_amount = 181.0
    default_orig = "C1305486145"
    default_old_orig = 181.0
    default_new_orig = 0.0
    default_dest = "C553264065"
    default_old_dest = 0.0
    default_new_dest = 0.0

with st.sidebar.form("tx_form"):
    tx_type = st.selectbox("Type", ["TRANSFER", "CASH_OUT"], index=0 if default_type == "TRANSFER" else 1)
    amount = st.number_input("Amount (INR)", value=default_amount, step=500.0)
    name_orig = st.text_input("Origin Account", value=default_orig)
    old_orig = st.number_input("Origin Prev Balance", value=default_old_orig)
    new_orig = st.number_input("Origin Post Balance", value=default_new_orig)
    name_dest = st.text_input("Destination Account", value=default_dest)
    old_dest = st.number_input("Dest Prev Balance", value=default_old_dest)
    new_dest = st.number_input("Dest Post Balance", value=default_new_dest)
    step = st.number_input("Timestamp Step", value=1, min_value=1)

    st.markdown("<br>", unsafe_allow_html=True)
    submit_btn = st.form_submit_button("Evaluate Risk Signal", use_container_width=True)

payload = {
    "step": int(step),
    "type": tx_type,
    "amount": float(amount),
    "nameOrig": name_orig,
    "oldbalanceOrg": float(old_orig),
    "newbalanceOrig": float(new_orig),
    "nameDest": name_dest,
    "oldbalanceDest": float(old_dest),
    "newbalanceDest": float(new_dest),
}

# TAB 1: RISK ANALYSIS
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    try:
        response = requests.post(f"{API_BASE}/v1/assess-fraud", json=payload, timeout=3)

        if response.status_code == 200:
            data = response.json()
            assessment = data.get("assessment", {})
            explainability = data.get("explainability", {})
            agent_report = data.get("investigation_report", {})

            risk_score = assessment.get("final_risk_score", 0.0)
            risk_band = assessment.get("risk_band", "LOW")

            col1, col2 = st.columns([1, 1.2])

            with col1:
                st.markdown("<div class='card-title'>Risk Score Index</div>", unsafe_allow_html=True)

                gauge_color = "#10B981" if risk_band == "LOW" else "#F59E0B" if risk_band == "MEDIUM" else "#EF4444"

                fig_gauge = go.Figure(
                    go.Indicator(
                        mode="gauge+number",
                        value=risk_score,
                        number={"font": {"color": "#FFFFFF", "size": 44}, "suffix": "/100"},
                        gauge={
                            "axis": {"range": [0, 100], "tickcolor": "#30363D", "tickwidth": 1},
                            "bgcolor": "#161B22",
                            "bordercolor": "#30363D",
                            "bar": {"color": gauge_color, "thickness": 0.25},
                            "steps": [
                                {"range": [0, 30], "color": "rgba(16, 185, 129, 0.08)"},
                                {"range": [30, 70], "color": "rgba(245, 158, 11, 0.08)"},
                                {"range": [70, 100], "color": "rgba(239, 68, 68, 0.08)"},
                            ],
                        },
                    )
                )
                fig_gauge.update_layout(
                    height=220, margin=dict(l=10, r=10, t=10, b=10),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig_gauge, use_container_width=True)

                badge_class = "badge-high" if risk_band in ["HIGH", "CRITICAL"] else "badge-medium" if risk_band == "MEDIUM" else "badge-low"

                st.markdown(
                    f"""
                    <div class="content-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                            <span style="color:#8B949E; font-size:0.8rem; text-transform:uppercase; font-weight:700;">System Verdict</span>
                            <span class="{badge_class}">{risk_band} RISK</span>
                        </div>
                        <div style="font-family:monospace; font-size:0.85rem; color:#C9D1D9; line-height:1.6;">
                            Origin ID &nbsp;: <span style="color:#FFFFFF; font-weight:bold;">{data.get('account_id')}</span><br>
                            Dest ID &nbsp;&nbsp;&nbsp;: <span style="color:#FFFFFF; font-weight:bold;">{data.get('dest_account_id')}</span><br>
                            Amount &nbsp;&nbsp;&nbsp;&nbsp;: <span style="color:#FFFFFF; font-weight:bold;">₹{data.get('transaction_amount'):,.2f}</span><br>
                            TX Hash &nbsp;&nbsp;&nbsp;: <span style="color:#8B949E;">{data.get('transaction_hash')[:16]}...</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown("<div class='card-title'>Feature Impact Attribution</div>", unsafe_allow_html=True)
                drivers = explainability.get("top_risk_drivers", [])

                if drivers:
                    df_shap = pd.DataFrame(drivers)
                    fig_bar = go.Figure(
                        go.Bar(
                            x=df_shap["shap_value"], y=df_shap["feature"],
                            orientation="h",
                            marker=dict(color="#FF6B00", line=dict(color="#E05D00", width=1)),
                        )
                    )
                    fig_bar.update_layout(
                        xaxis=dict(title="SHAP Value", title_font=dict(size=11, color="#8B949E"), tickfont=dict(color="#8B949E"), gridcolor="#21262D"),
                        yaxis=dict(autorange="reversed", tickfont=dict(color="#C9D1D9", size=12)),
                        height=220, margin=dict(l=10, r=10, t=10, b=10),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)

            st.markdown("<div class='card-title'>Automated Investigation Report</div>", unsafe_allow_html=True)
            action = agent_report.get("action", "AUTO_APPROVE")
            action_border = "#EF4444" if "BLOCK" in action else "#F59E0B" if "FLAG" in action else "#10B981"
            formatted_summary = agent_report.get("investigation_summary", "No summary available.").replace("$", "₹")

            st.markdown(
                f"""
                <div style="background-color:#161B22; border:1px solid #30363D; border-left:4px solid {action_border}; border-radius:8px; padding:16px;">
                    <div style="font-size:0.85rem; font-weight:700; color:{action_border}; text-transform:uppercase; margin-bottom:8px;">
                        Recommended Action: {action}
                    </div>
                    <div style="font-family:monospace; font-size:0.85rem; color:#C9D1D9; white-space:pre-wrap; line-height:1.5;">{formatted_summary}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    except Exception:
        st.warning("API service unavailable.")
# TAB 2: LIVE STREAM MONITOR
with tab2:
    st.markdown("<br><div class='card-title'>Real-Time Transaction Stream & Performance Metrics</div>", unsafe_allow_html=True)

    stream_col1, stream_col2 = st.columns([1, 2.5])

    with stream_col1:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.markdown("<b style='color:#FFFFFF; display:block; margin-bottom:12px;'>Stream Controls</b>", unsafe_allow_html=True)
        num_events = st.slider("Transaction Events to Simulate", min_value=5, max_value=50, value=15, step=5)
        fraud_ratio = st.slider("Attack Injection Ratio (%)", min_value=0, max_value=50, value=20, step=5)
        st.markdown("<br>", unsafe_allow_html=True)
        run_stream = st.button("Start Live Stream", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with stream_col2:
        metrics_placeholder = st.empty()
        chart_placeholder = st.empty()
        feed_placeholder = st.empty()

    if run_stream:
        latencies = []
        alerts = []
        total_scanned = 0
        fraud_blocked = 0
        start_total_time = time.time()

        for i in range(num_events):
            is_fraud_event = random.randint(1, 100) <= fraud_ratio
            if is_fraud_event:
                sim_amount = random.uniform(100000.0, 800000.0)
                sim_orig_old = sim_amount
                sim_orig_new = 0.0
                sim_dest_old = 0.0
                sim_dest_new = 0.0
            else:
                sim_amount = random.uniform(200.0, 5000.0)
                sim_orig_old = random.uniform(10000.0, 50000.0)
                sim_orig_new = sim_orig_old - sim_amount
                sim_dest_old = random.uniform(1000.0, 20000.0)
                sim_dest_new = sim_dest_old + sim_amount

            sim_payload = {
                "step": random.randint(1, 100), "type": "TRANSFER", "amount": float(sim_amount),
                "nameOrig": f"C{random.randint(10000000, 99999999)}", "oldbalanceOrg": float(sim_orig_old), "newbalanceOrig": float(sim_orig_new),
                "nameDest": f"C{random.randint(10000000, 99999999)}", "oldbalanceDest": float(sim_dest_old), "newbalanceDest": float(sim_dest_new),
            }

            t0 = time.time()
            try:
                res = requests.post(f"{API_BASE}/v1/assess-fraud", json=sim_payload, timeout=2)
                latency_ms = (time.time() - t0) * 1000
                latencies.append(latency_ms)

                if res.status_code == 200:
                    res_data = res.json()
                    risk_score = res_data.get("assessment", {}).get("final_risk_score", 0.0)
                    risk_band = res_data.get("assessment", {}).get("risk_band", "LOW")

                    total_scanned += 1
                    if risk_band in ["HIGH", "CRITICAL"]:
                        fraud_blocked += 1

                    alerts.append({
                        "tx_hash": res_data.get("transaction_hash")[:12], "account": sim_payload["nameOrig"],
                        "amount": f"₹{sim_amount:,.2f}", "score": f"{risk_score:.1f}/100", "band": risk_band, "latency": f"{latency_ms:.1f}ms",
                    })
            except Exception:
                pass

            elapsed = time.time() - start_total_time
            tps = total_scanned / elapsed if elapsed > 0 else 0
            avg_lat = sum(latencies) / len(latencies) if latencies else 0

            metrics_placeholder.markdown(
                f"""
                <div style="display:flex; gap:16px; margin-bottom:16px;">
                    <div class="content-card" style="flex:1; text-align:center; padding:12px;">
                        <div class="card-title" style="margin-bottom:4px;">Throughput</div>
                        <div style="font-size:1.8rem; font-weight:700; color:#FFFFFF;">{tps:.1f} <span style="font-size:0.9rem; color:#8B949E;">TPS</span></div>
                    </div>
                    <div class="content-card" style="flex:1; text-align:center; padding:12px;">
                        <div class="card-title" style="margin-bottom:4px;">Avg Latency</div>
                        <div style="font-size:1.8rem; font-weight:700; color:#58A6FF;">{avg_lat:.1f} <span style="font-size:0.9rem; color:#8B949E;">ms</span></div>
                    </div>
                    <div class="content-card" style="flex:1; text-align:center; padding:12px;">
                        <div class="card-title" style="margin-bottom:4px;">Blocked</div>
                        <div style="font-size:1.8rem; font-weight:700; color:#EF4444;">{fraud_blocked}/{total_scanned}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True,
            )

            df_lat = pd.DataFrame({"Event": range(1, len(latencies) + 1), "Latency (ms)": latencies})
            fig_stream = go.Figure(go.Scatter(x=df_lat["Event"], y=df_lat["Latency (ms)"], mode="lines+markers", line=dict(color="#FF6B00", width=2), marker=dict(size=6, color="#58A6FF")))
            fig_stream.update_layout(
                xaxis_title="Event Sequence", yaxis_title="Latency (ms)", height=180, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(gridcolor="#21262D", tickfont=dict(color="#8B949E")), yaxis=dict(gridcolor="#21262D", tickfont=dict(color="#8B949E")),
            )
            chart_placeholder.plotly_chart(fig_stream, use_container_width=True)

            if alerts:
                df_alerts = pd.DataFrame(alerts).iloc[::-1]
                feed_placeholder.dataframe(df_alerts, use_container_width=True, height=200)

            time.sleep(0.1)

# TAB 3: ENTITY NETWORK
with tab3:
    st.markdown("<br><div class='card-title'>Entity Graph Topology</div>", unsafe_allow_html=True)
    net = Network(height="450px", width="100%", bgcolor="#0D1117", font_color="#C9D1D9", directed=True)
    net.add_node(name_orig, label=f"Origin: {name_orig}", color="#EF4444" if amount > 100000 else "#FF6B00", size=22)
    net.add_node(name_dest, label=f"Dest: {name_dest}", color="#F59E0B" if amount > 100000 else "#10B981", size=18)
    net.add_edge(name_orig, name_dest, title=f"Transfer: ₹{amount:,.2f}", weight=2, color="#FF6B00")
    net.add_node("C_MULE_HUB_99", label="Mule Hub", color="#EF4444", size=26)
    net.add_edge(name_dest, "C_MULE_HUB_99", title="Outflow Link", color="#EF4444")
    net.add_node("C_NORMAL_ACC_01", label="Secondary Acc", color="#10B981", size=14)
    net.add_edge("C_NORMAL_ACC_01", name_orig, title="Inflow Link", color="#30363D")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        with open(tmp_file.name, "r", encoding="utf-8") as f:
            html_content = f.read()
    components.html(html_content, height=470)

# TAB 4: ANALYST WORKBENCH
with tab4:
    st.markdown("<br><div class='card-title'>Human-in-the-Loop Audit Log</div>", unsafe_allow_html=True)
    try:
        logs_res = requests.get(f"{API_BASE}/v1/audit-logs", timeout=3).json()
        logs = logs_res.get("logs", [])
        if logs:
            df_logs = pd.DataFrame(logs)
            st.dataframe(df_logs[["transaction_hash", "account_id", "amount", "risk_score", "risk_band", "recommended_action", "analyst_status", "timestamp"]], use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)
            col_left, col_right = st.columns([1.2, 1])

            with col_left:
                st.markdown("<div class='card-title'>Override Case Decision</div>", unsafe_allow_html=True)
                with st.form("override_form"):
                    selected_hash = st.selectbox("Select Transaction Hash", df_logs["transaction_hash"].tolist())
                    status_choice = st.selectbox("Decision", ["CONFIRMED_FRAUD", "FALSE_POSITIVE", "FLAGGED_FOR_LEGAL"])
                    notes_input = st.text_area("Notes", value="Manual review complete. KYC verification and risk indicators checked.", height=95)
                    st.markdown("<br>", unsafe_allow_html=True)
                    submit_override = st.form_submit_button("Save Decision", use_container_width=True)
                    if submit_override:
                        override_payload = {"transaction_hash": selected_hash, "status": status_choice, "notes": notes_input}
                        res = requests.post(f"{API_BASE}/v1/analyst-override", json=override_payload)
                        if res.status_code == 200:
                            st.success(f"Audit decision logged for {selected_hash[:12]}...")
                            st.rerun()

            with col_right:
                st.markdown("<div class='card-title'>Export Compliance PDF</div>", unsafe_allow_html=True)
                st.markdown("<div class='content-card'>", unsafe_allow_html=True)
                st.markdown("<p style='font-size:0.9rem; color:#C9D1D9; margin-bottom:16px;'>Generate an audit-ready compliance case file for regulatory reporting.</p>", unsafe_allow_html=True)
                if st.button("Generate Case Report", use_container_width=True):
                    try:
                        pdf_res = requests.post(f"{API_BASE}/v1/download-case-pdf", json=payload)
                        if pdf_res.status_code == 200:
                            st.download_button(
                                label="Download PDF Case File", data=pdf_res.content,
                                file_name=f"Compliance_Report_{selected_hash[:8]}.pdf", mime="application/pdf",
                                use_container_width=True,
                            )
                    except Exception as err:
                        st.error(f"Failed to generate PDF: {err}")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No transaction audit records logged yet.")
    except Exception:
        st.warning("API service unavailable.")