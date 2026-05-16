from fastapi import FastAPI
from pydantic import BaseModel, Field

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
    signals: list[RiskSignal]
    disclaimer: str


def classify_level(score: int) -> str:
    if score >= 8:
        return "critical"
    if score >= 5:
        return "high"
    if score >= 3:
        return "moderate"
    return "low"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/risk/household", response_model=RiskAssessment)
def assess_household(profile: HouseholdProfile) -> RiskAssessment:
    income = max(profile.monthly_income, 1)
    debt_to_income = profile.emi_payments / income
    expense_to_income = (profile.fixed_expenses + profile.emi_payments + profile.monthly_medical_costs) / income
    monthly_gap = max(profile.fixed_expenses + profile.emi_payments + profile.monthly_medical_costs - profile.monthly_income, 0)
    monthly_burn = max(profile.fixed_expenses + profile.emi_payments + profile.monthly_medical_costs, 1)
    runway = profile.savings_balance / monthly_burn

    score = 0
    signals: list[RiskSignal] = []

    if debt_to_income >= 0.5:
        score += 3
        signals.append(RiskSignal(
            name="EMI trap risk",
            level="critical",
            explanation="Debt payments are consuming at least half of monthly income.",
            next_action="Freeze new borrowing, list all lenders, and prioritize high-interest debt renegotiation.",
        ))
    elif debt_to_income >= 0.35:
        score += 2
        signals.append(RiskSignal(
            name="High debt pressure",
            level="high",
            explanation="Debt payments are above a safe monthly range.",
            next_action="Avoid new EMIs and compare avalanche vs. snowball repayment plans.",
        ))

    if expense_to_income >= 1:
        score += 3
        signals.append(RiskSignal(
            name="Negative cash flow",
            level="critical",
            explanation="Monthly obligations are equal to or greater than monthly income.",
            next_action="Create a 30-day squeeze plan: protect essentials, pause non-essentials, and negotiate payments.",
        ))
    elif expense_to_income >= 0.85:
        score += 2
        signals.append(RiskSignal(
            name="Low flexibility",
            level="high",
            explanation="Very little income remains after fixed expenses and debt payments.",
            next_action="Cut or renegotiate the largest recurring costs before reducing essential spending.",
        ))

    if runway < 1:
        score += 2
        signals.append(RiskSignal(
            name="Emergency buffer gap",
            level="high",
            explanation="Liquid savings cover less than one month of essential obligations.",
            next_action="Build a starter emergency buffer before taking non-essential financial risks.",
        ))

    if profile.monthly_medical_costs > 0 or profile.dependents > 0:
        score += 1
        signals.append(RiskSignal(
            name="Healthcare shock exposure",
            level="moderate",
            explanation="Dependents or recurring medical costs increase vulnerability to sudden expenses.",
            next_action="Review insurance coverage, nearby hospital costs, and emergency cash access.",
        ))

    if monthly_gap > 0:
        score += 1

    if not signals:
        signals.append(RiskSignal(
            name="Stable baseline",
            level="low",
            explanation="No major stress signal was detected from the provided inputs.",
            next_action="Maintain savings automation and review debt exposure monthly.",
        ))

    return RiskAssessment(
        debt_to_income_ratio=round(debt_to_income, 4),
        expense_to_income_ratio=round(expense_to_income, 4),
        liquidity_runway_months=round(runway, 2),
        risk_level=classify_level(score),
        signals=signals,
        disclaimer="Educational decision-support only. Not financial, legal, tax, insurance, investment, or medical advice.",
    )
