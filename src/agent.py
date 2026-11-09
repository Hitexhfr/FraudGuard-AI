import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class InvestigationState:
    transaction_id: str
    risk_score: float
    risk_band: str
    top_drivers: List[Dict[str, Any]]
    recommendation: str = ""
    investigation_summary: str = ""


class FraudInvestigatorAgent:

    def __init__(self):
        pass

    def evaluate_case(self, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Automated rule-and-explainability based case investigation agent."""
        risk_score = assessment_data.get("assessment", {}).get(
            "final_risk_score", 0.0
        )
        risk_band = assessment_data.get("assessment", {}).get(
            "risk_band", "UNKNOWN"
        )
        drivers = assessment_data.get("explainability", {}).get(
            "top_risk_drivers", []
        )
        account_id = assessment_data.get("account_id", "N/A")
        amount = assessment_data.get("transaction_amount", 0.0)

        # Decision Strategy
        if risk_band in ["CRITICAL", "HIGH"]:
            rec = "BLOCK_TRANSACTION_AND_FREEZE_ACCOUNT"
        elif risk_band == "MEDIUM":
            rec = "FLAG_FOR_MANUAL_AUDIT"
        else:
            rec = "AUTO_APPROVE"

        # Automated Brief Summary Synthesis
        driver_names = [d["feature"] for d in drivers]
        summary = (
            f"Automated Case Analysis for Account {account_id}:\n"
            f"- Transaction Amount: ₹{amount:,.2f}\n"
            f"- Risk Assessment: {risk_score}/100 ({risk_band})\n"
            f"- Action Recommended: {rec}\n"
            f"- Primary Risk Drivers Identified: {', '.join(driver_names)}"
        )

        return {
            "account_id": account_id,
            "action": rec,
            "investigation_summary": summary,
        }


if __name__ == "__main__":
    sample_payload = {
        "account_id": "C1305486145",
        "transaction_amount": 181.0,
        "assessment": {"final_risk_score": 76.21, "risk_band": "HIGH"},
        "explainability": {
            "top_risk_drivers": [
                {"feature": "errorBalanceOrig", "shap_value": 0.3453},
                {"feature": "newbalanceOrig", "shap_value": 0.2489},
            ]
        },
    }

    agent = FraudInvestigatorAgent()
    report = agent.evaluate_case(sample_payload)
    print("\n=== AI Investigation Report ===")
    print(report["investigation_summary"])