# Production-readiness audit

## Executive assessment

TrojanChat contains useful FastAPI, WebSocket, Redis-cache, frontend, container, and supply-chain
building blocks, but its repository layout combines multiple generations and languages without a
single declared support boundary. This change designates `backend.api:app` as the canonical service
and makes its evidence enforceable rather than aspirational.

## Strengths

- Dependency-injected AI tests avoid network calls and credentials.
- Non-root multi-stage container with an HTTP health check.
- Dependabot, SBOM, secret scan, Trivy, CodeQL default setup, and tag-driven release automation.
- Cache failures are designed to fail open without blocking inference.

## Findings and disposition

| Priority | Finding | Disposition |
|---|---|---|
| P0 | Benchmark workflow reported success and â€œsub-millisecondâ€ performance without running a benchmark | Replaced with reproducible latency/throughput/memory comparison and artifact |
| P1 | Dependency and vulnerability findings did not fail CI | Audits and HIGH/CRITICAL Trivy findings now block |
| P1 | Coverage was reported but had no minimum | Canonical critical path now fails below 90% |
| P1 | Message history grew without bound | Bounded retention with configurable `CHAT_HISTORY_LIMIT` |
| P1 | Message fields and history limit were unbounded | Strict username/content/query validation added |
| P2 | WebSocket router existed but was not mounted | Mounted and integration-tested connection lifecycle |
| P2 | Exceptions were reflected to callers | Replaced with sanitized 503 responses |
| P2 | Multiple duplicate legacy trees obscure ownership | Documented; removal requires a separate migration PR |

## Residual risk

- The in-process store is neither durable nor shared. Production multi-instance deployments require
  Redis Streams, Postgres, or another durable ordered store with tenant-aware authorization.
- WebSocket authentication, origin policy, rate limiting, message schema enforcement, and TLS
  termination remain required before exposing realtime chat publicly.
- Runtime requirements use lower bounds rather than a lock file. Release builds should generate and
  review a hashed lock before claiming byte-for-byte reproducibility.
- AI accuracy, safety, precision/recall, and retrieval quality cannot be claimed without a versioned,
  representative labeled evaluation dataset.
