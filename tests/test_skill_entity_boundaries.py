import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

_DIRECT_SKILL_ALIAS_PATTERNS = (
    re.compile(r"\bthis\s+skill\s+is\s+(?:an?\s+)?(?:agent\s+)?capabilit(?:y|ies)\b", re.I),
    re.compile(r"\b(?:this\s+skill|the\s+skill|skill)\s+(?:represents|means)\s+(?:an?\s+)?(?:agent\s+)?capabilit(?:y|ies)\b", re.I),
    re.compile(r"\b(?:this\s+skill|the\s+skill|skill)\s+itself\s+is\s+(?:an?\s+)?(?:agent\s+)?capabilit(?:y|ies)\b", re.I),
)


def test_skill_documents_do_not_define_skill_as_capability():
    violations = []
    for path in sorted(SKILLS.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for pattern in _DIRECT_SKILL_ALIAS_PATTERNS:
            if pattern.search(text):
                violations.append(str(path.relative_to(ROOT)))
                break

    assert violations == []


def test_skill_when_to_use_language_does_not_alias_skill_as_capability():
    violations = []
    for path in sorted(SKILLS.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if re.search(r"\bUse this capability\b", text, re.I):
            violations.append(str(path.relative_to(ROOT)))

    assert violations == []


def test_skill_security_boundary_does_not_grant_authorization():
    violations = []
    for path in sorted(SKILLS.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split()).lower()
        if re.search(r"\bskill\b.{0,120}\b(grants?|creates?|gives?|provides?)\b.{0,80}\bauthori[sz]ation\b", normalized):
            if "does not authorize" not in normalized and "doesn't authorize" not in normalized:
                violations.append(str(path.relative_to(ROOT)))

    assert violations == []
