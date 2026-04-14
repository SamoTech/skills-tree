import os
import re
import sys
import tempfile

CAT_MAP = {
    "01-perception": "01-perception", "02-reasoning": "02-reasoning",
    "03-memory": "03-memory", "04-action-execution": "04-action-execution",
    "05-code": "05-code", "06-communication": "06-communication",
    "07-tool-use": "07-tool-use", "08-multimodal": "08-multimodal",
    "09-agentic-patterns": "09-agentic-patterns", "10-computer-use": "10-computer-use",
    "11-web": "11-web", "12-data": "12-data", "13-creative": "13-creative",
    "14-security": "14-security", "15-orchestration": "15-orchestration",
    "16-domain-specific": "16-domain-specific",
}
REQUIRED = ["title", "category", "level", "stability", "description"]

# Ordered list of known frontmatter keys used when rebuilding.
# Keys found in the original file but absent from this list are appended
# verbatim at the end so they are never silently discarded.
ORDER = [
    "title", "category", "level", "stability", "description",
    "added", "version", "tags", "updated", "dependencies",
    "phase", "badge", "badge_key", "author",
]


def slug_to_title(slug):
    CAPS = {
        "API", "SQL", "OCR", "RAG", "PDF", "HTML", "XML", "JSON",
        "HTTP", "CSV", "ETL", "LLM", "DOM", "RSS", "VM", "OS",
        "TTS", "ASR", "RPC", "VQA", "SBOM",
    }
    return " ".join(
        w.upper() if w.upper() in CAPS else w.capitalize()
        for w in slug.replace("-", " ").split()
    )


def extract_section(content, *headings):
    for h in headings:
        m = re.search(
            rf"#{{{2,3}}}\s+{re.escape(h)}\s*\n+(.*?)(?=\n#|\Z)",
            content, re.DOTALL | re.IGNORECASE,
        )
        if m:
            txt = re.sub(r"\s+", " ", m.group(1).strip())
            if len(txt) > 200:
                idx = txt.rfind(".", 0, 200)
                txt = (txt[:idx + 1] if idx > 50 else txt[:197] + "...").strip()
            return txt
    return None


def parse_level(raw):
    r = (raw or "").lower()
    return "basic" if "basic" in r or "beginner" in r else "advanced" if "advanced" in r else "intermediate"


def parse_stability(raw):
    r = (raw or "").lower()
    return "experimental" if "exp" in r else "deprecated" if "dep" in r else "stable"


def _parse_frontmatter(fm_raw):
    """Parse a raw frontmatter string into two parallel structures.

    Returns:
        scalars  : dict[str, str]   – key → single-line value (for comparison/overwrite)
        segments : list[(str, str)] – ordered (key, raw_block) pairs preserving
                                      multiline values verbatim

    A "raw_block" is the complete original text for that key, e.g.:
        dependencies:\n  - package: anthropic\n    tested_version: "0.49.0"\n

    Keys whose value is a block (indented continuation lines, YAML list `- …`
    entries, or literal/folded block scalars `|`/`>`) are stored in `segments`
    with their full text but are absent from `scalars` — they must be written
    back verbatim and must NOT be overwritten by the scalar rewriter.
    """
    scalars = {}
    segments = []  # list of (key, raw_block_text)

    lines = fm_raw.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        # Top-level key: no leading whitespace
        if line and not line[0].isspace():
            m = re.match(r"^([a-z][\w-]*):\s*(.*)$", line)
            if m:
                key = m.group(1)
                first_val = m.group(2).strip()
                # Collect any indented continuation lines that belong to this key
                block_lines = [line]
                j = i + 1
                while j < len(lines) and lines[j] and lines[j][0].isspace():
                    block_lines.append(lines[j])
                    j += 1
                raw_block = "\n".join(block_lines)
                segments.append((key, raw_block))
                # Only populate scalars for genuinely single-line values
                # (no continuation lines, not a block scalar indicator)
                is_multiline = j > i + 1
                is_block_scalar = first_val in ("|", ">", "|+", "|-", ">+", ">-")
                is_empty = first_val == ""
                if not is_multiline and not is_block_scalar and not is_empty:
                    if first_val != ">":  # legacy guard kept from original
                        scalars[key] = first_val
                i = j
                continue
        i += 1

    return scalars, segments


def _rebuild_frontmatter(segments, scalars, overrides, path):
    """Rebuild frontmatter lines in ORDER, then append any extra keys.

    Parameters:
        segments  : original (key, raw_block) pairs from _parse_frontmatter
        scalars   : original scalar values (read-only reference for unchanged fields)
        overrides : dict[str, str] of scalar key→value lines that must be updated
                    (e.g. category correction, newly synthesised REQUIRED fields)
        path      : file path — used only for [WARN] messages

    Returns a list of strings (one per frontmatter line) ready to join with \n.

    Preservation guarantee: every key that was present in *segments* will appear
    in the output.  If a key would be dropped, a [WARN] is printed to stderr.
    """
    # Build lookup: key → raw_block (original text) for quick access
    seg_map = dict(segments)       # last writer wins for duplicates (shouldn't happen)
    all_original_keys = [k for k, _ in segments]

    output_lines = []
    emitted = set()

    # 1. Emit ORDER keys first (preserves canonical ordering)
    for key in ORDER:
        if key in overrides:
            # Scalar override (category fix or newly synthesised field)
            output_lines.append(f"{key}: {overrides[key]}")
            emitted.add(key)
        elif key in seg_map:
            # Preserve original raw block (handles multiline values)
            output_lines.append(seg_map[key])
            emitted.add(key)
        # Keys in ORDER but absent from the file are simply skipped (not added)

    # 2. Emit extra keys not in ORDER — verbatim from original
    for key in all_original_keys:
        if key not in emitted:
            if key in overrides:
                output_lines.append(f"{key}: {overrides[key]}")
            else:
                output_lines.append(seg_map[key])
            emitted.add(key)

    # 3. Safety check: warn about any original key that ended up missing
    for key in all_original_keys:
        if key not in emitted:
            print(
                f"[WARN] {path}: frontmatter key '{key}' could not be preserved "
                f"and was dropped — manual review required.",
                file=sys.stderr,
            )

    return output_lines


def _atomic_write(path, content):
    """Write *content* to *path* atomically using a sibling temp file + os.replace().

    os.replace() maps to rename(2) on POSIX — atomic by POSIX spec.
    On Windows it replaces the destination in a single syscall (best-effort atomic).
    The temp file lives in the same directory as the target so os.replace() never
    crosses a filesystem boundary (which would make it non-atomic on Linux).
    The except block guarantees the .tmp file is removed even on error.
    """
    dir_ = os.path.dirname(os.path.abspath(path))
    fd, tmp_path = tempfile.mkstemp(dir=dir_, suffix=".tmp", prefix=".fix-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def fix_file(path, cat):
    try:
        # Normalise CRLF → LF so frontmatter regex works on Windows-authored files.
        content = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    except Exception:
        return False

    slug = os.path.basename(path)[:-3]
    correct_cat = CAT_MAP[cat]
    has_fm = content.startswith("---\n")

    if has_fm:
        end = content.find("\n---\n", 3)
        if end == -1:
            return False
        fm_raw = content[4:end]
        body = content[end + 4:]

        scalars, segments = _parse_frontmatter(fm_raw)
        # overrides: scalar replacements/additions that will supersede the original
        overrides = {}
        changed = False

        # ── Category correction ──────────────────────────────────────────────
        if scalars.get("category") != correct_cat:
            overrides["category"] = correct_cat
            changed = True

        # ── Synthesise any missing REQUIRED fields ───────────────────────────
        existing_keys = {k for k, _ in segments}
        for field in REQUIRED:
            if field not in existing_keys and field not in scalars:
                changed = True
                if field == "title":
                    h1 = re.search(r"^#\s+(.+)$", body, re.M)
                    t = re.sub(r"!\[.*?\]\(.*?\)", "", h1.group(1)).strip() if h1 else ""
                    overrides["title"] = f'"{t or slug_to_title(slug)}"'
                elif field == "level":
                    raw = re.search(r"Skill\s*Level[:\*`\s]+(\w+)", body, re.I)
                    overrides["level"] = parse_level(raw.group(1) if raw else "")
                elif field == "stability":
                    raw = re.search(r"Stability[:\*`\s]+(\w+)", body, re.I)
                    overrides["stability"] = parse_stability(raw.group(1) if raw else "")
                elif field == "description":
                    desc = extract_section(body, "Description", "What It Does", "Overview", "Summary")
                    if not desc:
                        desc = f"Apply {slug_to_title(slug).lower()} in AI agent workflows."
                    overrides["description"] = f'"{desc.replace(chr(34), chr(39))}"'

        if not changed:
            return False

        fm_lines = _rebuild_frontmatter(segments, scalars, overrides, path)
        # Strip legacy `added:` lines from the *body* only (old-format artefact).
        body = re.sub(r'^added:\s*"[\d-]+"[\r\n]+', "", body, flags=re.M)
        new = "---\n" + "\n".join(fm_lines) + "\n---\n" + body

    else:
        # No frontmatter at all — synthesise a minimal block from body content.
        clean = re.sub(r'^added:\s*"[\d-]+"[\r\n]*', "", content, flags=re.M)
        h1 = re.search(r"^#\s+(.+)$", clean, re.M)
        title = re.sub(r"!\[.*?\]\(.*?\)", "", h1.group(1)).strip() if h1 else ""
        if not title:
            title = slug_to_title(slug)
        raw_l = re.search(r"Skill\s*Level[:\*`\s]+(\w+)", clean, re.I)
        level = parse_level(raw_l.group(1) if raw_l else "")
        raw_s = re.search(r"Stability[:\*`\s]+(\w+)", clean, re.I)
        stability = parse_stability(raw_s.group(1) if raw_s else "")
        desc = extract_section(clean, "Description", "What It Does", "Overview", "Summary")
        if not desc:
            desc = f"Apply {title.lower()} in AI agent workflows."
        desc = desc.replace('"', "'")[:200]
        fm = (
            f'---\ntitle: "{title}"\ncategory: {correct_cat}\n'
            f'level: {level}\nstability: {stability}\n'
            f'description: "{desc}"\nadded: "2025-03"\n---\n\n'
        )
        new = fm + clean

    _atomic_write(path, new)
    return True


def main():
    fixed = 0
    for cat in CAT_MAP:
        folder = f"skills/{cat}"
        if not os.path.isdir(folder):
            continue
        for fname in sorted(os.listdir(folder)):
            if fname.endswith(".md") and fname != "README.md":
                if fix_file(os.path.join(folder, fname), cat):
                    print(f"Fixed: skills/{cat}/{fname}")
                    fixed += 1
    print(f"\nDone. {fixed} files modified.")


if __name__ == "__main__":
    main()
