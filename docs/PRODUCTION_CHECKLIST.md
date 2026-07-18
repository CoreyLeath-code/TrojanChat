# Production checklist

- [ ] All CI, CodeQL, secret, dependency, filesystem, and container scans pass for the release SHA.
- [ ] Coverage remains at or above 90% for the canonical critical path.
- [ ] Benchmark regression is within budget and raw artifacts are retained.
- [ ] Image digest, SBOM, provenance, changelog, and rollback target are recorded.
- [ ] TLS, WebSocket authentication/origin policy, API rate limits, and request limits are enforced.
- [ ] Durable shared message storage is deployed, backed up, and restore-tested.
- [ ] Redis/Qdrant health, timeouts, resource limits, logs, metrics, and alerts have owners.
- [ ] A canary validates `/health`, message send/history, WebSocket lifecycle, and AI dependency failure.
- [ ] Previous image and schema/model revisions can be restored within the recovery objective.
