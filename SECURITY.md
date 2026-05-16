# Security Policy

Octopus handles sensitive financial information, so security and privacy issues are treated seriously.

## Supported versions

Octopus is currently pre-1.0. Security fixes will target the `main` branch until the first stable release.

## Reporting a vulnerability

Please do not create public GitHub issues for vulnerabilities.

Email: benchbrex@gmail.com

Include:

- A clear description of the issue
- Steps to reproduce
- Potential impact
- Suggested fix, if available

## Security principles

- Minimize data collection.
- Encrypt sensitive fields at rest.
- Avoid storing raw financial documents unless required.
- Do not log secrets or sensitive personal data.
- Use least-privilege access.
- Keep AI providers optional.
- Make self-hosting safe by default.

## Out of scope

- Social engineering against maintainers
- Physical attacks
- Denial-of-service attacks without a concrete vulnerability
- Reports based only on missing security headers in a development build
