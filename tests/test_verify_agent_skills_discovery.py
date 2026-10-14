import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.verify_agent_skills_discovery import digest, verify_served

ROOT = Path(__file__).resolve().parents[1]
INDEX_URL = "https://pages.example.invalid/.well-known/agent-skills/index.json"
SKILL_URL = "https://pages.example.invalid/agent-skills/demo/SKILL.md"


def _index_bytes(content_digest: str) -> bytes:
    index = {"skills": [{"name": "demo", "type": "skill", "url": SKILL_URL, "digest": content_digest}]}
    return json.dumps(index).encode("utf-8")


def test_served_verification_passes_immediately_when_consistent(monkeypatch):
    good = b"fresh bytes"

    def fake_fetch(url: str) -> bytes:
        if url == INDEX_URL:
            return _index_bytes(digest(good))
        return good

    monkeypatch.setattr("tools.verify_agent_skills_discovery.fetch", fake_fetch)
    sleeps: list = []
    monkeypatch.setattr("tools.verify_agent_skills_discovery.time.sleep", lambda s: sleeps.append(s))
    verify_served(INDEX_URL, max_attempts=3, retry_delay=5.0)
    assert sleeps == []


def test_served_verification_retries_until_cdn_serves_consistent_bytes(monkeypatch):
    stale = b"stale bytes from the previous deployment"
    good = b"fresh bytes"
    responses = [stale, stale, good]

    def fake_fetch(url: str) -> bytes:
        if url == INDEX_URL:
            # The index always advertises the digests of the current build;
            # the CDN just lags on some artifact bytes right after publish.
            return _index_bytes(digest(good))
        return responses.pop(0)

    monkeypatch.setattr("tools.verify_agent_skills_discovery.fetch", fake_fetch)
    sleeps: list = []
    monkeypatch.setattr("tools.verify_agent_skills_discovery.time.sleep", lambda s: sleeps.append(s))
    verify_served(INDEX_URL, max_attempts=5, retry_delay=7.0)
    assert sleeps == [7.0, 7.0]


def test_served_verification_retries_transient_fetch_errors(monkeypatch):
    good = b"fresh bytes"
    state = {"skill_calls": 0}

    def fake_fetch(url: str) -> bytes:
        if url == INDEX_URL:
            return _index_bytes(digest(good))
        state["skill_calls"] += 1
        if state["skill_calls"] == 1:
            raise OSError("connection reset by a CDN edge")
        return good

    monkeypatch.setattr("tools.verify_agent_skills_discovery.fetch", fake_fetch)
    monkeypatch.setattr("tools.verify_agent_skills_discovery.time.sleep", lambda s: None)
    verify_served(INDEX_URL, max_attempts=2, retry_delay=0.0)
    assert state["skill_calls"] == 2


def test_served_verification_fails_closed_after_max_attempts(monkeypatch):
    stale = b"stale bytes from the previous deployment"
    good = b"fresh bytes"

    def fake_fetch(url: str) -> bytes:
        if url == INDEX_URL:
            return _index_bytes(digest(good))
        return stale

    monkeypatch.setattr("tools.verify_agent_skills_discovery.fetch", fake_fetch)
    sleeps: list = []
    monkeypatch.setattr("tools.verify_agent_skills_discovery.time.sleep", lambda s: sleeps.append(s))
    with pytest.raises(ValueError, match="served digest mismatch for demo"):
        verify_served(INDEX_URL, max_attempts=3, retry_delay=4.0)
    assert sleeps == [4.0, 4.0]


def test_retry_flags_require_index_url():
    result = subprocess.run(
        [sys.executable, "tools/verify_agent_skills_discovery.py", "--max-attempts", "3"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "require --index-url" in result.stdout + result.stderr


def test_max_attempts_must_be_positive():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_agent_skills_discovery.py",
            "--index-url",
            "https://pages.example.invalid/index.json",
            "--max-attempts",
            "0",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "must be >= 1" in result.stdout + result.stderr
