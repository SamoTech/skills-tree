#!/usr/bin/env python3
"""Verify discovery-index digests against local or served Agent Skills bytes."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse


def digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def load_index(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_local(index: dict, site_root: Path) -> None:
    for item in index["skills"]:
        path = urlparse(item["url"]).path.lstrip("/")
        # Discovery URLs intentionally include the project-site prefix.
        marker = "/agent-skills/"
        if marker not in "/" + path:
            raise ValueError(f"skill URL has no agent-skills path: {item['url']}")
        relative = "agent-skills/" + path.split("/agent-skills/", 1)[1]
        artifact = site_root / relative
        if not artifact.is_file():
            raise ValueError(f"missing published artifact: {artifact}")
        actual = digest(artifact.read_bytes())
        if actual != item["digest"]:
            raise ValueError(f"digest mismatch for {item['name']}: {actual} != {item['digest']}")


def fetch(url: str) -> bytes:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError(f"refusing non-HTTPS URL: {url}")
    request = Request(url, headers={"User-Agent": "skills-tree-discovery-verifier/1.0"})
    with urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise ValueError(f"{url}: HTTP {response.status}")
        return response.read()


def verify_served(index_url: str) -> None:
    index_bytes = fetch(index_url)
    index = json.loads(index_bytes)
    for item in index["skills"]:
        actual = digest(fetch(item["url"]))
        if actual != item["digest"]:
            raise ValueError(f"served digest mismatch for {item['name']}: {actual} != {item['digest']}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index-file", type=Path)
    parser.add_argument("--site-root", type=Path)
    parser.add_argument("--index-url")
    args = parser.parse_args()

    if args.index_file and args.site_root:
        verify_local(load_index(args.index_file), args.site_root)
        print("OK: all local published Agent Skills bytes match discovery digests")
        return 0
    if args.index_url:
        verify_served(args.index_url)
        print("OK: discovery index and all served Agent Skills bytes match SHA-256 digests")
        return 0
    parser.error("provide --index-file and --site-root, or --index-url")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
