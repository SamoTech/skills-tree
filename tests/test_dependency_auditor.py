from pathlib import Path

from tools.dependency_auditor import (
    AuditResult,
    Dependency,
    _safe_env,
    extract_python_snippets,
    parse_dependencies,
)


def test_parse_canonical_dependencies() -> None:
    text = """---
dependencies:
  - package: httpx
    min_version: "0.28.0"
    tested_version: "0.28.1"
    confidence: verified
  - package: packaging
    confidence: machine-inferred
---
"""
    deps = parse_dependencies(text)
    assert [(d.package, d.version, d.confidence) for d in deps] == [
        ("httpx", "0.28.1", "verified"),
        ("packaging", None, "machine-inferred"),
    ]


def test_parse_legacy_deps_for_migration() -> None:
    text = """---
deps:
  - package: httpx
    version: "0.28.1"
    confidence: verified
---
"""
    deps = parse_dependencies(text)
    assert len(deps) == 1
    assert deps[0].package == "httpx"
    assert deps[0].version == "0.28.1"


def test_extracts_all_executable_python_and_skips_illustrative() -> None:
    text = """---
title: Example
---
```python
print("one")
```

```python type: illustrative
print("illustrative")
```

```python
print("two")
```
"""
    snippets = extract_python_snippets(text)
    assert len(snippets) == 2
    assert "one" in snippets[0]
    assert "two" in snippets[1]
    assert all("illustrative" not in snippet for snippet in snippets)


def test_build_specs_preserves_pinned_versions() -> None:
    from tools.dependency_auditor import build_pip_specs

    assert build_pip_specs([Dependency(package="httpx", version="0.28.1"), Dependency(package="packaging")]) == ["httpx==0.28.1", "packaging"]


def test_timeout_cannot_become_a_pass() -> None:
    result = AuditResult(
        skill_path=Path("skills/example.md"),
        skill_key="skills-example",
        deps=[Dependency(package="httpx")],
        install_ok=True,
        snippet_ok=False,
        snippet_skipped=False,
        error="snippet 1 timed out after 30s",
    )
    assert result.passed is False


def test_snippet_environment_excludes_runner_secrets(monkeypatch) -> None:
    monkeypatch.setenv("GITHUB_TOKEN", "secret")
    env = _safe_env(Path("/tmp/venv"), "/tmp/audit")
    assert "GITHUB_TOKEN" not in env
    assert env["HOME"] == "/tmp/audit"
