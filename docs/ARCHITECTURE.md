# Octopus Architecture

Octopus is a modular, privacy-first financial resilience system.

## Design metaphor

An octopus has almost no rigid structure, but it still has one hard limit: the beak. Octopus uses this idea for household finance. The system should adapt around the user's real constraints instead of forcing a rigid budget model.

## Hard constraints

The first production system should model five constraints:

1. Monthly cash flow
2. Essential spending
3. Debt and EMI load
4. Emergency readiness
5. Scam and misinformation exposure

## System components

### Web app

The web app handles onboarding, dashboard views, scenario planning, education content, and user settings.

Recommended stack: Next.js, TypeScript, Tailwind CSS, and accessible UI components.

### API service

The API is the decision-support layer. It handles household risk assessment, rule execution, simulations, user settings, and audit logs.

Recommended stack: FastAPI, Pydantic, PostgreSQL, Redis, and OpenTelemetry.

### Worker service

The worker runs asynchronous tasks such as imports, scheduled checks, report generation, and optional AI-assisted explanations.

### Rules package

The rules package contains deterministic and versioned financial rules. AI can help with plain-language explanations, but core risk logic should stay testable and explainable.

### Data layer

PostgreSQL stores structured application data. Sensitive fields should be encrypted. Logs should avoid storing raw personal financial details unless strictly required.

### AI adapter

AI providers are optional. The default system should work in rules-only mode. Any AI output should be labeled, explainable, and non-authoritative.

## Production principles

- Privacy first.
- Self-hostable deployment.
- No sale of user data.
- No steering toward predatory products.
- Auditable recommendations.
- Deterministic rules for safety-critical paths.
- Clear uncertainty when the system does not have enough data.

## First deployment shape

```text
Client -> Web App -> API -> PostgreSQL
                     -> Redis
                     -> Worker
                     -> Optional AI Provider
```

## Future modules

- Statement import
- Transaction classification
- Coverage gap planner
- Scam-pattern registry
- Education library
- Local-language explainers
- Anonymous benchmark datasets
