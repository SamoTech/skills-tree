#!/usr/bin/env python3
"""
Architect MCP Server v1 — Sprint C-10

A lightweight stdio MCP server that exposes the existing Architect capabilities
as MCP tools:
  - recommend_skills
  - generate_blueprint
  - list_goals
  - list_skills

Design goals
------------
- No duplicated business logic.
- Reuse existing API layer (api.main) end-to-end.
- Be compatible with Claude Desktop / Cursor / VS Code MCP launch patterns.

Protocol support
----------------
Implements a minimal JSON-RPC 2.0 subset over stdio sufficient for:
  - initialize
  - tools/list
  - tools/call

Run locally
-----------
    python -m mcp.server
or
    python mcp/server.py
"""

from __future__ import annotations

import json
import sys
import traceback
from typing import Any, Dict

from mcp.tools import tool_schemas, dispatch_tool, MCPToolError

SERVER_INFO = {
    "name": "architect-mcp-server",
    "version": "1.0.0",
}


def _read_message() -> Dict[str, Any] | None:
    line = sys.stdin.readline()
    if not line:
        return None
    line = line.strip()
    if not line:
        return None
    return json.loads(line)


def _write_message(payload: Dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload) + "\n")
    sys.stdout.flush()


def _success(id_: Any, result: Dict[str, Any]) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": id_, "result": result}


def _error(id_: Any, code: int, message: str, data: Any = None) -> Dict[str, Any]:
    err = {"code": code, "message": message}
    if data is not None:
        err["data"] = data
    return {"jsonrpc": "2.0", "id": id_, "error": err}


def handle_request(request: Dict[str, Any]) -> Dict[str, Any] | None:
    method = request.get("method")
    id_    = request.get("id")
    params = request.get("params", {})

    if method == "initialize":
        return _success(id_, {
            "protocolVersion": "2025-03-26",
            "serverInfo": SERVER_INFO,
            "capabilities": {
                "tools": {},
            },
        })

    if method == "notifications/initialized":
        return None

    if method == "tools/list":
        return _success(id_, {"tools": tool_schemas()})

    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments", {})
        try:
            result = dispatch_tool(name, arguments)
            return _success(id_, {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2),
                    }
                ]
            })
        except MCPToolError as exc:
            return _error(id_, -32000, str(exc))
        except Exception as exc:  # defensive server boundary
            return _error(id_, -32603, "Internal error", data={"detail": str(exc)})

    return _error(id_, -32601, f"Method not found: {method}")


def main() -> None:
    while True:
        try:
            request = _read_message()
            if request is None:
                continue
            response = handle_request(request)
            if response is not None:
                _write_message(response)
        except KeyboardInterrupt:
            break
        except Exception as exc:  # hard boundary: never crash silently
            _write_message(_error(None, -32603, "Server crash", data={
                "detail": str(exc),
                "traceback": traceback.format_exc(),
            }))


if __name__ == "__main__":
    main()
