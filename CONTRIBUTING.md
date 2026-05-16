# Contributing to Octopus

Thank you for helping build Octopus.

Octopus is an open-source financial resilience system. Contributions should improve user safety, privacy, clarity, and reliability.

## Ways to contribute

- Improve documentation
- Add tests
- Improve financial rule explainability
- Build web UI components
- Improve deployment scripts
- Add local-language educational content
- Report bugs or unclear recommendations
- Review safety and privacy risks

## Development setup

```bash
git clone https://github.com/benchbrex-USA/Octopus.git
cd Octopus
cp .env.example .env
docker compose up --build
```

API health check:

```bash
curl http://localhost:8000/health
```

## Contribution principles

1. Keep recommendations explainable.
2. Do not add dark patterns.
3. Do not introduce affiliate steering.
4. Do not log sensitive user data unnecessarily.
5. Prefer deterministic rules for high-impact flows.
6. Write tests for risk logic.
7. Keep language simple and respectful.

## Pull request checklist

Before opening a PR, check:

- The change has a clear purpose.
- Risk logic has tests.
- User-facing explanations are plain-language.
- No secrets are committed.
- No unnecessary personal data is collected.
- Documentation is updated when behavior changes.

## Reporting sensitive issues

Please do not open public issues for security or privacy vulnerabilities. Follow `SECURITY.md` instead.
