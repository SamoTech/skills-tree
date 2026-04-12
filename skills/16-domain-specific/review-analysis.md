**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Aggregates and analyses customer reviews to extract themes, sentiment distribution, product attribute ratings, and verbatim quote highlights. Produces actionable insight summaries for product, marketing, and support teams.

### Example
```python
import anthropic, json

client = anthropic.Anthropic()

def analyse_reviews(reviews: list[str]) -> dict:
    text = "\n".join(f"- {r}" for r in reviews)
    prompt = (
        "Analyse these customer reviews. Return JSON: {overall_sentiment, "
        "top_positives: [str], top_negatives: [str], recurring_themes: [str], "
        "net_promoter_estimate: int}.\n\n" + text
    )
    resp = client.messages.create(
        model="claude-opus-4-5", max_tokens=600,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(resp.content[0].text)

reviews = ["Battery is incredible", "Keyboard feels cheap", "Best laptop I've owned",
           "Runs hot under load", "Display is stunning"]
print(analyse_reviews(reviews))
```

### Related Skills
- [Data Summarization](../12-data/data-summarization.md)
- [SEO Optimization](seo-optimization.md)
