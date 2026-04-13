#!/usr/bin/env python3
"""
tools/common.py

Shared utilities for the Skills Tree Dependency Watchdog pipeline.

Import from here, never duplicate:
    from common import skill_path_to_badge_key

This module is intentionally minimal. Every function here must be
used by at least two tools. Keep it free of third-party imports so
it can be imported anywhere without a venv.
"""

from pathlib import Path


def skill_path_to_badge_key(skill_path: str) -> str:
    """
    Convert a skill file path to its badge JSON key.

    Rules (applied in order):
      1. Coerce to str (accepts Path objects)
      2. Normalise Windows backslashes to forward slashes
      3. Strip a leading './' if present (git sometimes produces it)
      4. Replace all '/' with '-'
      5. Strip the '.md' extension

    Examples:
        'skills/05-code/code-review.md'  -> 'skills-05-code-code-review'
        'skills\\05-code\\code-review.md' -> 'skills-05-code-code-review'
        './skills/05-code/code-review.md' -> 'skills-05-code-code-review'

    The single source of truth for key generation across:
        - tools/ast_sweep.py   (badge state computation)
        - tools/write_badge.py (manual CLI)
        - tools/osv_check.py   (advisory badge writes)
        - .github/workflows/   (via Python inline scripts)
    """
    key = str(skill_path)
    key = key.replace("\\", "/")     # Windows → POSIX
    key = key.lstrip("./")           # Strip leading ./ or /
    # Collapse any accidental double-slashes that survive the lstrip
    while "//" in key:
        key = key.replace("//", "/")
    key = key.replace("/", "-")
    if key.endswith(".md"):
        key = key[:-3]
    return key


# ─── STDLIB detection ────────────────────────────────────────────────────────
# Used by ast_sweep.py to filter standard library imports.
# Defined here so the fallback logic is tested in one place.

# Hardcoded baseline: modules present in every CPython >= 3.8.
# This list is intentionally conservative — it's the FLOOR, not the ceiling.
# sys.stdlib_module_names (3.10+) is authoritative and always preferred.
_STDLIB_BASELINE: frozenset[str] = frozenset({
    # Built-ins / always-there
    "__future__", "_thread", "abc", "ast", "asyncio", "builtins",
    "cProfile", "calendar", "cmath", "cmd", "code", "codecs",
    "collections", "colorsys", "compileall", "concurrent", "contextlib",
    "contextvars", "copy", "copyreg", "csv", "ctypes",
    # D-F
    "dataclasses", "datetime", "decimal", "difflib", "dis",
    "email", "encodings", "enum", "errno",
    "filecmp", "fnmatch", "fractions", "ftplib", "functools",
    # G-I
    "gc", "getopt", "getpass", "glob", "gzip",
    "hashlib", "heapq", "hmac", "html", "http",
    "imaplib", "importlib", "inspect", "io", "itertools",
    # J-L
    "json",
    "keyword",
    "lib2to3", "linecache", "locale", "logging",
    # M-O
    "math", "mimetypes", "multiprocessing",
    "numbers",
    "operator", "os",
    # P-R
    "pathlib", "pickle", "pkgutil", "platform", "pprint",
    "profile", "pstats", "pty", "pwd",
    "queue",
    "random", "re",
    # S-T
    "select", "shelve", "shlex", "shutil", "signal",
    "socket", "socketserver", "sqlite3", "ssl", "stat",
    "statistics", "string", "struct", "subprocess", "sys", "sysconfig",
    "tarfile", "tempfile", "textwrap", "threading", "time",
    "timeit", "tkinter", "tomllib", "traceback", "tracemalloc",
    "types", "typing",
    # U-Z
    "unicodedata", "unittest", "urllib", "uuid",
    "venv",
    "warnings", "weakref",
    "xml", "xmlrpc",
    "zipfile", "zipimport", "zlib", "zoneinfo",
})


def get_stdlib_modules() -> frozenset[str]:
    """
    Return the set of standard library module names for the current Python.

    Priority order:
      1. sys.stdlib_module_names  (Python 3.10+ — authoritative, exhaustive)
      2. pkgutil walk of stdlib path (Python 3.8-3.9 — best-effort)
      3. _STDLIB_BASELINE hardcoded set (ultimate fallback — never empty)

    Never raises. Returns a frozenset so callers can use `in` efficiently.
    """
    import sys

    # Best path: Python 3.10+
    if hasattr(sys, "stdlib_module_names"):
        return frozenset(sys.stdlib_module_names)

    # Walk the stdlib directory — works on 3.8/3.9, portable
    try:
        import sysconfig
        import pkgutil
        stdlib_path = sysconfig.get_paths()["stdlib"]
        walked = {
            mod.name
            for mod in pkgutil.iter_modules(path=[stdlib_path])
        }
        if walked:  # Sanity: the walk should return hundreds of names
            return frozenset(walked) | _STDLIB_BASELINE
    except Exception:
        pass  # Fall through to baseline

    # Ultimate fallback: hardcoded baseline
    # Fail-safe: never returns an empty set, never misclassifies common stdlib
    # as third-party (which would cause false Orange badges).
    return _STDLIB_BASELINE
