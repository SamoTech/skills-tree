---
name: popup-dialog-handling
description: Detect, classify, and respond to browser popups and modal dialogs during automation, including alert, confirm, beforeunload, and permission prompts, without blocking the run.
metadata:
  source: skills/11-web/popup-dialog-handling.md
  category: 11-web
  version: "v1"
---

# Popup and Dialog Handling

Category: Web | Level: intermediate | Stability: experimental | Version: v1

## Description

Dialog handling is a policy problem, not just a dismissal problem. The skill registers handlers before navigation, classifies each interruption by its browser API rather than its appearance, matches it against an expected set, and applies an explicit policy: accept, refuse, or escalate to review. Every decision is logged with the full message text so the run can be audited later.

## When to Use

Use when automation must dismiss, accept, or inspect popup windows, native dialogs, cookie banners, or modal overlays that interrupt page interaction.

Do not blanket-dismiss every dialog. Some confirm dialogs authorize irreversible actions and must be refused by default or surfaced to an operator for review.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `page` | `object` | Yes | Live browser page or session object |
| `expected` | `map` | No | Dialog kinds mapped to approved responses for this run |
| `policy` | `enum` | No | Default action for unexpected dialogs: `refuse` (default), `accept`, or `review` |

## Procedure

1. Register dialog and popup handlers before navigation so no interruption can block the run.
2. Classify each interruption by browser API type: native dialog, popup window, or in-page overlay.
3. Match the dialog against the expected set; unexpected dialogs route to the review policy.
4. Apply the policy action and record the dialog message and the chosen response.
5. Verify page state after dismissal; some dialogs trigger navigation or reload.
6. Report any dialog that required manual review with its complete message text.

## Outputs

| Output | Type | Description |
|---|---|---|
| `dialog_log` | `array` | Every dialog observed with kind, message, and applied response |
| `action_results` | `object` | Page state after each dismissal, including any navigation |
| `escalations` | `list` | Dialogs that could not be resolved without operator review |

## Runnable Example

```python
def classify_dialogs(dialogs, expected, default_policy="refuse"):
    """dialogs: [(kind, message)]"""
    plan = []
    for kind, message in dialogs:
        if kind in expected:
            action = expected[kind]
        elif kind == "confirm":
            action = "refuse"
        else:
            action = default_policy
        plan.append({"kind": kind, "action": action, "message": message})
    return plan

print(classify_dialogs(
    [("alert", "Session expires in 5 minutes"),
     ("confirm", "Delete all records?"),
     ("beforeunload", "Leave site with unsaved changes?")],
    {"alert": "accept", "beforeunload": "accept"},
))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Automation hangs on dialog | No handler registered before the dialog fired | Register handlers prior to navigation, always |
| Confirm dialog auto-accepted | Destructive confirmation treated as dismissible | Default confirm dialogs to refuse or manual review |
| Dialog race after reload | Handler detached mid-navigation | Re-register handlers on every navigation event |
| Cookie banner misread as dialog | In-page overlay classified as a native dialog | Classify by browser API, not visual similarity |
| Lost dialog message | Dismissal logged without content | Capture full message text before responding |

## Security and Authority Boundary

Dialogs can be forged by a page to phish credentials or manufacture consent. Never enter secrets into a dialog, and treat unexpected authentication or permission prompts as suspicious until their origin is verified.

## Evidence

This skill is grounded in dated public implementation references:

1. The MDN reference for the HTML dialog element (https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog).
2. The Playwright dialogs documentation (https://playwright.dev/python/docs/dialogs).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Browser Navigation](browser-navigation.md) — the navigation lifecycle whose beforeunload events trigger dialogs.
- [Form Filling](form-filling.md) — in-page overlays that often wrap forms and must be cleared before filling.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
