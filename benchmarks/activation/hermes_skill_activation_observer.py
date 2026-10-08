"""Minimal Hermes observer plugin for capturing real skill-activation evidence.

This plugin records only explicit skill_view and on_skill_lifecycle facts needed by
Skills Tree's activation benchmark. It intentionally omits prompts, model output,
tool results, and aggregate counters.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Any

def _path() -> Path:
    return Path(os.environ.get("SKILLS_TREE_HERMES_TRACE", "hermes-skill-activation.jsonl")).expanduser()

def _write(event: dict[str, Any]) -> None:
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")
        handle.flush()

def on_tool_call(tool_name: str, args: Any, result: Any, **kwargs: Any) -> None:
    if tool_name != "skill_view" or not isinstance(args, dict):
        return
    name = args.get("name")
    if not name:
        return
    _write({"hook_event_name": "post_tool_call", "tool_name": "skill_view", "args": {"name": str(name)}, "session_id": str(kwargs.get("session_id") or ""), "task_id": str(kwargs.get("task_id") or "")})

def on_skill_lifecycle(action: str, skill_name: str, task_id: str = "", session_id: str = "", **kwargs: Any) -> None:
    if action != "loaded" or not skill_name:
        return
    _write({"hook_event_name": "on_skill_lifecycle", "action": "loaded", "skill_name": str(skill_name), "session_id": str(session_id or ""), "task_id": str(task_id or "")})

def register(ctx: Any) -> None:
    ctx.register_hook("post_tool_call", on_tool_call)
    ctx.register_hook("on_skill_lifecycle", on_skill_lifecycle)
