from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAYBOOK = ROOT / "skills/social-accessibility-distribution/references/multiplatform-distribution-architecture-v1.md"
S11 = ROOT / "skills/social-accessibility-distribution/SKILL.md"
SUITE = ROOT / "tests/social-distribution-cases.json"
TRACE = ROOT / "tests/social-distribution-traceability.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_instagram_capability_inventory_has_all_three_classes():
    text = PLAYBOOK.read_text(encoding="utf-8")
    rows = re.findall(r"^\| (IG-\d{2}) \| [^|]+ \| (ADOPTABLE|PARTIAL|ABSENT) \|", text, flags=re.M)
    assert len(rows) == 18
    ids = [row[0] for row in rows]
    assert ids == [f"IG-{i:02d}" for i in range(1, 19)]
    classes = [row[1] for row in rows]
    assert classes.count("ADOPTABLE") == 1
    assert classes.count("PARTIAL") == 8
    assert classes.count("ABSENT") == 9


def test_four_platforms_keep_distinct_discovery_surfaces():
    text = PLAYBOOK.read_text(encoding="utf-8")
    for heading in ("### 4.1 Instagram", "### 4.2 Facebook", "### 4.3 TikTok", "### 4.4 YouTube"):
        assert heading in text
    requirements = {
        "Instagram": ("Feed", "Reels", "Stories", "Explore", "Search"),
        "Facebook": ("Feed", "Reels", "Pages", "Groups", "original"),
        "TikTok": ("For You", "Following", "Friends", "Search", "LIVE", "eligibility"),
        "YouTube": ("Home", "Suggested", "Search", "Shorts", "Subscriptions", "Live")
    }
    platforms = ("Instagram", "Facebook", "TikTok", "YouTube")
    for index, platform in enumerate(platforms, start=1):
        start = text.index(f"### 4.{index} {platform}")
        next_heading = text.find("\n### 4.", start + 1)
        section = text[start:] if next_heading < 0 else text[start:next_heading]
        for term in requirements[platform]:
            assert term.lower() in section.lower(), f"{platform} missing {term}"


def test_s11_preserves_promkes_ownership_and_hard_guardrails():
    text = S11.read_text(encoding="utf-8")
    for term in ("S02", "Fact Lock", "S03", "S12", "S14", "no S15", "diagnosis", "unsolicited bulk"):
        assert term.lower() in text.lower()
    assert "no performance or algorithmic outcome is guaranteed" in text.lower()


def test_social_acceptance_suite_is_separate_and_not_run():
    suite = load(SUITE)
    assert suite["suite_status"] == "SPECIFICATION_ONLY_NOT_RUN"
    assert suite["owner_skill"] == "social-accessibility-distribution"
    cases = suite["cases"]
    assert len(cases) == 34
    ids = [case["test_id"] for case in cases]
    assert ids == [f"SD-{i:03d}" for i in range(1, 35)]
    assert all(case["status"] == "NOT_RUN" for case in cases)
    assert all(case["owner_skill"] == "social-accessibility-distribution" for case in cases)


def test_social_traceability_is_complete_and_one_to_one():
    suite = load(SUITE)
    trace = load(TRACE)
    test_ids = {case["test_id"] for case in suite["cases"]}
    assert set(trace["cases"]) == test_ids
    req_ids = {item["requirement_id"] for item in trace["requirements"]}
    out_ids = {item["output_id"] for item in trace["outputs"]}
    for test_id, record in trace["cases"].items():
        assert record["owner_skill"] == "social-accessibility-distribution"
        assert record["requirement_ids"]
        assert record["output_ids"]
        assert set(record["requirement_ids"]) <= req_ids
        assert set(record["output_ids"]) <= out_ids
        assert set(record["dependency_ids"]) <= test_ids


def test_existing_v4_acceptance_inventories_are_untouched():
    baseline = load(ROOT / "tests/acceptance-cases.json")
    reference = load(ROOT / "tests/reference-output-cases.json")
    assert len(baseline["cases"]) == 45
    assert len(reference["cases"]) == 13
    assert baseline["suite_status"] == "SPECIFICATION_ONLY_NOT_RUN"
    assert reference["suite_status"] == "SPECIFICATION_ONLY_NOT_RUN"
    assert all(case["status"] == "NOT_RUN" for case in baseline["cases"])
    assert all(case["status"] == "NOT_RUN" for case in reference["cases"])
