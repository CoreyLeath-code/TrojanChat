# Changelog
All notable changes to TrojanChat will be documented in this file.

## [Unreleased]
### Added
- Reproducible before/after latency, throughput, and peak-memory benchmark with raw JSON evidence.
- Unit and integration tests for bounded storage, negative API cases, and WebSocket lifecycle.
- CodeQL default-setup documentation, blocking static/security scans, audit, and production checklist.

### Changed
- Canonical critical-path coverage is enforced at 90%.
- Message retention is bounded and thread-safe; API inputs and history queries are constrained.

### Performance
- Reference run reduced peak Python allocations by 80.06% with a 6.8% throughput tradeoff.

### Security
- Sanitized internal errors and changed dependency/Trivy findings from advisory to blocking.

## [0.2.0] - 2026-04-02
### Changed
- **Python runtime**: Docker base image upgraded from `python:3.10-slim` to `python:3.12-slim`
- **CI/CD**: GitHub Actions updated â€” `actions/checkout@v3â†’v4`, `actions/setup-python@v4â†’v5`, Python `3.11â†’3.12`
- **CI/CD**: Fixed `backend/requirements.txt` reference (created missing file) and corrected test runner path
- **requirements.txt**: Pinned minimum versions for all Python dependencies; added `pydantic-settings>=2.5.0`, `fastapi>=0.115.0`, `uvicorn>=0.30.0`, `httpx>=0.27.0`, `pytest-asyncio>=0.24.0`
- **Pydantic v2**: Migrated `BaseSettings` import in `app/core/app/core/config.py` from `pydantic` to `pydantic_settings` package
- **Deprecation fixes**: Replaced `datetime.utcnow()` (deprecated in Python 3.12) with `datetime.now(timezone.utc)` in `mcp_adapter.py`, `app/core/security.py`, and `backend/services/chat_service.py`
- **Node.js (server/)**: Upgraded dependencies â€” `express@4.18â†’4.21`, `socket.io@4.7â†’4.8`, `mongoose@7â†’8`, `dotenv@16.0â†’16.4`, `jest@29.5â†’29.7`, `supertest@6â†’7`, `nodemon@2â†’3`

### Breaking Changes
- **Pydantic v2**: `BaseSettings` is no longer exported from `pydantic`; it requires the `pydantic-settings` package. Run `pip install pydantic-settings` or use the updated `requirements.txt`.
- **Mongoose 8**: See the [Mongoose 8 migration guide](https://mongoosejs.com/docs/migrating_to_8.html) for any schema or query API changes.

## [0.1.0] - 2025-03-01
### Added
- Initial FastAPI backend
- MongoDB + Redis integration
- JWT authentication
- Docker & CUDA support
- Render deployment support
- Metrics, logging, and rate limiting

### Changed
- Improved container startup time
- Optimized async database access

### Security
- Added JWT expiration
- Added request rate limiting
