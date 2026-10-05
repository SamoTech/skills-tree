import hashlib
import json
from pathlib import Path

import pytest

from tools.build_agent_skills_discovery import artifact_digest, build_index, validate_index

ROOT = Path(__file__).resolve().parents[1]


def test_artifact_digest_is_sha256():
    assert artifact_digest(b"hello") == "sha256:" + hashlib.sha256(b"hello").hexdigest()


def test_discovery_index_is_schema_valid_and_deterministic():
    first = build_index(ROOT)
    second = build_index(ROOT)
    assert first == second
    assert first["skills"] == sorted(first["skills"], key=lambda item: item["name"])
    assert len(first["skills"]) == 264
    assert all(item["type"] == "skill" for item in first["skills"])
    assert all(item["digest"].startswith("sha256:") for item in first["skills"])
    validate_index(first)


def test_discovery_index_rejects_duplicate_names():
    index = build_index(ROOT)
    index["skills"].append(index["skills"][0].copy())
    with pytest.raises(ValueError, match="duplicate"):
        validate_index(index)
