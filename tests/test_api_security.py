#!/usr/bin/env python3
"""
Security hygiene tests for the Architect API (audit finding AUD-011):

- CORS is not a wildcard by default and is environment-configurable.
- The 500 handler does not disclose exception details to clients.

Run:
    pytest tests/test_api_security.py -v
"""

import asyncio
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient

from api import main as api_main
from api.main import app

client = TestClient(app, raise_server_exceptions=False)


class TestCorsPolicy:
    def test_default_policy_is_not_wildcard(self):
        origins, regex = api_main._cors_policy()
        assert origins != ["*"]
        assert "*" not in origins
        assert regex is not None

    def test_default_policy_allows_only_local_development_origins(self):
        _origins, regex = api_main._cors_policy()
        pattern = re.compile(regex or "")
        assert pattern.match("http://localhost:8000")
        assert pattern.match("https://127.0.0.1:5173")
        assert not pattern.match("https://evil.example.com")

    def test_explicit_env_origins_replace_the_default(self, monkeypatch):
        monkeypatch.setenv(
            "SKILLS_TREE_API_CORS_ORIGINS",
            "https://example.com, https://other.example.com",
        )
        origins, regex = api_main._cors_policy()
        assert origins == ["https://example.com", "https://other.example.com"]
        assert regex is None

    def test_wildcard_is_an_explicit_opt_in(self, monkeypatch):
        monkeypatch.setenv("SKILLS_TREE_API_CORS_ORIGINS", "*")
        origins, regex = api_main._cors_policy()
        assert origins == ["*"]
        assert regex is None

    def test_preflight_from_localhost_is_allowed(self):
        response = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:8000",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert (
            response.headers.get("access-control-allow-origin")
            == "http://localhost:8000"
        )

    def test_preflight_from_unknown_origin_is_not_allowed(self):
        response = client.options(
            "/health",
            headers={
                "Origin": "https://evil.example.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.headers.get("access-control-allow-origin") is None


class TestInternalErrorHandler:
    def test_500_response_omits_exception_details(self):
        class FakeURL:
            path = "/health"

        class FakeRequest:
            method = "GET"
            url = FakeURL()

        response = asyncio.run(
            api_main.internal_error_handler(
                FakeRequest(), RuntimeError("SECRET-INTERNAL-DETAIL")
            )
        )
        assert response.status_code == 500
        payload = json.loads(response.body.decode("utf-8"))
        assert payload["error"]["code"] == "INTERNAL_ERROR"
        assert "SECRET-INTERNAL-DETAIL" not in json.dumps(payload)
