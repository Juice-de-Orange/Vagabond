# Security Policy

## Reporting a Vulnerability

**Please do NOT open a public GitHub issue for security vulnerabilities.**

Instead, please report them via email to: **200407033+Juice-de-Orange@users.noreply.github.com**

You will receive a response within 48 hours. Please include:

1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if you have one)

## What qualifies as a security issue?

- SQL injection, XSS, CSRF
- Authentication/authorization bypass
- Exposure of user data (GPS coordinates, personal information)
- Secrets exposure in code or logs
- Dependency vulnerabilities with known exploits

## What does NOT qualify?

- Bugs that don't have security implications
- Feature requests
- Performance issues

## Security Practices

- GPS coordinates are **never** logged server-side
- All API communication uses HTTPS
- Secrets are managed via environment variables, never in code
- Docker containers run as non-root with minimal capabilities
- Dependencies are scanned with Trivy in CI/CD