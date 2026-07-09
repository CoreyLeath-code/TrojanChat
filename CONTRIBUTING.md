# Contributing to TrojanChat

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

## Required Local Validation

```bash
black --check app tests/test_api.py tests/test_chat_service.py tests/test_inference_cache.py
ruff check app tests/test_api.py tests/test_chat_service.py tests/test_inference_cache.py
PYTHONPATH=. CACHE_ENABLED=false pytest tests/test_api.py tests/test_chat_service.py tests/test_inference_cache.py --cov=app
```

## Pull Requests

- Use a focused branch and conventional commit messages.
- Explain the problem, design choice, test evidence, and operational impact.
- Add or update tests for behavior changes.
- Do not commit credentials, tokens, local `.env` files, generated artifacts, or customer data.
- Keep backward compatibility unless the PR documents a migration path.

## Review Standard

Reviewers should evaluate correctness, security, observability, failure behavior, maintainability, performance, and deployment impact rather than only checking whether the happy path works.
