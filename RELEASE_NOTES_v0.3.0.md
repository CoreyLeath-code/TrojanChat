# TrojanChat v0.3.0 Release Notes

## Release workflow contract

TrojanChat already has a GitHub Actions release workflow at `.github/workflows/release.yml`.

Publishing a semantic-version tag matching `v*.*.*` (for example, `v0.3.0`) triggers the workflow. It can also be started manually with `workflow_dispatch`.

For a tag-triggered release, the workflow:

1. Checks out the tagged repository revision.
2. Uses Python 3.11 for the release job environment.
3. Builds a source archive at `dist/trojanchat-${GITHUB_REF_NAME}.tar.gz` while excluding `.git` and `dist`.
4. Creates a GitHub Release with `softprops/action-gh-release@v3`.
5. Attaches the source archive to the GitHub Release.
6. Generates the GitHub Release notes automatically from repository history.
7. Logs into GitHub Container Registry using `GITHUB_TOKEN`.
8. Builds the repository Docker image and publishes it to GHCR using metadata generated for the current Git ref.

The workflow has `contents: write` and `packages: write` permissions to support the GitHub Release and GHCR publication.

## v0.3.0 scope

This release promotes the changes currently documented under `Unreleased` in `CHANGELOG.MD`. No new runtime capability is claimed by this release-preparation change.

Documented changes include:

- Reproducible before/after latency, throughput, and peak-memory benchmarking with raw JSON evidence.
- Unit and integration tests covering bounded storage, negative API cases, and WebSocket lifecycle behavior.
- Blocking static/security scans, dependency auditing, and production-readiness documentation.
- 90% canonical critical-path coverage enforcement.
- Bounded, thread-safe message retention and constrained API/history inputs.
- Sanitized internal errors and blocking dependency/container security findings.
- Next.js dependency/security maintenance documented in the changelog.

The changelog's existing performance result reports an 80.06% reduction in peak Python allocations with a 6.8% throughput tradeoff. This release note preserves that existing repository claim rather than introducing a new measurement.

## Publishing

After this release-preparation PR is reviewed and merged to `main`, create and push the `v0.3.0` tag from the intended release commit. The existing release workflow will then create the GitHub Release and publish the container image according to the contract above.
