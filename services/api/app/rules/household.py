"""Deterministic household risk scoring rules."""

from dataclasses import dataclass

from .version import RULE_ENGINE_VERSION


@dataclass(frozen=True)
class RiskSignalResult:
    name: str
    level: str
    explanation: str
    next_action: str


@dataclass(frozen=True)
class HouseholdRiskResult:
    debt_to_income_ratio: float
    expense_to_income_ratio: float
    liquidity_runway_months: float
    risk_level: str
    signals: tuple[RiskSignalResult, ...]
    rule_version: str


def classify_level(score: int) -> str:
    if score >= 8:
        return "critical"
    if score >= 5:
        return "high"
    if score >= 3:
        return "moderate"
    return "low"


def assess_household_risk(
    *,
    monthly_income: float,
    fixed_expenses: float,
    emi_payments: float,
    savings_balance: float,
    monthly_medical_costs: float,
    dependents: int,
) -> HouseholdRiskResult:
    income = max(monthly_income, 1)
    debt_to_income = emi_payments / income
    expense_to_income = (fixed_expenses + emi_payments + monthly_medical_costs) / income
    monthly_gap = max(fixed_expenses + emi_payments + monthly_medical_costs - monthly_income, 0)
    monthly_burn = max(fixed_expenses + emi_payments + monthly_medical_costs, 1)
    runway = savings_balance / monthly_burn

    score = 0
    signals: list[RiskSignalResult] = []

    if debt_to_income >= 0.5:
        score += 3
        signals.append(
            RiskSignalResult(
                name="EMI trap risk",
                level="critical",
                explanation="Debt payments are consuming at least half of monthly income.",
                next_action="Freeze new borrowing, list all lenders, and prioritize high-interest debt renegotiation.",
            )
        )
    elif debt_to_income >= 0.35:
        score += 2
        signals.append(
            RiskSignalResult(
                name="High debt pressure",
                level="high",
                explanation="Debt payments are above a safe monthly range.",
                next_action="Avoid new EMIs and compare avalanche vs. snowball repayment plans.",
            )
        )

    if expense_to_income >= 1:
        score += 3
        signals.append(
            RiskSignalResult(
                name="Negative cash flow",
                level="critical",
                explanation="Monthly obligations are equal to or greater than monthly income.",
                next_action="Create a 30-day squeeze plan: protect essentials, pause non-essentials, and negotiate payments.",
            )
        )
    elif expense_to_income >= 0.85:
        score += 2
        signals.append(
            RiskSignalResult(
                name="Low flexibility",
                level="high",
                explanation="Very little income remains after fixed expenses and debt payments.",
                next_action="Cut or renegotiate the largest recurring costs before reducing essential spending.",
            )
        )

    if runway < 1:
        score += 2
        signals.append(
            RiskSignalResult(
                name="Emergency buffer gap",
                level="high",
                explanation="Liquid savings cover less than one month of essential obligations.",
                next_action="Build a starter emergency buffer before taking non-essential financial risks.",
            )
        )

    if monthly_medical_costs > 0 or dependents > 0:
        score += 1
        signals.append(
            RiskSignalResult(
                name="Healthcare shock exposure",
                level="moderate",
                explanation="Dependents or recurring medical costs increase vulnerability to sudden expenses.",
                next_action="Review insurance coverage, nearby hospital costs, and emergency cash access.",
            )
        )

    if monthly_gap > 0:
        score += 1

    if not signals:
        signals.append(
            RiskSignalResult(
                name="Stable baseline",
                level="low",
                explanation="No major stress signal was detected from the provided inputs.",
                next_action="Maintain savings automation and review debt exposure monthly.",
            )
        )

    return HouseholdRiskResult(
        debt_to_income_ratio=round(debt_to_income, 4),
        expense_to_income_ratio=round(expense_to_income, 4),
        liquidity_runway_months=round(runway, 2),
        risk_level=classify_level(score),
        signals=tuple(signals),
        rule_version=RULE_ENGINE_VERSION,
    )
