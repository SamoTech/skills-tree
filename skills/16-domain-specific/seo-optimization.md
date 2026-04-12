**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Analyses and improves on-page SEO factors including title tags, meta descriptions, heading hierarchy, keyword density, internal linking, schema markup, and Core Web Vitals recommendations. Supports both content creation and technical auditing workflows.

### Example
```python
import re

def seo_audit(html: str, target_keyword: str) -> dict:
    title = re.search(r"<title>(.*?)</title>", html, re.I)
    desc = re.search(r'name=["\']description["\'].*?content=["\']([^"\']+)', html, re.I)
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.I)
    kw_count = html.lower().count(target_keyword.lower())
    word_count = len(re.sub(r"<[^>]+>", "", html).split())
    density = round(kw_count / max(word_count, 1) * 100, 2)
    return {
        "title_ok": bool(title) and target_keyword.lower() in (title.group(1).lower()),
        "meta_desc": bool(desc),
        "h1_count": len(h1s),
        "keyword_density_pct": density,
        "word_count": word_count,
    }

html = "<title>Best SSD for Developers 2026</title><h1>Best SSD for Developers</h1><p>best ssd</p>"
print(seo_audit(html, "best ssd"))
```

### Related Skills
- [Product Description Writing](product-description.md)
- [Web Scraping](../11-web/web-scraping.md)
