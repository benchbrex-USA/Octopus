from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.rules import RiskSignalResult, assess_household_risk

app = FastAPI(
    title="Octopus API",
    description="Open-source financial resilience API for debt pressure, savings recovery, medical shocks, cost-of-living stress, and scam safety.",
    version="0.1.0",
)


class HouseholdProfile(BaseModel):
    monthly_income: float = Field(ge=0, description="Total monthly take-home income")
    fixed_expenses: float = Field(ge=0, description="Rent, food, utilities, school fees, transport, etc.")
    emi_payments: float = Field(ge=0, description="Total monthly EMI and debt payments")
    credit_card_due: float = Field(ge=0, description="Current credit card due")
    savings_balance: float = Field(ge=0, description="Liquid savings available now")
    monthly_medical_costs: float = Field(default=0, ge=0, description="Recurring healthcare or medicine costs")
    dependents: int = Field(default=0, ge=0, description="Number of dependents")


class RiskSignal(BaseModel):
    name: str
    level: str
    explanation: str
    next_action: str


class RiskAssessment(BaseModel):
    debt_to_income_ratio: float
    expense_to_income_ratio: float
    liquidity_runway_months: float
    risk_level: str
    rule_version: str
    signals: list[RiskSignal]
    disclaimer: str

def to_api_signal(signal: RiskSignalResult) -> RiskSignal:
    return RiskSignal(
        name=signal.name,
        level=signal.level,
        explanation=signal.explanation,
        next_action=signal.next_action,
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/risk/household", response_model=RiskAssessment)
def assess_household(profile: HouseholdProfile) -> RiskAssessment:
    result = assess_household_risk(
        monthly_income=profile.monthly_income,
        fixed_expenses=profile.fixed_expenses,
        emi_payments=profile.emi_payments,
        savings_balance=profile.savings_balance,
        monthly_medical_costs=profile.monthly_medical_costs,
        dependents=profile.dependents,
    )

    return RiskAssessment(
        debt_to_income_ratio=result.debt_to_income_ratio,
        expense_to_income_ratio=result.expense_to_income_ratio,
        liquidity_runway_months=result.liquidity_runway_months,
        risk_level=result.risk_level,
        rule_version=result.rule_version,
        signals=[to_api_signal(signal) for signal in result.signals],
        disclaimer="Educational decision-support only. Not financial, legal, tax, insurance, investment, or medical advice.",
    )
