from tools.apply_agent_skills_reconciliation import _rewrite_package_name


def test_rewrite_package_name_updates_frontmatter_only():
    text = """---
name: audio-transcription
description: Audio transcription.
metadata:
  source: skills/01-perception/audio-transcription.md
---

# Audio Transcription
"""
    updated = _rewrite_package_name(text, "perception-audio-transcription")
    assert "name: perception-audio-transcription" in updated
    assert "description: Audio transcription." in updated
    assert "# Audio Transcription" in updated
