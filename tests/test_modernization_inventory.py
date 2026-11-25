"""Freshness contract for the modernization inventory (issue #699).

Pattern of tests/test_quality_report_freshness.py: the committed
meta/MODERNIZATION-INVENTORY.md must be byte-identical to the deterministic
render of tools/modernization_inventory.py over the live canonical corpus and
committed badges. The projection carries no timestamp fields, so there are no
exclusions.
"""

from __future__ import annotations

import re

from tools.modernization_inventory import (
    INVENTORY_PATH,
    build_inventory_markdown,
    build_records,
    render_markdown,
)


def test_modernization_inventory_is_deterministic() -> None:
    assert build_inventory_markdown() == build_inventory_markdown()


def test_modernization_inventory_is_byte_fresh() -> None:
    committed = INVENTORY_PATH.read_text(encoding="utf-8")
    assert committed == build_inventory_markdown(), (
        "meta/MODERNIZATION-INVENTORY.md is stale or absent; run "
        "python tools/modernization_inventory.py and commit the output"
    )


def test_modernization_inventory_covers_whole_corpus() -> None:
    records = build_records()
    markdown = render_markdown(records)
    total = len(records)
    m = re.search(r"\*\*Total canonical skill files:\*\* (\d+)", markdown)
    assert m and int(m.group(1)) == total
    assert "Coverage:" in markdown
