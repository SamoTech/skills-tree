#!/usr/bin/env python3
"""
Architect CLI v1 — Sprint C-11

Installable command-line interface for the Skills Tree Architect engine.
Exposes every Architect capability as a first-class terminal command.

Commands
--------
skills-tree recommend   --goal <str> [--experience <lvl>] [--time-budget <hrs>] [--format <fmt>]
skills-tree blueprint   --goal <str> [--format <fmt>]
skills-tree goals       [--format <fmt>]
skills-tree skills      [--format <fmt>]
skills-tree validate    [--goal <str>]

Usage
-----
    pip install -e .
    skills-tree recommend --goal "Coding Agent"
    skills-tree recommend --goal "RAG Assistant" --experience intermediate --time-budget 80
    skills-tree blueprint --goal "Coding Agent"
    skills-tree goals
    skills-tree skills
    skills-tree validate
    skills-tree validate --goal "Coding Agent"

Design
------
- Zero duplicated logic: CLI calls the existing API layer via FastAPI TestClient.
- Output formats: json (default), pretty, table.
- All exits follow POSIX conventions: 0 = success, 1 = user error, 2 = engine error.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Dict, List, Optional

import typer
from fastapi.testclient import TestClient
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from api.main import app as _api_app

# ---------------------------------------------------------------------------
# Typer app
# ---------------------------------------------------------------------------

app = typer.Typer(
    name="skills-tree",
    help="Architect — taxonomy-driven skill recommendation engine for AI agent builders.",
    add_completion=False,
    no_args_is_help=True,
)

console = Console()
_client: Optional[TestClient] = None


def _get_client() -> TestClient:
    global _client
    if _client is None:
        _client = TestClient(_api_app)
    return _client


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def _output(data: Any, fmt: str) -> None:
    if fmt == "json":
        typer.echo(json.dumps(data, indent=2))
    elif fmt == "pretty":
        rprint(data)
    elif fmt == "table":
        _print_table(data)
    else:
        typer.echo(json.dumps(data, indent=2))


def _print_table(data: Any) -> None:
    if isinstance(data, list):
        if not data:
            console.print("[yellow]No results.[/yellow]")
            return
        table = Table(show_header=True, header_style="bold cyan")
        for key in data[0].keys():
            table.add_column(str(key))
        for row in data:
            table.add_row(*[str(v) for v in row.values()])
        console.print(table)
    elif isinstance(data, dict):
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Field")
        table.add_column("Value")
        for k, v in data.items():
            table.add_row(str(k), json.dumps(v) if isinstance(v, (dict, list)) else str(v))
        console.print(table)
    else:
        console.print(str(data))


def _error(msg: str, code: int = 1) -> None:
    console.print(f"[bold red]Error:[/bold red] {msg}")
    raise typer.Exit(code=code)


# ---------------------------------------------------------------------------
# recommend
# ---------------------------------------------------------------------------

@app.command()
def recommend(
    goal: str = typer.Option(..., "--goal", "-g", help="Goal name or ID, e.g. 'Coding Agent' or 'G01'"),
    experience: str = typer.Option("intermediate", "--experience", "-e",
                                    help="Experience level: beginner | intermediate | advanced"),
    time_budget: Optional[int] = typer.Option(None, "--time-budget", "-t",
                                               help="Study time budget in hours"),
    fmt: str = typer.Option("json", "--format", "-f",
                             help="Output format: json | pretty | table"),
) -> None:
    """Get skill recommendations for a goal."""
    payload: Dict[str, Any] = {"goal": goal, "experience": experience}
    if time_budget is not None:
        payload["time_budget_hours"] = time_budget

    client = _get_client()
    response = client.post("/recommend", json=payload)

    if response.status_code == 404:
        _error(f"Goal not found: '{goal}'. Run 'skills-tree goals' to list available goals.", code=1)
    if response.status_code == 422:
        detail = response.json().get("detail", response.text)
        _error(f"Invalid input: {detail}", code=1)
    if response.status_code >= 500:
        _error(f"Engine error: {response.text}", code=2)

    data = response.json()
    _output(data, fmt)


# ---------------------------------------------------------------------------
# blueprint
# ---------------------------------------------------------------------------

@app.command()
def blueprint(
    goal: str = typer.Option(..., "--goal", "-g", help="Goal name or ID"),
    fmt: str = typer.Option("json", "--format", "-f", help="Output format: json | pretty | table"),
) -> None:
    """Generate a full architecture blueprint for a goal."""
    client = _get_client()
    response = client.post("/blueprint", json={"goal": goal})

    if response.status_code == 404:
        _error(f"Goal not found: '{goal}'. Run 'skills-tree goals' to list available goals.", code=1)
    if response.status_code >= 500:
        _error(f"Engine error: {response.text}", code=2)

    _output(response.json(), fmt)


# ---------------------------------------------------------------------------
# goals
# ---------------------------------------------------------------------------

@app.command()
def goals(
    fmt: str = typer.Option("json", "--format", "-f", help="Output format: json | pretty | table"),
) -> None:
    """List all taxonomy goals."""
    client = _get_client()
    response = client.get("/goals")
    if response.status_code >= 400:
        _error(f"Failed to fetch goals: {response.text}", code=2)
    _output(response.json()["goals"], fmt)


# ---------------------------------------------------------------------------
# skills
# ---------------------------------------------------------------------------

@app.command()
def skills(
    fmt: str = typer.Option("json", "--format", "-f", help="Output format: json | pretty | table"),
) -> None:
    """List all graph skills."""
    client = _get_client()
    response = client.get("/skills")
    if response.status_code >= 400:
        _error(f"Failed to fetch skills: {response.text}", code=2)
    _output(response.json()["skills"], fmt)


# ---------------------------------------------------------------------------
# validate
# ---------------------------------------------------------------------------

@app.command()
def validate(
    goal: Optional[str] = typer.Option(None, "--goal", "-g",
                                        help="Optional: validate a specific goal end-to-end"),
    fmt: str = typer.Option("json", "--format", "-f", help="Output format: json | pretty | table"),
) -> None:
    """
    Validate the Architect stack health.

    Without --goal: runs a full stack health check (health, goals count, skills count).
    With --goal:    additionally runs a dry recommend + blueprint for the given goal.
    """
    client = _get_client()
    report: Dict[str, Any] = {"status": "ok", "checks": {}}

    # Health endpoint
    h = client.get("/health")
    report["checks"]["health"] = {
        "status_code": h.status_code,
        "pass": h.status_code == 200,
        "body": h.json() if h.status_code == 200 else h.text,
    }

    # Goals
    g = client.get("/goals")
    goals_data = g.json().get("goals", []) if g.status_code == 200 else []
    report["checks"]["goals"] = {
        "status_code": g.status_code,
        "pass": g.status_code == 200,
        "goal_count": len(goals_data),
    }

    # Skills
    s = client.get("/skills")
    skills_data = s.json().get("skills", []) if s.status_code == 200 else []
    report["checks"]["skills"] = {
        "status_code": s.status_code,
        "pass": s.status_code == 200,
        "skill_count": len(skills_data),
    }

    # Optional goal-specific validation
    if goal:
        rec = client.post("/recommend", json={"goal": goal, "experience": "intermediate"})
        report["checks"]["recommend"] = {
            "goal": goal,
            "status_code": rec.status_code,
            "pass": rec.status_code == 200,
        }
        bp = client.post("/blueprint", json={"goal": goal})
        report["checks"]["blueprint"] = {
            "goal": goal,
            "status_code": bp.status_code,
            "pass": bp.status_code == 200,
        }

    # Overall
    all_pass = all(v.get("pass", False) for v in report["checks"].values())
    report["status"] = "ok" if all_pass else "degraded"
    report["all_pass"] = all_pass

    _output(report, fmt)
    if not all_pass:
        raise typer.Exit(code=2)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app()
