import os, re

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

def slug_to_title(slug):
    CAPS = {"API","SQL","OCR","RAG","PDF","HTML","XML","JSON","HTTP","CSV","ETL","LLM","DOM","RSS","VM","OS","TTS","ASR","RPC","VQA","SBOM"}
    return " ".join(w.upper() if w.upper() in CAPS else w.capitalize() for w in slug.replace("-"," ").split())

def extract_section(content, *headings):
    for h in headings:
        m = re.search(rf"#{{{2,3}}}\s+{re.escape(h)}\s*\n+(.*?)(?=\n#|\Z)", content, re.DOTALL|re.IGNORECASE)
        if m:
            txt = re.sub(r"\s+", " ", m.group(1).strip())
            if len(txt) > 200:
                idx = txt.rfind(".", 0, 200)
                txt = (txt[:idx+1] if idx > 50 else txt[:197]+"...").strip()
            return txt
    return None

def parse_level(raw):
    r = (raw or "").lower()
    return "basic" if "basic" in r or "beginner" in r else "advanced" if "advanced" in r else "intermediate"

def parse_stability(raw):
    r = (raw or "").lower()
    return "experimental" if "exp" in r else "deprecated" if "dep" in r else "stable"

def fix_file(path, cat):
    try:
        content = open(path, encoding="utf-8").read()
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
        body = content[end+4:]
        fields, field_order = {}, []
        for line in fm_raw.split("\n"):
            m = re.match(r"^([a-z][\w-]*):\s*(.*)$", line)
            if m:
                val = m.group(2).strip()
                if val and val != ">":
                    fields[m.group(1)] = val
                    field_order.append(m.group(1))
        changed = False
        if fields.get("category") != correct_cat:
            fields["category"] = correct_cat; changed = True
        for field in REQUIRED:
            if field not in fields:
                changed = True
                if field == "title":
                    h1 = re.search(r"^#\s+(.+)$", body, re.M)
                    t = re.sub(r"!\[.*?\]\(.*?\)", "", h1.group(1)).strip() if h1 else ""
                    fields["title"] = f'"{t or slug_to_title(slug)}"'
                elif field == "level":
                    raw = re.search(r"Skill\s*Level[:\*`\s]+(\w+)", body, re.I)
                    fields["level"] = parse_level(raw.group(1) if raw else "")
                elif field == "stability":
                    raw = re.search(r"Stability[:\*`\s]+(\w+)", body, re.I)
                    fields["stability"] = parse_stability(raw.group(1) if raw else "")
                elif field == "description":
                    desc = extract_section(body, "Description", "What It Does", "Overview", "Summary")
                    if not desc:
                        desc = f"Apply {slug_to_title(slug).lower()} in AI agent workflows."
                    fields["description"] = f'"{desc.replace(chr(34), chr(39))}"'
        if not changed:
            return False
        ORDER = ["title","category","level","stability","description","added","version","tags","updated","dependencies","phase","badge","badge_key","author"]
        extra = [k for k in field_order if k not in ORDER]
        lines = [f"{k}: {fields[k]}" for k in ORDER + extra if k in fields]
        body = re.sub(r'^added:\s*"[\d-]+"[\r\n]+', "", body, flags=re.M)
        new = "---\n" + "\n".join(lines) + "\n---\n" + body
    else:
        clean = re.sub(r'^added:\s*"[\d-]+"[\r\n]*', "", content, flags=re.M)
        h1 = re.search(r"^#\s+(.+)$", clean, re.M)
        title = re.sub(r"!\[.*?\]\(.*?\)", "", h1.group(1)).strip() if h1 else ""
        if not title: title = slug_to_title(slug)
        raw_l = re.search(r"Skill\s*Level[:\*`\s]+(\w+)", clean, re.I)
        level = parse_level(raw_l.group(1) if raw_l else "")
        raw_s = re.search(r"Stability[:\*`\s]+(\w+)", clean, re.I)
        stability = parse_stability(raw_s.group(1) if raw_s else "")
        desc = extract_section(clean, "Description", "What It Does", "Overview", "Summary")
        if not desc: desc = f"Apply {title.lower()} in AI agent workflows."
        desc = desc.replace('"', "'")[:200]
        fm = f'---\ntitle: "{title}"\ncategory: {correct_cat}\nlevel: {level}\nstability: {stability}\ndescription: "{desc}"\nadded: "2025-03"\n---\n\n'
        new = fm + clean

    open(path, "w", encoding="utf-8", newline="\n").write(new)
    return True

fixed = 0
for cat in CAT_MAP:
    folder = f"skills/{cat}"
    if not os.path.isdir(folder): continue
    for fname in sorted(os.listdir(folder)):
        if fname.endswith(".md") and fname != "README.md":
            if fix_file(os.path.join(folder, fname), cat):
                print(f"Fixed: skills/{cat}/{fname}")
                fixed += 1
print(f"\nDone. {fixed} files modified.")
