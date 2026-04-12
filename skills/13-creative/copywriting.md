**Category:** Creative
**Skill Level:** Intermediate
**Stability:** stable
**Added:** 2025-03

### Description
Crafts persuasive marketing and advertising copy — headlines, CTAs, product descriptions, email campaigns — applying proven frameworks such as AIDA (Attention, Interest, Desire, Action) and PAS (Problem, Agitate, Solution).

### Example
```python
import anthropic

client = anthropic.Anthropic()

prompt = """
Write three headline variants for a productivity SaaS app using the AIDA framework.
Product: FocusFlow — a Pomodoro timer with AI scheduling.
Target audience: remote software developers.
Keep each headline under 12 words.
"""

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=256,
    messages=[{"role": "user", "content": prompt}]
)
print(message.content[0].text)
```

### Related Skills
- [Tone Adjustment](../06-communication/tone-adjustment.md)
- [Social Media Post Generation](social-media-post.md)
- [Email Drafting](../06-communication/email-drafting.md)
