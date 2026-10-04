#!/usr/bin/env python3
"""Validate the deterministic JSON-LD projection emitted by export_skills.py."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = ROOT / "docs" / "api"
JSON_INDEX = API / "skills.json"
JSONLD_ROOT = API / "jsonld"
JSONLD_INDEX = JSONLD_ROOT / "index.jsonld"


def fail(message: str) -> None:
    raise SystemExit(f"JSON-LD validation failed: {message}")


def load(path: Path):
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def main() -> None:
    registry = load(JSON_INDEX)
    skills = registry.get("skills")
    if not isinstance(skills, list):
        fail("skills.json.skills must be an array")

    index = load(JSONLD_INDEX)
    if index.get("@type") != "ItemList":
        fail("JSON-LD index must have @type=ItemList")
    items = index.get("itemListElement")
    if not isinstance(items, list) or len(items) != len(skills):
        fail("JSON-LD ItemList count does not match skills.json")

    urls = []
    for position, skill in enumerate(skills, 1):
        skill_id = skill.get("id")
        category = skill.get("category_dir") or "uncategorized"
        if not skill_id:
            fail(f"skill at position {position} has no id")
        path = JSONLD_ROOT / category / f"{skill_id}.jsonld"
        doc = load(path)

        if doc.get("@type") != "TechArticle":
            fail(f"{path.relative_to(ROOT)} must have @type=TechArticle")
        if doc.get("@id") != doc.get("url"):
            fail(f"{path.relative_to(ROOT)} has mismatched @id and url")
        if doc.get("skillId") != skill_id:
            fail(f"{path.relative_to(ROOT)} skillId does not match registry")
        if doc.get("name") != skill.get("name"):
            fail(f"{path.relative_to(ROOT)} name does not match registry")

        urls.append(doc["url"])
        item = items[position - 1]
        if item.get("@type") != "ListItem" or item.get("position") != position:
            fail(f"ItemList position {position} is invalid")
        if item.get("url") != doc["url"] or item.get("name") != doc["name"]:
            fail(f"ItemList item {position} does not match skill projection")

    if index.get("numberOfItems") != len(skills):
        fail("ItemList numberOfItems does not match skills.json")
    if len(set(urls)) != len(urls):
        fail("duplicate JSON-LD skill URLs detected")

    print(f"PASS: validated {len(skills)} skill JSON-LD documents and the ItemList index.")


if __name__ == "__main__":
    main()
