from fastapi.testclient import TestClient

from app.main import app
from app.rules import RULE_ENGINE_VERSION

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_household_risk_detects_emi_trap() -> None:
    response = client.post(
        "/v1/risk/household",
        json={
            "monthly_income": 50000,
            "fixed_expenses": 25000,
            "emi_payments": 26000,
            "credit_card_due": 80000,
            "savings_balance": 10000,
            "monthly_medical_costs": 2000,
            "dependents": 2,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["risk_level"] == "critical"
    assert body["rule_version"] == RULE_ENGINE_VERSION
    assert body["debt_to_income_ratio"] >= 0.5
    assert any(signal["name"] == "EMI trap risk" for signal in body["signals"])


def test_household_risk_stable_baseline() -> None:
    response = client.post(
        "/v1/risk/household",
        json={
            "monthly_income": 100000,
            "fixed_expenses": 35000,
            "emi_payments": 5000,
            "credit_card_due": 0,
            "savings_balance": 300000,
            "monthly_medical_costs": 0,
            "dependents": 0,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["risk_level"] == "low"
    assert body["rule_version"] == RULE_ENGINE_VERSION
    assert body["liquidity_runway_months"] >= 7


def test_household_risk_is_deterministic_for_same_input() -> None:
    payload = {
        "monthly_income": 70000,
        "fixed_expenses": 30000,
        "emi_payments": 14000,
        "credit_card_due": 12000,
        "savings_balance": 60000,
        "monthly_medical_costs": 1000,
        "dependents": 1,
    }

    response_a = client.post("/v1/risk/household", json=payload)
    response_b = client.post("/v1/risk/household", json=payload)

    assert response_a.status_code == 200
    assert response_b.status_code == 200
    assert response_a.json() == response_b.json()
