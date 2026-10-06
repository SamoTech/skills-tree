from pathlib import Path

import pytest

from tools.verify_governance import verify_workflow_inventory


def write_workflow(path: Path) -> None:
    path.write_text("name: test\n", encoding="utf-8")


def test_workflow_inventory_accepts_exact_tree(tmp_path):
    write_workflow(tmp_path / "a.yml")
    write_workflow(tmp_path / "b.yaml")

    inventory = """# Workflow Inventory

**Live workflow files:** 2

| Workflow | Classification | Purpose / disposition |
|---|---|---|
| `a.yml` | Supporting validation | test |
| `b.yaml` | Supporting validation | test |
"""

    verify_workflow_inventory(tmp_path, inventory)


def test_workflow_inventory_rejects_missing_or_stale_entries(tmp_path):
    write_workflow(tmp_path / "a.yml")

    inventory = """# Workflow Inventory

**Live workflow files:** 2

| Workflow | Classification | Purpose / disposition |
|---|---|---|
| `a.yml` | Supporting validation | test |
| `stale.yml` | Supporting validation | stale |
"""

    with pytest.raises(SystemExit):
        verify_workflow_inventory(tmp_path, inventory)
