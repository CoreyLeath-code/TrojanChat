# TrojanChat L6 Nine-Tier Deployment Hygiene

This document defines the repository's engineering maturity baseline and the evidence produced by automation.

## Tier 1 — Source Hygiene

- Black formatting policy
- Ruff correctness checks
- Python syntax compilation
- Conventional, reviewable changes

## Tier 2 — Test Engineering

- Maintained unit and API test suite
- Python 3.11 and 3.12 compatibility matrix
- JUnit test reports
- Coverage XML and terminal coverage reports

## Tier 3 — Static Quality

- Blocking syntax and high-confidence Ruff rules
- Formatting findings surfaced without obscuring functional failures
- Reproducible development dependencies

## Tier 4 — Security Engineering

- CodeQL analysis
- Gitleaks repository-history scanning
- Trivy filesystem scanning
- Trivy container-image scanning
- Private vulnerability reporting guidance

## Tier 5 — Supply-Chain Hygiene

- Dependabot for Python, GitHub Actions, and Docker
- pip-audit dependency reports
- CycloneDX SBOM artifacts
- Explicit runtime and development dependency manifests

## Tier 6 — Reproducible Runtime

- Multi-stage Docker build
- Non-root runtime account
- Minimal Python slim image
- Explicit health check
- Deterministic Uvicorn entry point

## Tier 7 — Continuous Delivery

- Pull-request and main-branch verification
- Concurrency cancellation for superseded runs
- Container build and live health smoke test
- Release-readiness contract

## Tier 8 — Release Engineering

- Semantic version tag trigger
- GitHub Release source artifacts
- Generated release notes
- GHCR image publishing

## Tier 9 — Operational Governance

- SECURITY.md disclosure process
- CONTRIBUTING.md validation and review standard
- Architecture and deployment documentation
- Auditable CI artifacts for tests, coverage, dependency findings, and SBOMs

## Promotion Standard

A change is release-ready when correctness tests, compatibility checks, container health validation, security workflows, and release metadata checks are green. Advisory findings are retained as artifacts and should be converted into focused remediation issues rather than hidden or ignored.
