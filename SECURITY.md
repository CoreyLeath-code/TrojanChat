
# Security Policy

TrojanChat is committed to maintaining a secure, reliable, and trustworthy application. Security is considered throughout development, testing, dependency management, and deployment.

## Supported Versions

Security fixes are prioritized for the latest maintained release and the `main` branch.

| Version | Supported |
|---------|-----------|
| Latest maintained release | Yes |
| `main` branch | Yes |
| Older unsupported releases | No |

Users should upgrade to the latest maintained version to receive available security fixes.

## Reporting a Vulnerability

If you discover a potential security vulnerability, please report it responsibly.

**Do not disclose security vulnerabilities through public GitHub issues, discussions, or pull requests before remediation.**

### Preferred Reporting Method

Use GitHub's private vulnerability reporting feature when enabled:

1. Navigate to the TrojanChat repository.
2. Select the **Security** tab.
3. Select **Report a vulnerability**, if available.
4. Submit a detailed description of the issue.

Repository:

https://github.com/CoreyLeath-code/TrojanChat

If private vulnerability reporting is unavailable, contact the repository maintainer through an established private communication channel.

### Information to Include

Please provide:

- Affected component and version
- Description of the vulnerability
- Steps required to reproduce the issue
- Expected and observed behavior
- Potential security impact
- Relevant logs or screenshots with sensitive information removed
- Suggested mitigation, if known

Never include passwords, API keys, authentication tokens, or private user information in reports.

## Vulnerability Response Process

Security reports are handled through the following process:

1. **Acknowledgment:** Review the submitted report as soon as practical.
2. **Triage:** Evaluate reproducibility, affected components, and potential impact.
3. **Severity Assessment:** Prioritize the vulnerability according to its severity and exploitability.
4. **Remediation:** Develop and review an appropriate security fix.
5. **Validation:** Run applicable automated tests, static analysis, and regression tests.
6. **Release:** Publish the fix through the appropriate maintained release or branch.
7. **Disclosure:** Document confirmed and remediated vulnerabilities when appropriate.

Response and remediation timelines depend on the vulnerability's severity, complexity, and available maintainer resources.

## Security Controls

TrojanChat uses or may incorporate the following security controls, depending on the repository's active configuration.

### Static Application Security Testing

- GitHub CodeQL analysis
- Automated security checks in GitHub Actions
- Code review and secure coding practices
- Regression testing for identified vulnerabilities

### Dependency Security

- Dependabot dependency monitoring and update pull requests
- Dependency vulnerability auditing
- Dependency version management
- Review and testing of security-related updates

### Secret Management

- Secret scanning where enabled
- Environment-based configuration
- Avoidance of hardcoded credentials
- Restricted access to sensitive configuration
- Credential rotation when exposure is confirmed

### Container Security

- Container image vulnerability scanning using configured tools such as Trivy
- Non-root container execution where configured
- Minimal container privileges
- Dependency and image update reviews
- Software Bill of Materials (SBOM) generation where supported

### Application Security

Security considerations include:

- Input validation
- Authentication and authorization
- Secure session management
- Protection against unauthorized access
- Safe exception handling
- Secure API communication
- Appropriate logging without exposing sensitive information

These controls must be verified against the actual application implementation and deployment configuration.

## Security Testing

Before security-sensitive changes are merged, maintainers should perform applicable checks:

```bash
python -m pytest
```

Additional checks may include:

```bash
python -m pip_audit
```

```bash
trivy fs .
```

```bash
trivy image <image-name>
```

Commands depend on the tools and dependencies installed in the development environment.

Passing automated security checks does not guarantee that an application is free from vulnerabilities.

## Responsible Disclosure

Security researchers are encouraged to follow coordinated disclosure practices.

Please:

- Avoid accessing or modifying other users' data.
- Avoid disrupting application availability.
- Do not exploit vulnerabilities beyond what is necessary for verification.
- Do not publicly disclose unpatched vulnerabilities without coordinating with maintainers.
- Provide sufficient technical details to support investigation and remediation.

## Security Updates

Security-related changes may be communicated through:

- GitHub Security Advisories
- GitHub Releases
- Repository documentation
- Relevant changelog entries

Maintainers will determine the appropriate disclosure and release process based on the vulnerability.

## Security Limitations

TrojanChat is an actively maintained software project.

Automated testing, static analysis, dependency scanning, and container security controls reduce risk but do not guarantee complete protection against all vulnerabilities.

Users deploying TrojanChat are responsible for securing their infrastructure, credentials, networks, and operational environments.

## Maintainer

**Repository Owner:** CoreyLeath-code

**Repository:** https://github.com/CoreyLeath-code/TrojanChat

**Security Reporting:** GitHub private vulnerability reporting, when enabled.

---

_Last reviewed: November 2026_
