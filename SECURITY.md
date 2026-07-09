# Security Policy

## Supported Versions

Security fixes are applied to the latest release and the `main` branch.

## Reporting a Vulnerability

Please do not disclose suspected vulnerabilities in a public issue. Use GitHub's private vulnerability reporting feature when available, or contact the repository owner privately with:

- affected component and version
- reproduction steps
- expected and observed behavior
- potential impact
- suggested mitigation, if known

Reports will be acknowledged as soon as practical. Confirmed issues will be prioritized by severity and documented in release notes after a fix is available.

## Security Controls

TrojanChat uses automated CodeQL analysis, secret scanning, dependency auditing, Trivy filesystem and container scanning, Dependabot updates, non-root containers, and CycloneDX SBOM generation.
