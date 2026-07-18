"""Regression tests for symmetric JWT behavior after removing python-jose/ecdsa."""

import importlib
import sys


def load_security(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "test-only-secret-that-is-at-least-32-bytes")
    sys.modules.pop("app.core.security", None)
    return importlib.import_module("app.core.security")


def test_access_token_round_trip(monkeypatch) -> None:
    security = load_security(monkeypatch)
    token = security.create_access_token({"sub": "user-1", "role": "member"})
    payload = security.verify_token(token)
    assert payload["sub"] == "user-1"
    assert payload["role"] == "member"
    assert "exp" in payload


def test_invalid_token_is_rejected(monkeypatch) -> None:
    security = load_security(monkeypatch)
    assert security.verify_token("not-a-jwt") is None
