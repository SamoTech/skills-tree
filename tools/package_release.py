#!/usr/bin/env python3
"""
package_release.py — Skills Tree release packaging tool

Builds a self-contained zip artifact of the full skill catalog +
API artifacts and a MANIFEST.json file, placed in dist/.

Usage:
    python3 tools/package_release.py --tag v2.3.0

Outputs:
    dist/skills-tree-{tag}.zip
    dist/MANIFEST.json
"""

import argparse
import hashlib
import json
import os
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent
DIST_DIR = REPO_ROOT / "dist"
SKILLS_DIR = REPO_ROOT / "skills"
SYSTEMS_DIR = REPO_ROOT / "systems"
BLUEPRINTS_DIR = REPO_ROOT / "blueprints"
BENCHMARKS_DIR = REPO_ROOT / "benchmarks"
LABS_DIR = REPO_ROOT / "labs"
API_DIR = REPO_ROOT / "docs" / "api"

# Directories to include in the zip, mapped to their in-zip prefix
CONTENT_DIRS = [
    (SKILLS_DIR, "skills"),
    (SYSTEMS_DIR, "systems"),
    (BLUEPRINTS_DIR, "blueprints"),
    (BENCHMARKS_DIR, "benchmarks"),
    (LABS_DIR, "labs"),
]

# API files to include under api/ in the zip
API_FILES = [
    "skills.json",
    "skills.yaml",
    "skills-schema.json",
]


def count_skills(skills_dir: Path) -> tuple[int, int, int, int]:
    """Return (total, v1, v2, v3) skill counts."""
    total = v1 = v2 = v3 = 0
    for md_file in skills_dir.rglob("*.md"):
        if md_file.name in ("README.md", "index.md"):
            continue
        total += 1
        # Quick version detection via frontmatter scan (no full YAML parse needed)
        try:
            text = md_file.read_text(encoding="utf-8", errors="ignore")
            lines = text.splitlines()
            in_fm = False
            ver = 1
            for line in lines:
                if line.strip() == "---":
                    in_fm = not in_fm
                    if not in_fm and ver != 1:
                        break
                    continue
                if in_fm and line.startswith("version:"):
                    raw = line.split(":", 1)[1].strip().strip('"').strip("'")
                    if raw.startswith("v"):
                        raw = raw[1:]
                    try:
                        ver = int(raw.split(".")[0])
                    except ValueError:
                        ver = 1
                    break
            if ver >= 3:
                v3 += 1
            elif ver >= 2:
                v2 += 1
            else:
                v1 += 1
        except Exception:
            v1 += 1
    return total, v1, v2, v3


def count_categories(skills_dir: Path) -> int:
    """Count top-level category directories under skills/."""
    return sum(1 for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith("."))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def add_dir_to_zip(zf: zipfile.ZipFile, source_dir: Path, prefix: str) -> int:
    """Recursively add all files from source_dir into the zip under prefix/.
    Returns count of files added."""
    count = 0
    if not source_dir.exists():
        print(f"  ⚠️  Directory not found, skipping: {source_dir}", file=sys.stderr)
        return 0
    for file_path in sorted(source_dir.rglob("*")):
        if file_path.is_file() and not file_path.name.startswith("."):
            arcname = f"{prefix}/{file_path.relative_to(source_dir)}"
            zf.write(file_path, arcname)
            count += 1
    return count


def build_package(tag: str) -> tuple[Path, dict]:
    """Build the release zip and return (zip_path, manifest_data)."""
    DIST_DIR.mkdir(exist_ok=True)

    zip_name = f"skills-tree-{tag}.zip"
    zip_path = DIST_DIR / zip_name

    # Remove stale artifact if it exists
    if zip_path.exists():
        zip_path.unlink()
        print(f"Removed stale {zip_path.name}")

    # ── Gather counts before building ─────────────────────────────────────────
    total_skills, v1_count, v2_count, v3_count = count_skills(SKILLS_DIR)
    category_count = count_categories(SKILLS_DIR)

    print(f"📦 Building {zip_name}")
    print(f"   Skills : {total_skills} total  (v1={v1_count}, v2={v2_count}, v3={v3_count})")
    print(f"   Categories: {category_count}")

    total_files = 0
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:

        # ── Content directories ───────────────────────────────────────────────
        for source_dir, prefix in CONTENT_DIRS:
            n = add_dir_to_zip(zf, source_dir, prefix)
            print(f"   + {prefix:12s}: {n} files")
            total_files += n

        # ── API files ─────────────────────────────────────────────────────────
        api_files_added = 0
        for api_file in API_FILES:
            api_path = API_DIR / api_file
            if api_path.exists():
                zf.write(api_path, f"api/{api_file}")
                api_files_added += 1
            else:
                print(f"  ⚠️  API file not found, skipping: {api_path}", file=sys.stderr)
        print(f"   + {'api':12s}: {api_files_added} files")
        total_files += api_files_added

    # ── Compute zip SHA-256 ────────────────────────────────────────────────────
    zip_sha256 = sha256_file(zip_path)
    zip_size_bytes = zip_path.stat().st_size

    manifest = {
        "name": "Skills Tree",
        "tag": tag,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "commit_sha": os.environ.get("GITHUB_SHA", "unknown"),
        "skill_count": total_skills,
        "battle_tested_count": v3_count,
        "expanded_count": v2_count,
        "stub_count": v1_count,
        "category_count": category_count,
        "total_files_in_zip": total_files,
        "zip_filename": zip_name,
        "zip_size_bytes": zip_size_bytes,
        "zip_sha256": zip_sha256,
        "download_url": f"https://github.com/SamoTech/skills-tree/releases/download/{tag}/{zip_name}",
        "api_url": "https://samotech.github.io/skills-tree/api/skills.json",
        "schema_url": "https://samotech.github.io/skills-tree/api/skills-schema.json",
    }

    manifest_path = DIST_DIR / "MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n✅ Done.")
    print(f"   Zip     : {zip_path}")
    print(f"   Size    : {zip_size_bytes / 1024:.1f} KB")
    print(f"   Files   : {total_files}")
    print(f"   SHA-256 : {zip_sha256}")
    print(f"   Manifest: {manifest_path}")

    return zip_path, manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a Skills Tree release package zip + MANIFEST."
    )
    parser.add_argument(
        "--tag",
        required=True,
        help="Release tag, e.g. v2.3.0",
    )
    args = parser.parse_args()

    if not args.tag.startswith("v"):
        print(f"ERROR: tag must start with 'v' (got: {args.tag})", file=sys.stderr)
        sys.exit(1)

    build_package(args.tag)


if __name__ == "__main__":
    main()
