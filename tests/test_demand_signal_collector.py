from __future__ import annotations

import json

from tools.collect_demand_signals import collect


def test_collect_normalizes_public_issue_evidence(monkeypatch):
    calls = []

    def fake_request(url):
        calls.append(url)
        return [{
            "number": 7,
            "title": "Request memory capability",
            "html_url": "https://github.com/example/project/issues/7",
            "repository_url": "https://api.github.com/repos/example/project",
            "state": "open",
            "created_at": "2026-10-01T00:00:00Z",
            "updated_at": "2026-10-02T00:00:00Z",
            "labels": [{"name": "feature"}, {"name": "memory"}],
        }, {
            "number": 8,
            "title": "Pull request",
            "html_url": "https://github.com/example/project/pull/8",
            "repository_url": "https://api.github.com/repos/example/project",
            "state": "open",
            "created_at": "2026-10-01T00:00:00Z",
            "updated_at": "2026-10-02T00:00:00Z",
            "labels": [],
            "pull_request": {"url": "https://api.github.com/repos/example/project/pulls/8"},
        }]

    monkeypatch.setattr("tools.collect_demand_signals._request", fake_request)
    result = collect({
        "sources": [{
            "id": "fixture",
            "type": "github_issue_search",
            "queries": ["repo:example/project is:issue memory"],
        }]
    }, "2026-10-04T00:00:00Z")

    assert len(calls) == 1
    assert result["method"] == "public GitHub issue search"
    assert len(result["signals"]) == 1
    assert result["signals"][0]["repository"] == "example/project"
    assert result["signals"][0]["issue_number"] == 7
    assert result["signals"][0]["labels"] == ["feature", "memory"]
    assert result["signals"][0]["observed_at"] == "2026-10-04T00:00:00Z"


def test_signal_order_is_deterministic(monkeypatch):
    def fake_request(url):
        return [
            {"number": 2, "title": "B", "html_url": "https://github.com/a/b/issues/2",
             "repository_url": "https://api.github.com/repos/a/b", "state": "open",
             "created_at": "2026-01-01T00:00:00Z", "updated_at": "2026-01-02T00:00:00Z", "labels": []},
            {"number": 1, "title": "A", "html_url": "https://github.com/a/b/issues/1",
             "repository_url": "https://api.github.com/repos/a/b", "state": "open",
             "created_at": "2026-01-01T00:00:00Z", "updated_at": "2026-01-02T00:00:00Z", "labels": []},
        ]

    monkeypatch.setattr("tools.collect_demand_signals._request", fake_request)
    config = {"sources": [{"id":"fixture","type":"github_issue_search","queries":["q"]}]}
    result = collect(config, "2026-10-04T00:00:00Z")
    assert [item["issue_number"] for item in result["signals"]] == [1, 2]
