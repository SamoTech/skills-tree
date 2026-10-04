import json
from pathlib import Path

from tools.verify_jsonld_export import main

ROOT = Path(__file__).resolve().parents[1]


def test_jsonld_projection_is_valid():
    main()


def test_jsonld_index_matches_skill_count():
    registry = json.loads((ROOT / "docs/api/skills.json").read_text(encoding="utf-8"))
    index = json.loads((ROOT / "docs/api/jsonld/index.jsonld").read_text(encoding="utf-8"))
    assert index["numberOfItems"] == registry["count"]
    assert len(index["itemListElement"]) == registry["count"]
